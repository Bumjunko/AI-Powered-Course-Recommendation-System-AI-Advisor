import re

# Knowledge Base
# Standardized key format: "DEPT ####" (e.g., "CS 1336")
courses_db = {
    "CS 1336": {"name": "Computer Science I", "prereq": [], "category": "Basic"},
    "CS 1337": {"name": "Computer Science II", "prereq": ["CS 1336"], "category": "Basic"},
    "CS 2336": {"name": "Data Structures", "prereq": ["CS 1337"], "category": "Core"},
    "CS 3304": {"name": "Programming Languages", "prereq": ["CS 2336"], "category": "Core"},
    "CS 3310": {"name": "Computer Architecture", "prereq": ["CS 1337"], "category": "Systems"},
    "CS 3311": {"name": "Operating Systems", "prereq": ["CS 2336", "CS 3310"], "category": "Systems"},
    "CS 4301": {"name": "Distributed Systems", "prereq": ["CS 3311"], "category": "Systems"},
    "CS 4306": {"name": "Artificial Intelligence", "prereq": ["CS 2336", "CS 3304"], "category": "AI"},
    "CS 4308": {"name": "Machine Learning", "prereq": ["CS 4306"], "category": "AI"},
    "CS 4310": {"name": "Advanced Architecture", "prereq": ["CS 3310"], "category": "Systems"},
    "CS 4312": {"name": "Web Applications", "prereq": ["CS 2336"], "category": "Software"},
    "CS 4314": {"name": "Cybersecurity", "prereq": ["CS 3311"], "category": "Security"},
    "CS 4318": {"name": "Data Mining", "prereq": ["CS 2336"], "category": "AI"},
    "CS 4320": {"name": "Networks", "prereq": ["CS 3311"], "category": "Security"}
}

def is_category_unlocked(category, user_passed):
    """
    Checks if the hierarchy level is met for a specific category.
    """
    # Define the hierarchy rules
    if category == "Basic":
        return True  # Basic is always unlocked
    
    # Get all courses belonging to a specific category
    def get_courses_by_cat(cat_name):
        return [code for code, info in courses_db.items() if info["category"] == cat_name]

    if category == "Core":
        # Unlock Core only if ALL Basic courses are passed
        basic_courses = get_courses_by_cat("Basic")
        return all(c in user_passed for c in basic_courses)
    
    # Unlock rest (AI, Systems, Security, etc.) only if ALL Core courses are passed
    if category in ["AI", "Systems", "Security", "Software", "Theory"]:
        core_courses = get_courses_by_cat("Core")
        return all(c in user_passed for c in core_courses)
    
    return True

def can_enroll(course_code, passed_courses):
    """
    Logic: Checks if all prerequisites for a specific course are met.
    Predicate Logic: ∀p (Prereq(p, course) → Passed(s, p))
    """
    prereqs = courses_db[course_code]["prereq"]
    return all(p in passed_courses for p in prereqs)

def ai_advisor_inference(user_passed, user_interest):
    """
    Forward Chaining: Derives recommended courses based on facts (passed courses).
    """
    available_courses = []
    
    for code, info in courses_db.items():
        if code in user_passed:
            continue
            
        if can_enroll(code, user_passed):
            priority = 1 if info["category"].lower() == user_interest.lower() else 0
            available_courses.append({
                "code": code,
                "name": info["name"],
                "category": info["category"],
                "priority": priority
            })
            
    return sorted(available_courses, key=lambda x: x['priority'], reverse=True)

def preprocess_input(raw_input):
    """
    Standardizes user input to match the Database keys (e.g., "cs1336" -> "CS 1336").
    Ensures input includes both Department and Number.
    """
    import re
    # Find all occurrences of "LetterPart+NumberPart"
    # Example: "CS1336", "cs 1337", "Math 1314"
    pattern = re.compile(r'([a-zA-Z]+)\s*(\d+)')
    matches = pattern.findall(raw_input)
    
    standardized = []
    for dept, num in matches:
        # Standardize to "DEPT ####" format (e.g., CS 1336)
        standardized.append(f"{dept.upper()} {num}")
    
    return standardized

def main():
    print("==========================================")
    print("   ASU CS Course Advisor (AI System)    ")
    print("==========================================\n")
    
    print("[GUIDE] To get accurate results, please follow the formats below:")
    print("- Interests: AI, Systems, Security, Basic, Theory, Software")
    print("- Passed Courses: Use 'CS ####' format (e.g., CS 1336, CS 1337)")

    # 1. User Interest Input
    print("01. Enter your interest (e.g., AI, Systems, Security, Basic, Theory, Software. If none, just press Enter)")
    user_interest = input(">> ").strip()

    # 2. Completed Courses Input
    print("\n02. Enter completed course codes")
    print("Example: CS 1336, CS 1337, CS 2336")
    print("Format must include both Letters and Numbers.")
    print("(Press Enter if you haven't taken any courses yet)")
    raw_user_input = input(">> ").strip()
    
    #preprocess user input into a standardized list
    my_passed = preprocess_input(raw_user_input)

    # 3. AI engine inference
    results = ai_advisor_inference(my_passed, user_interest)

    # 4.final Output
    print(f"\n[Advising Results]")
    print(f"- Verified Passed Courses: {', '.join(my_passed) if my_passed else 'None'}")
    print(f"- User Interest: {user_interest}")
    print("\n--- Recommended Course List ---")
    
    if not results:
        print("No recommendations available. Please check your prerequisites.")
    else:
        for item in results:
            recommendation_tag = "★ [High Priority]" if item["priority"] == 1 else "  "
            print(f"{recommendation_tag} {item['code']} - {item['name']} ({item['category']})")

    print("\n==========================================")

if __name__ == "__main__":
    main()