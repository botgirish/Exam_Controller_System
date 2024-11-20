
from datetime import datetime
start_time = datetime.now()

#Help
def proj_chat_tool():
	pass


###Code




#seating arrangement project

import pandas as pd
import os

# Function to process the Excel input
def process_excel(file_path):
    ip_1 = pd.read_excel(file_path, sheet_name="ip_1", skiprows=1)
    ip_1.columns = ['rollno', 'register_sem', 'schedule_sem', 'course_code']
    ip_2 = pd.read_excel(file_path, sheet_name="ip_2", skiprows=1)
    ip_2.columns = ['Date', 'Day', 'Morning', 'Evening']
    ip_3 = pd.read_excel(file_path, sheet_name="ip_3")
    ip_3.columns = ['Room_No', 'Exam_Capacity', 'Block']
    ip_4 = pd.read_excel(file_path, sheet_name="ip_4")
    ip_4.columns = ['Roll', 'Name']
    ip_op2 = pd.read_excel(file_path, sheet_name="op_2", skiprows=1)
    ip_op2.columns = ['Room_No', 'Exam_Capacity', 'Block', 'Vacant']
    return ip_1, ip_2, ip_3, ip_4, ip_op2

# Function to generate attendance sheets
def generate_attendance_sheets(seating_plan, ip_4, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for _, row in seating_plan.iterrows():
        if pd.isna(row["Date"]):  # Skip rows with invalid or missing dates
            continue

        date = pd.to_datetime(row["Date"]).strftime("%d_%m_%Y")
        session = row["Session"]
        course_code = row["course_code"]
        room_no = row["Room"]
        roll_list = row["Roll_list"].split(";")

        # Filter student details
        student_details = ip_4[ip_4["Roll"].isin(roll_list)]

        # Prepare attendance sheet
        attendance_data = student_details.copy()
        attendance_data["Sign"] = ""  # Add a blank column for signatures

        # Add blank rows for invigilator and TA signatures
        blank_rows = pd.DataFrame([{"Roll": "", "Name": "", "Sign": ""} for _ in range(5)])
        attendance_data = pd.concat([attendance_data, blank_rows], ignore_index=True)

        # Save the attendance sheet
        file_name = f"{date}{course_code}{room_no}_{session.lower()}.xlsx"
        file_path = os.path.join(output_folder, file_name)
        attendance_data.to_excel(file_path, index=False, columns=["Roll", "Name", "Sign"])

# Function to generate seating arrangement
def generate_seating_arrangement(ip_1, ip_2, ip_3, ip_4, buffer=5, dense=True):
    seating_plan = []
    session_vacant_data = {}

    ip_3_sorted = ip_3.sort_values(by=['Block', 'Exam_Capacity'], ascending=[True, False])

    for _, exam in ip_2.iterrows():
        date, day = exam["Date"], exam["Day"]
        time_slots = [("Morning", exam["Morning"]), ("Evening", exam["Evening"])]

        for time_slot, courses in time_slots:
            session_key = f"{day}_{time_slot}"
            vacant_seats = {room: cap - buffer for room, cap in zip(ip_3["Room_No"], ip_3["Exam_Capacity"])}
            session_vacant_data[session_key] = vacant_seats.copy()

            if pd.isna(courses) or courses.strip().upper() == "NO EXAM":
                continue

            course_list = [course.strip() for course in courses.split(";")]
            course_sizes = {}

            remaining_students_by_course = {}
            for course in course_list:
                registered_students = ip_1[ip_1["course_code"] == course]
                if registered_students.empty:
                    continue
                registered_students = registered_students.merge(ip_4, left_on="rollno", right_on="Roll")
                remaining_students_by_course[course] = registered_students
                course_sizes[course] = len(registered_students)

            sorted_courses = sorted(course_sizes.keys(), key=lambda c: course_sizes[c], reverse=True)

            for _, room in ip_3_sorted.iterrows():
                room_no = room["Room_No"]
                room_capacity = vacant_seats[room_no]
                if room_capacity <= 0:
                    continue

                allocated_students_in_room = []

                for course in sorted_courses:
                    if course not in remaining_students_by_course:
                        continue

                    students_for_course = remaining_students_by_course[course]
                    if students_for_course.empty or room_capacity <= 0:
                        continue

                    max_allocation = room_capacity if dense else room_capacity // 2
                    allocate_count = min(len(students_for_course), max_allocation)

                    allocated_students = students_for_course[:allocate_count]
                    remaining_students_by_course[course] = students_for_course[allocate_count:]
                    room_capacity -= allocate_count

                    allocated_students_in_room.append({
                        "course_code": course,
                        "Roll_list": ";".join(allocated_students["rollno"].tolist()),
                        "Allocated_students_count": allocate_count,
                    })

                vacant_seats[room_no] = room_capacity

                if allocated_students_in_room:
                    for allocation in allocated_students_in_room:
                        seating_plan.append({
                            "Date": date,
                            "Day": day,
                            "Session": time_slot,
                            "course_code": allocation["course_code"],
                            "Room": room_no,
                            "Allocated_students_count": allocation["Allocated_students_count"],
                            "Roll_list": allocation["Roll_list"],
                        })

            session_vacant_data[session_key] = vacant_seats.copy()

    seating_plan_df = pd.DataFrame(seating_plan)
    return seating_plan_df, session_vacant_data

# Main function
def main(file_path, buffer=5, dense=True, output_folder="/content/attendance_sheets"):
    ip_1, ip_2, ip_3, ip_4, ip_op2 = process_excel(file_path)

    seating_plan, session_vacant_data = generate_seating_arrangement(ip_1, ip_2, ip_3, ip_4, buffer, dense)

    # Define output files
    output_excel = "/content/seating_plan_with_vacant.xlsx"
    output_csv = "/content/seating_plan_with_vacant.csv"

    # Save seating plan and vacant details in Excel
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        seating_plan.to_excel(writer, sheet_name="Seating_Plan", index=False)

        # Add session-wise vacant seat details
        for session_key, vacant_data in session_vacant_data.items():
            session_df = ip_op2.copy()
            session_df["Vacant"] = session_df["Room_No"].map(vacant_data)
            session_df.to_excel(writer, sheet_name=session_key, index=False)

    # Save seating plan as CSV
    seating_plan.to_csv(output_csv, index=False)

    # Generate attendance sheets
    generate_attendance_sheets(seating_plan, ip_4, output_folder)

    # Notify user
    print(f"Seating plan and vacant details saved to {output_excel} and {output_csv}")
    print(f"Attendance sheets saved in: {output_folder}")

# File path and execution
file_path = "/content/2024 Python Project Part 1. Group of two.xlsx"
buffer = 5  # Adjust buffer size
dense = True  # Dense allocation
output_folder = "/content/attendance_sheets"
main(file_path, buffer=buffer, dense=dense, output_folder=output_folder)



from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


proj_chat_tool()






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
