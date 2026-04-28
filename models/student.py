class Student:
    def __init__(self, name, completed_courses=None, interests=None, max_credits=12):
        self.name = name.strip() if name else "Student"
        self.completed_courses = set(completed_courses or [])
        self.interests = {interest.lower() for interest in (interests or [])}
        self.max_credits = int(max_credits or 12)

    def has_completed(self, course_code):
        return course_code in self.completed_courses
