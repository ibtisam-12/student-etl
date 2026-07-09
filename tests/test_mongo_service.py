from services.mongo_service import safe_int, insert_denormalized_students

class TestSafeInt:
    def test_valid_int_string(self):
        assert safe_int("42") == 42

    def test_valid_int(self):
        assert safe_int(42) == 42

    def test_empty_string(self):
        assert safe_int("") == 0

    def test_none(self):
        assert safe_int(None) == 0

    def test_whitespace(self):
        assert safe_int("  7  ") == 7

    def test_non_numeric(self):
        assert safe_int("abc") == 0

class TestInsertDenormalized:
    def test_empty_records_returns_zero(self):
        from pymongo import MongoClient
        from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
        client = MongoClient(MONGO_URI)
        col = client[MONGO_DB][MONGO_COLLECTION]
        col.delete_many({})

        result = insert_denormalized_students([])
        assert result == 0
        client.close()

    def test_groups_enrollments_by_student(self):
        records = [
            {"student_id": "S1", "student_name": "Alice", "email": "a@x.com", "phone": "123",
             "department_id": "D1", "department_name": "CS",
             "course_id": "C1", "course_title": "DB", "credit_hours": "3",
             "instructor_id": "I1", "instructor_name": "Dr. X",
             "semester": "Spring-2025", "enroll_date": "2025-01-15", "grade": "A"},
            {"student_id": "S1", "student_name": "Alice", "email": "a@x.com", "phone": "123",
             "department_id": "D1", "department_name": "CS",
             "course_id": "C2", "course_title": "DS", "credit_hours": "3",
             "instructor_id": "I2", "instructor_name": "Dr. Y",
             "semester": "Spring-2025", "enroll_date": "2025-01-15", "grade": "B"},
        ]

        from pymongo import MongoClient
        from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
        client = MongoClient(MONGO_URI)
        col = client[MONGO_DB][MONGO_COLLECTION]
        col.delete_many({})

        result = insert_denormalized_students(records)
        assert result == 1

        doc = col.find_one({"student_id": "S1"})
        assert doc is not None
        assert len(doc["enrollments"]) == 2
        client.close()
