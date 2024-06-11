async function registerTutor() {
    const name = document.getElementById('tutor-name').value;
    const subjects = document.getElementById('tutor-subjects').value;
    const grades = document.getElementById('tutor-grades').value;
    const rate = document.getElementById('tutor-rate').value;
    const response = await fetch('/register_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, subjects, grades, rate })
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
    if(data.message === 'Student registered successfully') {
        alert('学生注册成功！');
        displayRecommendedTutors(data.recommended_tutors);
    } else {
        alert(data.message);
    }
}

// 显示推荐的家教并允许选择
function displayRecommendedTutors(recommendedTutors) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // 清空之前的内容
    if(recommendedTutors.length === 0) {
        resultsDiv.innerHTML = '<p>没有找到推荐的家教。</p>';
        return;
    }
    const tutorsHTML = recommendedTutors.map(tutor => `
        <div class="tutor-option">
            <h4>${tutor.name} - 收费: ${tutor.rate}元/小时</h4>
            <p>教授科目: ${tutor.subjects.join(', ')}</p>
            <p>教授年级: ${tutor.grades.join(', ')}</p>
            <button onclick="selectTutor(${tutor.id})">选择这个家教</button>
        </div>
    `).join('');
    resultsDiv.innerHTML = `<h3>推荐的家教:</h3>${tutorsHTML}`;
}

// 学生选择家教的函数
function selectTutor(tutorId) {
    fetch('/select_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tutor_id: tutorId }) // 假设前端已经知道 student_id
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
}

// 管理员查看信息的函数（根据需要实现）
async function adminViewTutors() {
    const response = await fetch('/admin_view_tutors');
    const data = await response.json();
    console.log(data.tutors); // 这里仅为示例，您可以根据需要进行展示
}

async function adminViewStudents() {
    const response = await fetch('/admin_view_students');
    const data = await response.json();
    console.log(data.students); // 这里仅为示例，您可以根据需要进行展示
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
