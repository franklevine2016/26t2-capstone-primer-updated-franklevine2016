from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "Fail to fetch students"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body, optional)
    return: The created student if successful
    """
    try:
        student_data = request.get_json()
        if not student_data:
            return jsonify({"error": "Missing JSON payload"}), 404

        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        if not name or not course:
            return jsonify({"error": "name and course required"}), 404

        if mark is not None:
            try:
                mark = int(mark)
            except ValueError:
                return jsonify({"error": "mark must be integer number"}), 404

        new_student = db.insert_student(name, course, mark)
        return jsonify(new_student), 200
    except Exception as err:
        print("POST error:", err)
        return jsonify({"error": "Fail to create student"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        data = request.get_json()
        name = data.get("name")
        course = data.get("course")
        mark = data.get("mark")

        if mark is not None:
            try:
                mark = int(mark)
            except ValueError:
                return jsonify({"error": "mark must be integer number"}), 404

        updated = db.update_student(student_id, name, course, mark)
        
        if updated is None:
            return jsonify({"error": "Student not found"}), 404
        
        return jsonify(updated), 200
    except Exception as err:
        print("PUT error:", err)
        return jsonify({"error": "Failed to update student"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        result = db.delete_student(student_id)
        if result is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(result), 200
    except Exception as err:
        print("DELETE error:", err)
        return jsonify({"error": "Failed to delete student"}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [s["mark"] for s in students if s["mark"] is not None]
        count = len(marks)

        if count == 0:
            average = 0
            min_mark = 0
            max_mark = 0
        else:
            average = sum(marks) / count
            min_mark = min(marks)
            max_mark = max(marks)

        stats_data = {
            "count": count,
            "average": average,
            "min": min_mark,
            "max": max_mark
        }
        return jsonify(stats_data), 200
    except Exception as err:
        print("STATS error:", err)
        return jsonify({"error": "Failed to get stats"}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)