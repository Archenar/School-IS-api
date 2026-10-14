"""Behaviour checks; all writes use temporary copies of the fictional data."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import main
import storage
from domain import Course, Student
from registration_demo import register
from tutorial import app as tutorial_app


class SchoolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        shutil.copytree(Path(__file__).resolve().parents[1] / "data", self.data)
        self.patch = patch.object(storage, "DATA_DIR", self.data)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.client = TestClient(main.app)
        self.addCleanup(self.client.close)

    def snapshot(self):
        return {p.name: p.read_bytes() for p in self.data.glob("*.json")}

    def test_list_and_known_records(self):
        before = self.snapshot()
        for path, expected in [("/students", 2), ("/courses", 2), ("/enrolments", 3)]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), expected)
        self.assertEqual(self.client.get("/students/1002").json(),
                         {"student_id": 1002, "name": "Noah"})
        self.assertEqual(self.client.get("/courses/IS101").json()["title"],
                         "Information Systems")
        self.assertEqual(self.client.get("/enrolments/1001/IS101").json(),
                         {"student_id": 1001, "course_id": "IS101", "grade": None})
        self.assertEqual(before, self.snapshot(), "GET must not change stored data")

    def test_absent_and_invalid_ids_are_different(self):
        for path in ["/students/9999", "/courses/UNKNOWN", "/enrolments/1002/DB101"]:
            self.assertEqual(self.client.get(path).status_code, 404)
        self.assertEqual(self.client.get("/students/abc").status_code, 422)
        self.assertEqual(self.client.get("/enrolments/abc/IS101").status_code, 422)
        self.assertEqual(self.client.post("/students", json={}).status_code, 405)

    def test_relationship_references_and_pair_uniqueness(self):
        students = {r["student_id"] for r in storage.load_records("students.json")}
        courses = {r["course_id"] for r in storage.load_records("courses.json")}
        records = storage.load_records("enrolments.json")
        self.assertEqual(len(students), 2)
        self.assertEqual(len(courses), 2)
        self.assertEqual(len({(r["student_id"], r["course_id"]) for r in records}), len(records))
        for r in records:
            self.assertIn(r["student_id"], students)
            self.assertIn(r["course_id"], courses)

    def test_file_edit_visible_on_next_request(self):
        records = storage.load_records("students.json")
        records[1]["name"] = "Noah Keller"
        storage.save_records("students.json", records)
        self.assertEqual(self.client.get("/students/1002").json()["name"], "Noah Keller")

    def test_objects_do_not_implicitly_save(self):
        before = self.snapshot()
        enrolment = Student(1002, "Noah").enrol(Course("DB101", "Databases"))
        self.assertEqual(enrolment.to_record(),
                         {"student_id": 1002, "course_id": "DB101", "grade": None})
        self.assertEqual(before, self.snapshot())

    def test_registration_persists_once_and_api_can_read_it(self):
        record = register(1002, "DB101")
        response = self.client.get("/enrolments/1002/DB101")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), record)
        self.assertEqual(len(storage.load_records("enrolments.json")), 4)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "already enrolled"):
            register(1002, "DB101")
        self.assertEqual(before, self.snapshot())

    def test_unknown_references_never_write(self):
        before = self.snapshot()
        for student, course in [(9999, "DB101"), (1002, "UNKNOWN")]:
            with self.assertRaisesRegex(ValueError, "must exist"):
                register(student, course)
        self.assertEqual(before, self.snapshot())

    def test_openapi_and_documentation(self):
        self.assertEqual(self.client.get("/docs").status_code, 200)
        schema = self.client.get("/openapi.json").json()
        params = schema["paths"]["/enrolments/{student_id}/{course_id}"]["get"]["parameters"]
        self.assertEqual({p["name"]:p["schema"]["type"] for p in params},
                         {"student_id": "integer", "course_id": "string"})

    def test_tutorial_echo_is_distinct_from_lookup(self):
        with TestClient(tutorial_app) as client:
            self.assertEqual(client.get("/students/9999").json(), {"requested_student_id": 9999})
            self.assertEqual(client.get("/students/abc").status_code, 422)
        self.assertEqual(self.client.get("/students/9999").status_code, 404)

    def test_bad_data_is_not_silently_an_empty_school(self):
        (self.data / "students.json").write_text("not JSON", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            storage.load_records("students.json")
        (self.data / "students.json").unlink()
        with self.assertRaises(FileNotFoundError):
            storage.load_records("students.json")


if __name__ == "__main__":
    unittest.main()
