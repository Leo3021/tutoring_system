async function registerTutor() {
    const name = document.getElementById('tutor-name').value;
    const subjects = document.getElementById('tutor-subjects').value;
    const grades = document.getElementById('tutor-grades').value;
    const response = await fetch('/register_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, subjects, grades })
    });
    const data = await response.json();
    alert(data.message);
}

async function registerStudent() {
    const name = document.getElementById('student-name').value;
    const needs = document.getElementById('student-needs').value;
    const grade = document.getElementById('student-grade').value;
    const response = await fetch('/register_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, needs, grade })
    });
    const data = await response.json();
    alert(data.message);
    displayRecommendedTutors(data.recommended_tutors);
}

function displayRecommendedTutors(recommendedTutors) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h3>推荐的家教:</h3>';
    recommendedTutors.forEach(tutor => {
        resultsDiv.innerHTML += `<p>${tutor}</p>`;
    });
}


async function searchTutors() {
    const response = await fetch('/search_tutors');
    const data = await response.json();
    displayResults(data.tutors);
}

async function searchStudents() {
    const response = await fetch('/search_students');
    const data = await response.json();
    displayResults(data.students);
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = JSON.stringify(results, null, 2);
}
