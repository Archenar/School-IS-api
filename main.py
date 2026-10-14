"""Start with: python run.py
Reading guide: docs/03-trace-a-request.md. All records are fictional.
"""

# 1. Imports and setup: FastAPI connects HTTP requests to Python functions.
from fastapi import FastAPI, HTTPException
from storage import load_records

app = FastAPI(title="School IS API", description="Student / Course / Enrolment")


@app.get("/")
def welcome():
    return {"message": "School IS API", "documentation": "/docs"}


# 2. Read all: a Python list becomes a JSON array in the HTTP response.
@app.get("/students")
def list_students():
    return load_records("students.json")


# 3. Read one: URL input -> load -> find -> return, or report not found.
@app.get("/students/{student_id}")
def get_student(student_id: int):
    # int lets FastAPI check/convert this URL parameter before calling us.
    students = load_records("students.json")
    for student in students:
        if student["student_id"] == student_id:
            return student
    # Outside the loop: only report absence after inspecting all records.
    raise HTTPException(status_code=404, detail="Student not found")


# The same read pattern, applied to the other concepts from our UML model.
@app.get("/courses")
def list_courses():
    return load_records("courses.json")


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    for course in load_records("courses.json"):
        if course["course_id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")


@app.get("/enrolments")
def list_enrolments():
    return load_records("enrolments.json")


# 4. Relationships: both IDs identify an enrolment in this small model.
@app.get("/enrolments/{student_id}/{course_id}")
def get_enrolment(student_id: int, course_id: str):
    for enrolment in load_records("enrolments.json"):
        if (enrolment["student_id"] == student_id
                and enrolment["course_id"] == course_id):
            return enrolment
    raise HTTPException(status_code=404, detail="Enrolment not found")

# Try /students/1002, /students/9999 and /students/abc in /docs.
# Then trace /enrolments/1001/IS101 to the two linked records.
# This first API reads data. The optional registration_demo.py writes one record.
