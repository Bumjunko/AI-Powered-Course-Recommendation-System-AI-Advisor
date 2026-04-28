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

function renderList(element, items, renderItem, emptyText) {
    element.innerHTML = items.length ? items.map(renderItem).join("") : `<p class="muted">${emptyText}</p>`;
}

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
        (course) => courseCard(course, course.explanation),
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
