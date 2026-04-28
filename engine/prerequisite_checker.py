def is_course_completed(student, course_code):
    return student.has_completed(course_code)


def get_missing_prerequisites(student, course_code, courses):
    prerequisites = courses[course_code].get("prerequisites", [])
    return [course for course in prerequisites if not is_course_completed(student, course)]


def has_completed_prerequisites(student, course_code, courses):
    return len(get_missing_prerequisites(student, course_code, courses)) == 0
