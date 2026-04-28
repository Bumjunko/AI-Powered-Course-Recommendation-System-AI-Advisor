from engine.prerequisite_checker import (
    get_missing_prerequisites,
    has_completed_prerequisites,
    is_course_completed,
)


def infer_course_eligibility(student, courses):
    eligible_courses = []
    unavailable_courses = []
    reasoning_steps = []

    passed_facts = sorted(student.completed_courses)
    interest_facts = sorted(student.interests)
    reasoning_steps.append(f"Known facts: Passed({student.name}, course) = {passed_facts or ['None']}")
    reasoning_steps.append(f"Known facts: Interest({student.name}, topic) = {interest_facts or ['None']}")

    for course_code, course_info in courses.items():
        prerequisites = course_info.get("prerequisites", [])
        reasoning_steps.append(f"Rule check: CanTake({student.name}, {course_code}) if all prerequisites {prerequisites or ['None']} are passed.")

        if is_course_completed(student, course_code):
            reasoning_steps.append(f"Inferred: AlreadyPassed({student.name}, {course_code}); skip recommendation.")
            continue

        if has_completed_prerequisites(student, course_code, courses):
            eligible_courses.append(course_code)
            reasoning_steps.append(f"Inferred: CanTake({student.name}, {course_code}).")
        else:
            missing = get_missing_prerequisites(student, course_code, courses)
            unavailable_courses.append({
                "code": course_code,
                "name": course_info["name"],
                "missing_prerequisites": missing,
            })
            reasoning_steps.append(f"Inferred: CannotTake({student.name}, {course_code}) because missing {missing}.")

    return {
        "eligible_courses": eligible_courses,
        "unavailable_courses": unavailable_courses,
        "reasoning_steps": reasoning_steps,
    }
