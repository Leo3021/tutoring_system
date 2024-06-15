async function checkTutorName() {
    const name = document.getElementById('tutor-name').value;
    if (!name) return;

    const response = await fetch('/check_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });

    const data = await response.json();
    const existingTutorDiv = document.getElementById('existing-tutor-info');

    if (data.exists) {
        existingTutorDiv.innerHTML = `
            <h3>家教信息</h3>
            <p>姓名: ${data.tutor.name}</p>
            <p>擅长科目: ${data.tutor.subjects}</p>
            <p>教授年级: ${data.tutor.grades}</p>
            <p>收费: ${data.tutor.rate}元/小时</p>
        `;
        document.getElementById('register-tutor').style.display = 'none';
    } else {
        existingTutorDiv.innerHTML = '<p>家教不存在，请注册。</p>';
        document.getElementById('register-tutor').style.display = 'block';
    }
}

async function loginTutor() {
    const name = document.getElementById('tutor-name').value;

    const response = await fetch('/check_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });

    const data = await response.json();
    if (data.exists) {
        alert('家教登录成功！');
        displayTutorInfo(data.tutor);
    } else {
        alert('家教不存在，请注册。');
        document.getElementById('register-tutor').style.display = 'block';
    }
}

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
    if (data.message === 'Tutor registered successfully') {
        alert('家教注册成功！');
        document.getElementById('register-tutor').style.display = 'none';
    } else {
        alert('家教已存在，请登录。');
    }
}

function displayTutorInfo(tutor) {
    const tutorInfoDiv = document.getElementById('tutor-info');

    tutorInfoDiv.innerHTML = `
        <h3>家教信息</h3>
        <p>姓名: ${tutor.name}</p>
        <p>擅长科目: ${tutor.subjects}</p>
        <p>教授年级: ${tutor.grades}</p>
        <p>收费: ${tutor.rate}元/小时</p>
    `;
}

async function checkStudentName() {
    const name = document.getElementById('student-name').value;
    if (!name) return;

    const response = await fetch('/check_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });

    const data = await response.json();
    const existingStudentDiv = document.getElementById('existing-student-info');

    if (data.exists) {
        existingStudentDiv.innerHTML = `
            <h3>学生信息</h3>
            <p>姓名: ${data.student.name}</p>
            <p>需求科目: ${data.student.needs}</p>
            <p>年级: ${data.student.grade}</p>
        `;
        document.getElementById('register-student').style.display = 'none';
        displayRecommendedTutors(data.student.needs, data.student.grade);
    } else {
        existingStudentDiv.innerHTML = '<p>学生不存在，请注册。</p>';
        document.getElementById('register-student').style.display = 'block';
    }
}

async function loginStudent() {
    const name = document.getElementById('student-name').value;

    const response = await fetch('/check_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });

    const data = await response.json();
    if (data.exists) {
        alert('学生登录成功！');
        displayStudentInfo(data.student);
    } else {
        alert('学生不存在，请注册。');
        document.getElementById('register-student').style.display = 'block';
    }
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
    if (data.message === 'Student registered successfully') {
        alert('学生注册成功！');
        document.getElementById('register-student').style.display = 'none';
        displayRecommendedTutors(needs, grade);
    } else {
        alert(data.message);
    }
}

async function displayRecommendedTutors(needs, grade, studentId) {
    const response = await fetch(`/get_recommended_tutors?needs=${encodeURIComponent(needs)}&grade=${encodeURIComponent(grade)}`);
    const data = await response.json();
    const resultsDiv = document.getElementById('results');

    if (data.recommended_tutors.length > 0) {
        let tutorsHtml = '<h3>推荐的家教</h3>';
        data.recommended_tutors.forEach(tutor => {
            tutorsHtml += `
                <div>
                    <p>姓名: ${tutor.name}</p>
                    <p>擅长科目: ${tutor.subjects}</p>
                    <p>教授年级: ${tutor.grades}</p>
                    <p>收费: ${tutor.rate}元/小时</p>
                    <button onclick="selectTutor(${studentId}, ${tutor.id})">选择</button>
                    <button onclick="deselectTutor(${studentId}, ${tutor.id})">删除</button>
                </div>
            `;
        });
        resultsDiv.innerHTML = tutorsHtml;
    } else {
        resultsDiv.innerHTML = '<p>没有找到符合条件的家教。</p>';
    }
}

async function selectTutor(studentId, tutorId) {
    const response = await fetch('/select_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ student_id: studentId, tutor_id: tutorId })
    });

    const data = await response.json();
    alert(data.message);
}

async function deselectTutor(studentId, tutorId) {
    const response = await fetch('/deselect_tutor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ student_id: studentId, tutor_id: tutorId })
    });

    const data = await response.json();
    alert(data.message);
}


// 显示学生信息
function displayStudentInfo(student) {
    const existingStudentDiv = document.getElementById('existing-student-info');
    existingStudentDiv.innerHTML = `
        <h3>学生信息</h3>
        <p>姓名: ${student.name}</p>
        <p>需求科目: ${student.needs}</p>
        <p>年级: ${student.grade}</p>
    `;
}

//// 显示推荐的家教并允许选择
//function displayRecommendedTutors(recommendedTutors) {
//    const resultsDiv = document.getElementById('results');
//    resultsDiv.innerHTML = ''; // 清空之前的内容
//    if (recommendedTutors.length === 0) {
//        resultsDiv.innerHTML = '<p>没有找到推荐的家教。</p>';
//        return;
//    }
//    const tutorsHTML = recommendedTutors.map(tutor => `
//        <div class="tutor-option">
//            <h4>${tutor.name} - 收费: ${tutor.rate}元/小时</h4>
//            <p>教授科目: ${tutor.subjects.join(', ')}</p>
//            <p>教授年级: ${tutor.grades.join(', ')}</p>
//            <button onclick="selectTutor(${tutor.id})">选择这个家教</button>
//        </div>
//    `).join('');
//    resultsDiv.innerHTML = `<h3>推荐的家教:</h3>${tutorsHTML}`;
//}

//// 学生选择家教的函数
//function selectTutor(tutorId) {
//    fetch('/select_tutor', {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json'
//        },
//        body: JSON.stringify({ tutor_id: tutorId }) // 假设前端已经知道 student_id
//    })
//    .then(response => response.json())
//    .then(data => {
//        alert(data.message);
//    })
//    .catch(error => console.error('Error:', error));
//}

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
