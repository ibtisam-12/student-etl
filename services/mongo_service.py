from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

_client = MongoClient(MONGO_URI)

def get_collection():
    return _client[MONGO_DB][MONGO_COLLECTION]


def insert_denormalized_students(records: list[dict]) -> int:
    """
    Store in MongoDB in denormalized form:
      - 1 document per student
      - embedded enrollments list
    """
    col = get_collection()
    col.delete_many({})  # overwrite for demo cleanliness

    grouped = {}

    for r in records:
        sid = r.get("student_id", "").strip()
        if not sid:
            continue

        if sid not in grouped:
            grouped[sid] = {
                "student_id": sid,
                "name": r.get("student_name", "").strip(),
                "email": r.get("email", "").strip(),
                "phone": r.get("phone", "").strip(),
                "department": {
                    "department_id": r.get("department_id", "").strip(),
                    "name": r.get("department_name", "").strip(),
                },
                "enrollments": []
            }

        # Enrollment item (embedded)
        grouped[sid]["enrollments"].append({
            "semester": r.get("semester", "").strip(),
            "enroll_date": r.get("enroll_date", "").strip(),
            "grade": r.get("grade", "").strip(),
            "course": {
                "course_id": r.get("course_id", "").strip(),
                "title": r.get("course_title", "").strip(),
                "credit_hours": safe_int(r.get("credit_hours", "0"))
            },
            "instructor": {
                "instructor_id": r.get("instructor_id", "").strip(),
                "name": r.get("instructor_name", "").strip()
            }
        })

    docs = list(grouped.values())
    if docs:
        col.insert_many(docs)

    return len(docs)


def safe_int(x) -> int:
    try:
        return int(str(x).strip())
    except (ValueError, TypeError):
        return 0


def load_mongo_as_flat_records() -> list[dict]:
    """
    Loads denormalized MongoDB documents and flattens them into row-like dictionaries,
    so SQL can be inserted in normalized form.
    """
    col = get_collection()
    docs = list(col.find({}, {"_id": 0}))

    flat_records: list[dict] = []

    for d in docs:
        dept = d.get("department", {})
        enrollments = d.get("enrollments", [])

        for e in enrollments:
            course = e.get("course", {})
            instr = e.get("instructor", {})

            flat_records.append({
                "student_id": d.get("student_id", ""),
                "student_name": d.get("name", ""),
                "email": d.get("email", ""),
                "phone": d.get("phone", ""),
                "department_id": dept.get("department_id", ""),
                "department_name": dept.get("name", ""),
                "course_id": course.get("course_id", ""),
                "course_title": course.get("title", ""),
                "credit_hours": course.get("credit_hours", 0),
                "instructor_id": instr.get("instructor_id", ""),
                "instructor_name": instr.get("name", ""),
                "semester": e.get("semester", ""),
                "enroll_date": e.get("enroll_date", ""),
                "grade": e.get("grade", "")
            })

    return flat_records


def status():
    col = get_collection()
    students = col.count_documents({})
    # enrollments count (safe)
    enrollments = 0
    for d in col.find({}, {"enrollments": 1}):
        enrollments += len(d.get("enrollments", []))
    return {"students_docs": students, "total_enrollments_embedded": enrollments}

def delete_all_mongo_data() -> int:
    """
    Deletes all documents from the Mongo collection.
    Returns number of deleted documents.
    """
    col = get_collection()
    res = col.delete_many({})
    return res.deleted_count

def delete_one_student_mongo(student_id: str) -> int:
    """
    Deletes one student document by student_id.
    Returns deleted count (0 or 1).
    """
    col = get_collection()
    res = col.delete_one({"student_id": student_id})
    return res.deleted_count
