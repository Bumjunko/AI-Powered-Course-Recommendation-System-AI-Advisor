def get_unlock_value(course_code, courses):
    return sum(1 for course in courses.values() if course_code in course.get("prerequisites", []))


def calculate_score(student, course_code, course_info, courses):
    score = 0
    reasons = []

    priority = course_info.get("priority", 0)
    if priority:
        score += priority
        reasons.append(f"course priority +{priority}")

    if course_info.get("category") in {"Basic", "Core"}:
        score += 8
        reasons.append("required foundation/core course +8")

    matched_interests = sorted(student.interests.intersection(course_info.get("interests", set())))
    if matched_interests:
        interest_points = 5 * len(matched_interests)
        score += interest_points
        reasons.append(f"interest match {matched_interests} +{interest_points}")

    unlock_value = get_unlock_value(course_code, courses)
    if unlock_value:
        unlock_points = 2 * unlock_value
        score += unlock_points
        reasons.append(f"unlocks {unlock_value} future course(s) +{unlock_points}")

    return score, reasons


def recommend_courses(student, courses, eligible_courses):
    ranked_courses = []

    for course_code in eligible_courses:
        if student.has_completed(course_code):
            continue

        course_info = courses[course_code]
        score, reasons = calculate_score(student, course_code, course_info, courses)
        ranked_courses.append({
            "code": course_code,
            "name": course_info["name"],
            "credits": course_info["credits"],
            "category": course_info["category"],
            "level": course_info["level"],
            "raw_score": score,
            "explanation": "; ".join(reasons) if reasons else "eligible course with no extra priority factors",
        })

    ranked_courses.sort(key=lambda item: (-item["raw_score"], item["level"], item["code"]))
    max_score = max((course["raw_score"] for course in ranked_courses), default=0)
    for course in ranked_courses:
        course["score"] = round((course["raw_score"] / max_score) * 100) if max_score else 0
        del course["raw_score"]

    recommended = []
    total_credits = 0
    for course in ranked_courses:
        if total_credits + course["credits"] <= student.max_credits:
            recommended.append(course)
            total_credits += course["credits"]

    return {
        "recommended_courses": recommended,
        "total_recommended_credits": total_credits,
        "ranked_eligible_courses": ranked_courses,
    }
