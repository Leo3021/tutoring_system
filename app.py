from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tutors = []
students = []
reviews = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_tutor', methods=['POST'])
def register_tutor():
    tutor = request.json
    tutor['subjects'] = tutor['subjects'].split('，')
    tutor['grades'] = tutor['grades'].split('，')
    tutors.append(tutor)
    print(tutors)
    return jsonify({'message': 'Tutor registered successfully', 'tutor': tutor})

@app.route('/register_student', methods=['POST'])
def register_student():
    student = request.json
    student['needs'] = student['needs'].split('，')
    students.append(student)
    recommended_tutors = find_tutors_for_student(student)
    return jsonify({'message': 'Student registered successfully', 'student': student, 'recommended_tutors': recommended_tutors})

def find_tutors_for_student(student):
    recommended_tutors = []
    for tutor in tutors:
        if student['grade'] in tutor['grades'] and any(subject in tutor['subjects'] for subject in student['needs']):
            recommended_tutors.append(tutor['name'])
    return recommended_tutors

@app.route('/search_tutors', methods=['GET'])
def search_tutors():
    return jsonify({'tutors': tutors})

@app.route('/search_students', methods=['GET'])
def search_students():
    student_results = []
    for student in students:
        recommended_tutors = find_tutors_for_student(student)
        student['recommended_tutors'] = recommended_tutors
        student_results.append(student)
    return jsonify({'students': student_results})

@app.route('/add_review', methods=['POST'])
def add_review():
    review = request.json
    reviews.append(review)
    return jsonify({'message': 'Review added successfully', 'review': review})

if __name__ == '__main__':
    app.run(debug=True)
