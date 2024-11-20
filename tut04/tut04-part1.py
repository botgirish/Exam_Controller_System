students = {}

n = int(input("Enter the number of students: "))

for i in range(n):
    name = input(f"Enter name for student {i + 1}: ")
    marks_input = input(f"Enter marks for '{name}' separated by spaces: ")
    marks = [int(mark) for mark in marks_input.split()]
    students[name] = marks
print(students)

student_list = []
for name in students:
    marks = students[name]
    average_marks = sum(marks) / len(marks)
    student_list.append((name, average_marks))

for i in range(len(student_list)):
    for j in range(0, len(student_list)-i-1):
        if student_list[j][1] < student_list[j + 1][1]:
            student_list[j], student_list[j + 1] = student_list[j + 1], student_list[j]

print("")
print("Students sorted by average marks:")
for name, average in student_list:
    print(f"{name} - Average: {average:.2f}")
