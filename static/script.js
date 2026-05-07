const form = document.querySelector("#advisor-form");
const recommendedCourses = document.querySelector("#recommended-courses");
const eligibleCourses = document.querySelector("#eligible-courses");
const unavailableCourses = document.querySelector("#unavailable-courses");
const reasoningSteps = document.querySelector("#reasoning-steps");
const creditTotal = document.querySelector("#credit-total");
const setupPage = document.querySelector("#setup-page");
const resultsPage = document.querySelector("#results-page");
const editProfileButton = document.querySelector("#edit-profile");
const goalResult = document.querySelector("#goal-result");
const roadmapPath = document.querySelector("#roadmap-path");

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

function showSetupPage() {
    setupPage.classList.remove("hidden");
    resultsPage.classList.add("hidden");
    window.scrollTo({top: 0, behavior: "smooth"});
}

function showResultsPage() {
    setupPage.classList.add("hidden");
    resultsPage.classList.remove("hidden");
    window.scrollTo({top: 0, behavior: "smooth"});
}

function renderRecommendationResults(data) {
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
}

function renderGoalResult(data) {
    if (!data) {
        goalResult.classList.add("hidden");
        roadmapPath.innerHTML = "";
        return;
    }

    goalResult.classList.remove("hidden");

    if (data.missing && data.missing.length > 0) {
        const pathText = data.missing.join(" → ");
        roadmapPath.innerHTML = `To take <strong>${data.target_course}</strong>, complete: <span class="roadmap-path">${pathText}</span>`;
    } else {
        roadmapPath.innerHTML = `All prerequisites are complete for <strong>${data.target_course}</strong>.`;
    }
}

async function analyzeSelectedGoal() {
    const targetCourse = document.querySelector("#target-course").value;

    if (!targetCourse) {
        return null;
    }

    const response = await fetch("/analyze-goal", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            target_course: targetCourse,
            passed_courses: checkedValues("completed"),
        }),
    });

    if (!response.ok) {
        throw new Error("Goal analysis failed.");
    }

    return response.json();
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: document.querySelector("#student-name").value,
        completed_courses: checkedValues("completed"),
        interests: checkedValues("interest"),
        max_credits: Number(document.querySelector("#max-credits").value),
    };

    try {
        const [recommendationResponse, goalData] = await Promise.all([
            fetch("/recommend", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            }),
            analyzeSelectedGoal(),
        ]);

        if (!recommendationResponse.ok) {
            throw new Error("Recommendation request failed.");
        }

        const recommendationData = await recommendationResponse.json();
        renderRecommendationResults(recommendationData);
        renderGoalResult(goalData);
        showResultsPage();
    } catch (error) {
        console.error("Error generating advisor results:", error);
        alert("An error occurred while generating advisor results.");
    }
});

editProfileButton.addEventListener("click", showSetupPage);
