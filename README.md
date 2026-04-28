# AI Computer Science Advisor

This project is a knowledge-based, rule-based AI advisor for Computer Science course planning. It recommends next-semester courses from a hard-coded curriculum knowledge base using completed courses, interests, prerequisite rules, and a maximum credit limit.

No machine learning model, external AI API, or database is required.

## AI Concepts Demonstrated

- Goal-based AI: recommends a schedule that helps the student progress through the curriculum.
- Knowledge base: course facts are stored in `data/courses.py`.
- State and state space: a student's completed courses represent the current state.
- Propositional logic: eligibility is checked with boolean prerequisite conditions.
- Predicate logic: the code models ideas such as `Passed(student, course)`, `Prereq(course1, course2)`, `CanTake(student, course)`, and `Recommend(student, course)`.
- Forward-chaining inference: known facts are used to infer eligible and unavailable courses.
- Search: `engine/planner.py` creates a simple multi-semester plan by repeatedly selecting eligible courses.

## Folder Structure

```text
.
├── app.py
├── data/
│   └── courses.py
├── models/
│   └── student.py
├── engine/
│   ├── prerequisite_checker.py
│   ├── inference_engine.py
│   ├── recommendation_engine.py
│   └── planner.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_advisor.py
├── prototype20260420.py
└── README.md
```

## How to Run

Install dependencies:

```bash
pip install flask pytest
```

Start the web app:

```bash
python app.py
```

Open the local Flask URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

Run tests:

```bash
pytest
```

## Example Input

```json
{
  "name": "Alex",
  "completed_courses": ["CS 1336", "CS 1337", "CS 2336"],
  "interests": ["ai", "software"],
  "max_credits": 6
}
```

## Example Output

```json
{
  "eligible_courses": ["CS 3304", "CS 3310", "CS 4312", "CS 4318"],
  "recommended_courses": [
    {
      "code": "CS 3304",
      "name": "Programming Languages",
      "credits": 3,
      "score": 18,
      "explanation": "course priority +8; required foundation/core course +8; unlocks 1 future course(s) +2"
    }
  ],
  "total_recommended_credits": 6
}
```

## Limitations

- The curriculum data is simplified and hard-coded.
- Course availability by semester is not fully modeled.
- The planner is greedy and does not guarantee an optimal graduation path.
- Recommendation scores are rule-based and manually weighted.
