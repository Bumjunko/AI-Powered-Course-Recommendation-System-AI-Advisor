from data.courses import COURSES
from engine.inference_engine import infer_course_eligibility
from engine.prerequisite_checker import get_missing_prerequisites, has_completed_prerequisites
from engine.recommendation_engine import calculate_score, recommend_courses
from models.student import Student


def test_missing_prerequisites_are_reported():
    student = Student("Alex", completed_courses=["CS 1336"])

    missing = get_missing_prerequisites(student, "CS 2336", COURSES)

    assert missing == ["CS 1337"]


def test_completed_prerequisite_allows_next_course():
    student = Student("Alex", completed_courses=["CS 1336"])

    assert has_completed_prerequisites(student, "CS 1337", COURSES)


def test_inference_marks_unavailable_courses():
    student = Student("Alex", completed_courses=[])

    inference = infer_course_eligibility(student, COURSES)
    blocked_codes = {course["code"] for course in inference["unavailable_courses"]}

    assert "CS 1336" in inference["eligible_courses"]
    assert "CS 1337" in blocked_codes


def test_interest_match_increases_score():
    interested_student = Student("Alex", completed_courses=["CS 1336", "CS 1337", "CS 2336"], interests=["web"])
    neutral_student = Student("Blair", completed_courses=["CS 1336", "CS 1337", "CS 2336"], interests=[])

    interested_score, _ = calculate_score(interested_student, "CS 4312", COURSES["CS 4312"], COURSES)
    neutral_score, _ = calculate_score(neutral_student, "CS 4312", COURSES["CS 4312"], COURSES)

    assert interested_score > neutral_score


def test_recommendations_respect_credit_limit():
    student = Student(
        "Alex",
        completed_courses=["CS 1336", "CS 1337", "CS 2336"],
        interests=["ai", "software"],
        max_credits=6,
    )
    inference = infer_course_eligibility(student, COURSES)

    recommendation = recommend_courses(student, COURSES, inference["eligible_courses"])

    assert recommendation["total_recommended_credits"] <= 6


def test_recommendations_do_not_include_completed_courses():
    student = Student("Alex", completed_courses=["CS 1336"], max_credits=12)
    inference = infer_course_eligibility(student, COURSES)

    recommendation = recommend_courses(student, COURSES, inference["eligible_courses"])
    recommended_codes = {course["code"] for course in recommendation["recommended_courses"]}

    assert "CS 1336" not in recommended_codes
