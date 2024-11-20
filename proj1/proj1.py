
from datetime import datetime
start_time = datetime.now()

#Help
def proj_chat_tool():
	pass


###Code




import pandas as pd
import os

# Function to load input Excel data
def load_excel_data(file_path):
    data_1 = pd.read_excel(file_path, sheet_name="ip_1", skiprows=1)
    data_1.columns = ['roll_number', 'registration_sem', 'schedule_sem', 'subject_code']
    data_2 = pd.read_excel(file_path, sheet_name="ip_2", skiprows=1)
    data_2.columns = ['Date', 'Day', 'AM_Session', 'PM_Session']
    data_3 = pd.read_excel(file_path, sheet_name="ip_3")
    data_3.columns = ['Room_ID', 'Max_Students', 'Block_ID']
    data_4 = pd.read_excel(file_path, sheet_name="ip_4")
    data_4.columns = ['Roll', 'Full_Name']
    vacant_data = pd.read_excel(file_path, sheet_name="op_2", skiprows=1)
    vacant_data.columns = ['Room_ID', 'Max_Students', 'Block_ID', 'Vacant_Seats']
    return data_1, data_2, data_3, data_4, vacant_data

# Function to create attendance sheets
def create_attendance_sheets(plan, student_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for _, record in plan.iterrows():
        if pd.isna(record["Date"]):  # Skip rows with missing or invalid dates
            continue

        date_str = pd.to_datetime(record["Date"]).strftime("%d_%m_%Y")
        session = record["Session"]
        subject = record["subject_code"]
        room_id = record["Room"]
        roll_numbers = record["Roll_list"].split(";")

        # Filter student data based on roll numbers
        filtered_students = student_data[student_data["Roll"].isin(roll_numbers)]

        # Prepare attendance sheet data
        attendance_data = filtered_students.copy()
        attendance_data["Signature"] = ""  # Column for student signatures

        # Add rows for invigilator and TA signatures
        empty_rows = pd.DataFrame([{"Roll": "", "Full_Name": "", "Signature": ""} for _ in range(5)])
        attendance_data = pd.concat([attendance_data, empty_rows], ignore_index=True)

        # Save the attendance sheet
        file_name = f"{date_str}{subject}{room_id}_{session.lower()}.xlsx"
        file_path = os.path.join(output_dir, file_name)
        attendance_data.to_excel(file_path, index=False, columns=["Roll", "Full_Name", "Signature"])

# Function to arrange seating
def arrange_seating(exam_data, schedule_data, room_data, student_data, buffer=5, dense_allocation=True):
    arrangement_plan = []
    available_seats_by_session = {}

    room_data_sorted = room_data.sort_values(by=['Block_ID', 'Max_Students'], ascending=[True, False])

    for _, schedule in schedule_data.iterrows():
        date, weekday = schedule["Date"], schedule["Day"]
        sessions = [("AM_Session", schedule["AM_Session"]), ("PM_Session", schedule["PM_Session"])]

        for session, subjects in sessions:
            session_id = f"{weekday}_{session}"
            vacant_rooms = {room: cap - buffer for room, cap in zip(room_data["Room_ID"], room_data["Max_Students"])}
            available_seats_by_session[session_id] = vacant_rooms.copy()

            if pd.isna(subjects) or subjects.strip().upper() == "NO EXAM":
                continue

            subject_list = [subj.strip() for subj in subjects.split(";")]
            subject_sizes = {}

            remaining_students = {}
            for subject in subject_list:
                enrolled_students = exam_data[exam_data["subject_code"] == subject]
                if enrolled_students.empty:
                    continue
                enrolled_students = enrolled_students.merge(student_data, left_on="roll_number", right_on="Roll")
                remaining_students[subject] = enrolled_students
                subject_sizes[subject] = len(enrolled_students)

            sorted_subjects = sorted(subject_sizes.keys(), key=lambda sub: subject_sizes[sub], reverse=True)

            for _, room in room_data_sorted.iterrows():
                room_id = room["Room_ID"]
                capacity = vacant_rooms[room_id]
                if capacity <= 0:
                    continue

                allocated_rolls = []

                for subject in sorted_subjects:
                    if subject not in remaining_students:
                        continue

                    student_group = remaining_students[subject]
                    if student_group.empty or capacity <= 0:
                        continue

                    max_to_allocate = capacity if dense_allocation else capacity // 2
                    allocation_count = min(len(student_group), max_to_allocate)

                    allocated_students = student_group[:allocation_count]
                    remaining_students[subject] = student_group[allocation_count:]
                    capacity -= allocation_count

                    allocated_rolls.append({
                        "subject_code": subject,
                        "Roll_list": ";".join(allocated_students["roll_number"].tolist()),
                        "Allocated_count": allocation_count,
                    })

                vacant_rooms[room_id] = capacity

                if allocated_rolls:
                    for alloc in allocated_rolls:
                        arrangement_plan.append({
                            "Date": date,
                            "Day": weekday,
                            "Session": session,
                            "subject_code": alloc["subject_code"],
                            "Room": room_id,
                            "Allocated_count": alloc["Allocated_count"],
                            "Roll_list": alloc["Roll_list"],
                        })

            available_seats_by_session[session_id] = vacant_rooms.copy()

    arrangement_df = pd.DataFrame(arrangement_plan)
    return arrangement_df, available_seats_by_session

# Main function
def main(file_path, buffer=5, dense_allocation=True, output_dir="/content/attendance_sheets"):
    data_1, data_2, data_3, data_4, vacant_data = load_excel_data(file_path)

    seating_plan, vacant_details = arrange_seating(data_1, data_2, data_3, data_4, buffer, dense_allocation)

    # Output files
    excel_output = "/content/seating_arrangement.xlsx"
    csv_output = "/content/seating_arrangement.csv"

    # Save seating arrangement and vacant details
    with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
        seating_plan.to_excel(writer, sheet_name="Seating_Arrangement", index=False)

        # Save session-wise vacant seat data
        for session, vacancy in vacant_details.items():
            session_df = vacant_data.copy()
            session_df["Vacant_Seats"] = session_df["Room_ID"].map(vacancy)
            session_df.to_excel(writer, sheet_name=session, index=False)

    # Save arrangement as CSV
    seating_plan.to_csv(csv_output, index=False)

    # Create attendance sheets
    create_attendance_sheets(seating_plan, data_4, output_dir)

    print(f"Seating arrangement saved to {excel_output} and {csv_output}")
    print(f"Attendance sheets stored in: {output_dir}")

# User inputs
file_path = "/content/2024 Python Project Part 1. Group of two.xlsx"
buffer = 5# Buffer size
allocation_type = input("Choose allocation type (dense/sparse): ").strip().lower()
dense_allocation = allocation_type == "dense"

output_dir = "/content/attendance_sheets"
main(file_path, buffer=buffer, dense_allocation=dense_allocation, output_dir=output_dir)








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
