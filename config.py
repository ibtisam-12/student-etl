import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "enrollment_db")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "students")

SQL_DRIVER = os.environ.get("SQL_DRIVER", "ODBC Driver 17 for SQL Server")
SQL_SERVER = os.environ.get("SQL_SERVER", "localhost")
SQL_DATABASE = os.environ.get("SQL_DATABASE", "EnrollmentDB")
SQL_TRUSTED_CONNECTION = os.environ.get("SQL_TRUSTED_CONNECTION", "yes")
