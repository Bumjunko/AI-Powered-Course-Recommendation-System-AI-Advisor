from flask import Flask, jsonify, render_template, request

from data.courses import COURSES, INTERESTS
from engine.inference_engine import infer_course_eligibility
from engine.planner import plan_semesters
from engine.recommendation_engine import recommend_courses
from models.student import Student


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", courses=COURSES, interests=INTERESTS)


@app.route("/recommend", methods=["POST"])
def recommend():
    payload = request.get_json(silent=True) or {}
    student = Student(
        name=payload.get("name", ""),
        completed_courses=payload.get("completed_courses", []),
        interests=payload.get("interests", []),
        max_credits=payload.get("max_credits", 12),
    )

    inference = infer_course_eligibility(student, COURSES)
    recommendation = recommend_courses(student, COURSES, inference["eligible_courses"])

    eligible_courses = [
        {
            "code": code,
            "name": COURSES[code]["name"],
            "credits": COURSES[code]["credits"],
            "category": COURSES[code]["category"],
        }
        for code in inference["eligible_courses"]
    ]

    return jsonify({
        "student": student.name,
        "eligible_courses": eligible_courses,
        "recommended_courses": recommendation["recommended_courses"],
        "unavailable_courses": inference["unavailable_courses"],
        "total_recommended_credits": recommendation["total_recommended_credits"],
        "reasoning_steps": inference["reasoning_steps"],
        "semester_plan": plan_semesters(student, COURSES, max_semesters=4),
    })


if __name__ == "__main__":
    app.run(debug=True)
