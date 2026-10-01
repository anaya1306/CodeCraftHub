"""
CodeCraftHub Course REST API

This Flask application provides CRUD operations for courses and stores
course data in a local JSON file called courses.json.

Run the application with:

    python app.py
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request


# Create the Flask application
app = Flask(__name__)


# Store courses.json in the same directory as this app.py file
COURSES_FILE = Path(__file__).parent / "courses.json"


# These are the only status values allowed for a course
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}


class StorageError(Exception):
    """
    Custom error used when there is a problem reading or writing
    the courses.json file.
    """

    pass


def ensure_courses_file_exists():
    """
    Create courses.json automatically if it does not already exist.

    The file starts with an empty JSON list because courses will be
    stored as a list of objects.
    """
    if not COURSES_FILE.exists():
        try:
            COURSES_FILE.write_text("[]", encoding="utf-8")
        except OSError as error:
            raise StorageError(
                f"Could not create {COURSES_FILE.name}: {error}"
            ) from error


def read_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries.

    Raises:
        StorageError: If the file cannot be read or contains invalid JSON.
    """
    ensure_courses_file_exists()

    try:
        with COURSES_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)
    except json.JSONDecodeError as error:
        raise StorageError(
            f"{COURSES_FILE.name} contains invalid JSON: {error}"
        ) from error
    except OSError as error:
        raise StorageError(
            f"Could not read {COURSES_FILE.name}: {error}"
        ) from error

    # The top-level JSON value should always be a list
    if not isinstance(courses, list):
        raise StorageError(
            f"{COURSES_FILE.name} must contain a JSON list"
        )

    return courses


def write_courses(courses):
    """
    Write all courses to courses.json.

    A temporary file is used first. Once writing succeeds, it replaces
    the original file. This helps prevent a partially written JSON file
    if the application stops during a write operation.
    """
    try:
        COURSES_FILE.parent.mkdir(parents=True, exist_ok=True)

        file_descriptor, temporary_path = tempfile.mkstemp(
            dir=COURSES_FILE.parent,
            prefix="courses_",
            suffix=".tmp",
        )

        try:
            with os.fdopen(
                file_descriptor,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(courses, file, indent=2)
                file.write("\n")

            # Replace the old file with the newly written file
            os.replace(temporary_path, COURSES_FILE)

        except Exception:
            # Remove the temporary file if something went wrong
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
            raise

    except OSError as error:
        raise StorageError(
            f"Could not write to {COURSES_FILE.name}: {error}"
        ) from error


def get_next_course_id(courses):
    """
    Generate the next numeric course ID.

    The first course receives ID 1. If courses have been deleted,
    this function continues using the highest existing ID plus 1.
    """
    if not courses:
        return 1

    existing_ids = [
        course.get("id", 0)
        for course in courses
        if isinstance(course.get("id", 0), int)
    ]

    return max(existing_ids, default=0) + 1


def validate_course_data(data):
    """
    Validate fields supplied when creating or updating a course.

    Required fields:
        name
        description
        target_date
        status

    Returns:
        None if the data is valid.
        A string containing an error message otherwise.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    required_fields = [
        "name",
        "description",
        "target_date",
        "status",
    ]

    # Check that every required field exists
    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return (
            "Missing required field(s): "
            + ", ".join(missing_fields)
        )

    # Check that name is a non-empty string
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "name must be a non-empty string"

    # Check that description is a non-empty string
    if (
        not isinstance(data["description"], str)
        or not data["description"].strip()
    ):
        return "description must be a non-empty string"

    # Check the date format
    target_date = data["target_date"]

    if not isinstance(target_date, str):
        return "target_date must be a string in YYYY-MM-DD format"

    try:
        parsed_date = datetime.strptime(
            target_date,
            "%Y-%m-%d",
        )

        # This additional check rejects dates such as 2026-02-30.
        # datetime.strptime may otherwise normalize some invalid dates
        # in certain situations.
        if parsed_date.strftime("%Y-%m-%d") != target_date:
            return "target_date must use YYYY-MM-DD format"

    except ValueError:
        return "target_date must use YYYY-MM-DD format"

    # Check that status is one of the allowed values
    if data["status"] not in VALID_STATUSES:
        return (
            "status must be one of: "
            + ", ".join(sorted(VALID_STATUSES))
        )

    return None


def find_course(courses, course_id):
    """
    Find a course by its numeric ID.

    Returns:
        The matching course dictionary, or None if not found.
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


@app.errorhandler(StorageError)
def handle_storage_error(error):
    """
    Return a JSON response when a file read/write error occurs.
    """
    return jsonify({
        "error": str(error)
    }), 500


@app.errorhandler(404)
def handle_not_found(error):
    """
    Return JSON instead of Flask's default HTML 404 response.
    """
    return jsonify({
        "error": "The requested endpoint was not found"
    }), 404


@app.errorhandler(500)
def handle_internal_error(error):
    """
    Return JSON for unexpected server errors.

    The detailed error is not exposed to the client.
    """
    return jsonify({
        "error": "An unexpected server error occurred"
    }), 500


@app.post("/api/courses")
@app.post("/api/courses/")
def create_course():
    """
    Create a new course.

    Endpoint:
        POST /api/courses

    Example request body:
    {
        "name": "Flask Fundamentals",
        "description": "Learn how to build Flask applications.",
        "target_date": "2026-12-31",
        "status": "Not Started"
    }
    """
    data = request.get_json(silent=True)

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    courses = read_courses()

    # Create a new course with automatically generated fields
    course = {
        "id": get_next_course_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now().astimezone().isoformat(),
    }

    courses.append(course)
    write_courses(courses)

    return jsonify(course), 201


@app.get("/api/courses")
@app.get("/api/courses/")
def get_all_courses():
    """
    Return all courses.

    Endpoints:
        GET /api/courses
        GET /api/courses/
    """
    courses = read_courses()

    return jsonify(courses), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """
    Return one course by ID.

    Endpoint:
        GET /api/courses/<course_id>
    """
    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with id {course_id} was not found"
        }), 404

    return jsonify(course), 200


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    """
    Update an existing course.

    The request must include all editable fields:
        name
        description
        target_date
        status

    The id and created_at values cannot be changed.

    Endpoint:
        PUT /api/courses/<course_id>
    """
    data = request.get_json(silent=True)

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with id {course_id} was not found"
        }), 404

    # Update only the editable fields
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    # Do not change the original id or created_at timestamp
    write_courses(courses)

    return jsonify(course), 200


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoint:
        DELETE /api/courses/<course_id>
    """
    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with id {course_id} was not found"
        }), 404

    # Create a new list without the selected course
    remaining_courses = [
        existing_course
        for existing_course in courses
        if existing_course.get("id") != course_id
    ]

    write_courses(remaining_courses)

    return jsonify({
        "message": f"Course with id {course_id} was deleted"
    }), 200


if __name__ == "__main__":
    # debug=True is useful while learning and developing locally.
    # Do not use debug mode in a production deployment.
    app.run(debug=True)

