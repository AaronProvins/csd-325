import json
from pathlib import Path

def print_students(student_list):
    for s in student_list:
        print(f"{s['L_Name']}, {s['F_Name']} : ID = {s['Student_ID']} , Email = {s['Email']}")

def main():
    data_path = Path(__file__).parent / "student.json"
    with data_path.open("r") as f:
        students = json.load(f)

    print("\nOriginal Student List:\n")
    print_students(students)

    new_student = {
        "F_Name": "Aaron",
        "L_Name": "Provins",
        "Student_ID": 21420314,
        "Email": "aaprovins@my365.bellevue.edu"
    }
    students.append(new_student)

    print("\nUpdated Student List:\n")
    print_students(students)

    with data_path.open("w") as f:
        json.dump(students, f, indent=4)

    print("\nstudent.json file updated successfully!\n")

if __name__ == "__main__":
    main()
