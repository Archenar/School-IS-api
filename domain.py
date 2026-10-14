"""A small implementation of the UML classes. See docs/04-models-and-objects.md.
These ordinary Python classes do not depend on FastAPI.
"""


class Course:
    def __init__(self, course_id: str, title: str):
        self.course_id = course_id
        self.title = title


class Student:
    def __init__(self, student_id: int, name: str):
        # self refers to this particular student object.
        self.student_id = student_id
        self.name = name

    def enrol(self, course: Course):
        """Create the relationship; the caller checks duplicates and saves it."""
        return Enrolment(self.student_id, course.course_id)


class Enrolment:
    def __init__(self, student_id: int, course_id: str, grade: float | None = None):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def to_record(self):
        # A method is behaviour; it is not stored as a JSON field.
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "grade": self.grade,
        }
