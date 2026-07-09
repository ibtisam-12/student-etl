import csv
import random
from datetime import date, timedelta

OUTPUT_PATH = "data/enrollments.csv"

DEPARTMENTS = [
    ("D1", "Computer Science"),
    ("D2", "Software Engineering"),
    ("D3", "Information Technology"),
    ("D4", "Business"),
    ("D5", "Mathematics"),
]

INSTRUCTORS = [
    ("I1", "Dr. Khan", "D1"),
    ("I2", "Dr. Ali", "D2"),
    ("I3", "Dr. Ahmed", "D3"),
    ("I4", "Dr. Sana", "D4"),
    ("I5", "Dr. Ayesha", "D5"),
]

COURSES = [
    ("C1", "Database Systems", 3, "D1", "I1"),
    ("C2", "Data Structures", 3, "D1", "I1"),
    ("C3", "Software Design", 3, "D2", "I2"),
    ("C4", "Web Engineering", 3, "D2", "I2"),
    ("C5", "Networks", 3, "D3", "I3"),
    ("C6", "Cyber Security", 3, "D3", "I3"),
    ("C7", "Accounting Basics", 3, "D4", "I4"),
    ("C8", "Marketing", 3, "D4", "I4"),
    ("C9", "Linear Algebra", 3, "D5", "I5"),
    ("C10", "Statistics", 3, "D5", "I5"),
]

SEMESTERS = ["Spring-2025", "Fall-2025", "Spring-2026"]
GRADES = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]

FIRST_NAMES = ["Ali", "Ahmed", "Usman", "Hassan", "Ayesha", "Fatima", "Sana", "Hina", "Zain", "Huzaifa"]
LAST_NAMES = ["Khan", "Raza", "Malik", "Butt", "Sheikh", "Chaudhry", "Mirza", "Iqbal", "Shah", "Aslam"]


def random_date(start: date, end: date) -> str:
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days))
    return d.isoformat()


def main(num_records: int = 150) -> None:
    headers = [
        "student_id", "student_name", "email", "phone",
        "department_id", "department_name",
        "course_id", "course_title", "credit_hours",
        "instructor_id", "instructor_name",
        "semester", "enroll_date", "grade"
    ]

    # create 60 unique students, each can have multiple enrollments
    students = []
    for i in range(1, 61):
        sid = f"S{i:03d}"
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        name = f"{fn} {ln}"
        email = f"{fn.lower()}{i}@example.com"
        phone = f"03{random.randint(0,9)}{random.randint(10000000,99999999)}"
        dept_id, dept_name = random.choice(DEPARTMENTS)
        students.append((sid, name, email, phone, dept_id, dept_name))

    rows = []
    for _ in range(num_records):
        sid, sname, email, phone, dept_id, dept_name = random.choice(students)

        course_id, course_title, credit_hours, _, instructor_id = random.choice(COURSES)
        instr = next((x for x in INSTRUCTORS if x[0] == instructor_id), None)
        instructor_name = instr[1] if instr else 'Unknown'

        semester = random.choice(SEMESTERS)
        enroll_date = random_date(date(2025, 1, 1), date(2026, 12, 31))
        grade = random.choice(GRADES)

        rows.append([
            sid, sname, email, phone,
            dept_id, dept_name,
            course_id, course_title, credit_hours,
            instructor_id, instructor_name,
            semester, enroll_date, grade
        ])

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Generated {len(rows)} records at: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
