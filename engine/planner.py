from models.student import Student
from engine.inference_engine import infer_course_eligibility
from engine.recommendation_engine import recommend_courses


def plan_semesters(student, courses, max_semesters=4):
    state = set(student.completed_courses)
    plan = []

    for semester_number in range(1, max_semesters + 1):
        current_student = Student(
            name=student.name,
            completed_courses=state,
            interests=student.interests,
            max_credits=student.max_credits,
        )
        inference = infer_course_eligibility(current_student, courses)
        recommendation = recommend_courses(current_student, courses, inference["eligible_courses"])
        semester_courses = recommendation["recommended_courses"]

        if not semester_courses:
            break

        plan.append({
            "semester": semester_number,
            "courses": semester_courses,
            "credits": recommendation["total_recommended_credits"],
        })
        state.update(course["code"] for course in semester_courses)

        if len(state) == len(courses):
            break

    return plan
