from engine.prerequisite_checker import (
    get_missing_prerequisites,
    has_completed_prerequisites,
    is_course_completed,
)


def is_category_unlocked(category, completed_courses, courses):
    """
    Hierarchy Logic: Checks if the previous level's courses are all completed.
    Basic -> Core -> Specialized (AI, Systems, Security, etc.)
    """
    def get_all_by_cat(cat_name):
        return [code for code, info in courses.items() if info.get("category") == cat_name]

    if category == "Basic":
        return True
    
    if category == "Core":
        basic_courses = get_all_by_cat("Basic")
        return all(c in completed_courses for c in basic_courses)
    
    # Specialized categories require all Core courses to be finished
    specialized_cats = ["AI", "Systems", "Security", "Software", "Theory"]
    if category in specialized_cats:
        core_courses = get_all_by_cat("Core")
        return all(c in completed_courses for c in core_courses)
    
    return True


def infer_course_eligibility(student, courses):
    """
    Advanced Forward Chaining:
    Infers next-semester courses based on completed courses and hierarchy rules.
    """
    eligible_courses = []
    unavailable_courses = []
    reasoning_steps = []

    passed_facts = sorted(student.completed_courses)
    interest_facts = sorted(student.interests)
    reasoning_steps.append(f"Known facts: Passed({student.name}, course) = {passed_facts or ['None']}")
    reasoning_steps.append(f"Known facts: Interest({student.name}, topic) = {interest_facts or ['None']}")

    for course_code, course_info in courses.items():
        category = course_info.get("category", "General")
        prerequisites = course_info.get("prerequisites", [])

        # 1. Skip if already completed
        if is_course_completed(student, course_code):
            continue

        # 2. Check Hierarchy (Category Unlock)
        if not is_category_unlocked(category, student.completed_courses, courses):
            reasoning_steps.append(f"Inferred: {course_code} is locked because {category} level is not yet accessible.")
            continue

        # 3. Check Prerequisites
        reasoning_steps.append(f"Rule check: CanTake({student.name}, {course_code}) if {prerequisites or ['None']} are passed.")
        
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


def get_missing_roadmap(target_course, passed_courses, courses_db, missing_list=None):
    """
    Backward Chaining Implementation:
    Finds a roadmap of prerequisites needed to reach a specific goal.
    """
    if missing_list is None:
        missing_list = []

    if target_course in passed_courses:
        return missing_list

    course_info = courses_db.get(target_course)
    if not course_info:
        return missing_list

    prereqs = course_info.get("prerequisites", [])

    for p in prereqs:
        if p not in passed_courses:
            # Recursive search to find the root missing prerequisite
            get_missing_roadmap(p, passed_courses, courses_db, missing_list)
            if p not in missing_list:
                missing_list.append(p)

    return missing_list