from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

# MySQL 配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'tutor_system'

# 初始化 MySQL
mysql = MySQL(app)

# 创建数据库
def create_database():
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456')
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tutor_system")
    cursor.close()
    db.close()

# 创建数据表
def create_tables():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS tutors (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        subjects VARCHAR(255) NOT NULL,
                        grades VARCHAR(255) NOT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        grade VARCHAR(255) NOT NULL,
                        needs VARCHAR(255) NOT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        review_text TEXT NOT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS matches (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT NOT NULL,
                        tutor_id INT NOT NULL,
                        FOREIGN KEY (student_id) REFERENCES students(id),
                        FOREIGN KEY (tutor_id) REFERENCES tutors(id))''')
        cur.close()
        mysql.connection.commit()

create_database()
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_tutor', methods=['POST'])
def register_tutor():
    tutor = request.json
    tutor['subjects'] = tutor['subjects'].split('，')
    tutor['grades'] = tutor['grades'].split('，')
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tutors (name, subjects, grades) VALUES (%s, %s, %s)", (tutor['name'], ','.join(tutor['subjects']), ','.join(tutor['grades'])))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Tutor registered successfully', 'tutor': tutor})

@app.route('/register_student', methods=['POST'])
def register_student():
    student = request.json
    # student['needs'] = student['needs'].split('，')
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, grade, needs) VALUES (%s, %s, %s)", (student['name'], student['grade'], ','.join(student['needs'])))
    student_id = cur.lastrowid  # 获取新插入的学生的ID
    mysql.connection.commit()
    
    recommended_tutors = find_tutors_for_student(student)
    
    # 将匹配信息保存到 matches 表中
    for tutor_id in recommended_tutors['tutor_ids']:
        cur.execute("INSERT INTO matches (student_id, tutor_id) VALUES (%s, %s)", (student_id, tutor_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Student registered successfully', 'student': student, 'recommended_tutors': recommended_tutors['tutors']})

def find_tutors_for_student(student):
    recommended_tutors = {'tutors': [], 'tutor_ids': []}
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors")
    tutors = cur.fetchall()
    cur.close()
    for tutor in tutors:
        tutor_id, name, subjects, grades = tutor
        subjects = subjects.split(',')
        grades = grades.split(',')
        print(subjects)
        matching_subjects = [subject for subject in subjects if subject in student['needs']]
        if student['grade'] in grades and matching_subjects:
            recommended_tutors['tutors'].append({'name': name, 'subjects': matching_subjects})
            recommended_tutors['tutor_ids'].append(tutor_id)
    print(recommended_tutors)
    return recommended_tutors


@app.route('/search_tutors', methods=['GET'])
def search_tutors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors")
    tutors = cur.fetchall()
    cur.close()
    return jsonify({'tutors': tutors})

@app.route('/search_students', methods=['GET'])
def search_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return jsonify({'students': students})

@app.route('/search_matches', methods=['GET'])
def search_matches():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT students.name as student_name, tutors.name as tutor_name
                   FROM matches
                   JOIN students ON matches.student_id = students.id
                   JOIN tutors ON matches.tutor_id = tutors.id''')
    matches = cur.fetchall()
    cur.close()
    return render_template('matches.html', matches=matches)

@app.route('/add_review', methods=['POST'])
def add_review():
    review = request.json['review']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO reviews (review_text) VALUES (%s)", (review,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Review added successfully', 'review': review})

if __name__ == '__main__':
    app.run(debug=True)


 



