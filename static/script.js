const form = document.querySelector("#advisor-form");
const recommendedCourses = document.querySelector("#recommended-courses");
const eligibleCourses = document.querySelector("#eligible-courses");
const unavailableCourses = document.querySelector("#unavailable-courses");
const reasoningSteps = document.querySelector("#reasoning-steps");
const creditTotal = document.querySelector("#credit-total");

function checkedValues(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`)).map((input) => input.value);
}

function courseCard(course, extra = "") {
    return `
        <div class="course-card">
            <strong>${course.code} - ${course.name}</strong>
            <div class="muted">${extra}</div>
            <div class="badges">
                ${course.credits ? `<span class="badge">${course.credits} credits</span>` : ""}
                ${course.category ? `<span class="badge">${course.category}</span>` : ""}
            </div>
        </div>
    `;
}

function recommendedCourseCard(course) {
    const explanationItems = course.explanation_items || [course.explanation];

    return `
        <div class="course-card">
            <strong>${course.code} - ${course.name}</strong>
            <div class="score-line">Recommendation score: ${course.score}/100</div>
            <details class="explanation-toggle">
                <summary>View recommendation reason</summary>
                <ul>
                    ${explanationItems.map((item) => `<li>${item}</li>`).join("")}
                </ul>
            </details>
            <div class="badges">
                ${course.credits ? `<span class="badge">${course.credits} credits</span>` : ""}
                ${course.category ? `<span class="badge">${course.category}</span>` : ""}
            </div>
        </div>
    `;
}

function renderList(element, items, renderItem, emptyText) {
    element.innerHTML = items.length ? items.map(renderItem).join("") : `<p class="muted">${emptyText}</p>`;
}

// Forward Chaining: Recommend Courses Logic
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: document.querySelector("#student-name").value,
        completed_courses: checkedValues("completed"),
        interests: checkedValues("interest"),
        max_credits: Number(document.querySelector("#max-credits").value),
    };

    const response = await fetch("/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
    });
    const data = await response.json();

    creditTotal.textContent = `Total recommended credits: ${data.total_recommended_credits}`;

    renderList(
        recommendedCourses,
        data.recommended_courses,
        recommendedCourseCard,
        "No recommended courses yet."
    );

    renderList(
        eligibleCourses,
        data.eligible_courses,
        (course) => courseCard(course, "All prerequisites are satisfied."),
        "No eligible courses."
    );

    renderList(
        unavailableCourses,
        data.unavailable_courses,
        (course) => courseCard(course, `Missing prerequisites: ${course.missing_prerequisites.join(", ")}`),
        "No blocked courses."
    );

    reasoningSteps.innerHTML = data.reasoning_steps
        .map((step) => `<li>${step}</li>`)
        .join("");
});

// Backward Chaining: Target Goal Analysis Logic
async function analyzeGoal() {
    const targetCourse = document.querySelector("#target-course").value;
    const resultDiv = document.querySelector("#goal-result");
    const roadmapPath = document.querySelector("#roadmap-path");

    if (!targetCourse) {
        alert("Please select a target course first.");
        return;
    }

    const payload = {
        target_course: targetCourse,
        passed_courses: checkedValues("completed")
    };

    try {
        const response = await fetch("/analyze-goal", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload),
        });
        
        const data = await response.json();

        resultDiv.style.display = "block";
        
        if (data.missing && data.missing.length > 0) {
            // Displays missing prerequisites with an arrow separator
            const pathText = data.missing.join(" → ");
            roadmapPath.innerHTML = `To take <strong>${data.target_course}</strong>, you need to complete: <br><span style="color: #e11d48; font-weight: bold;">${pathText}</span>`;
        } else {
            roadmapPath.innerHTML = `🎉 You have met all prerequisites for <strong>${data.target_course}</strong>!`;
        }
    } catch (error) {
        console.error("Error fetching backward chaining analysis:", error);
        alert("An error occurred while analyzing the goal.");
    }
}