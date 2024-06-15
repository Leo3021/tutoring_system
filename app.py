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
                        grades VARCHAR(255) NOT NULL,
                        rate FLOAT NOT NULL)''')  # 添加 rate 列
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


@app.route('/register_tutor_page')
def register_tutor_page():
    return render_template('register_tutor.html')


@app.route('/register_student_page')
def register_student_page():
    return render_template('register_student.html')

@app.route('/check_tutor', methods=['POST'])
def check_tutor():
    data = request.get_json()
    name = data.get('name')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors WHERE name = %s", (name,))
    tutor = cur.fetchone()
    cur.close()
    if tutor:
        tutor_data = {
            'id': tutor[0],
            'name': tutor[1],
            'subjects': tutor[2],
            'grades': tutor[3],
            'rate': tutor[4]
        }
        return jsonify({'exists': True, 'tutor': tutor_data})
    return jsonify({'exists': False})

# 家教注册，增加检查姓名是否已存在
@app.route('/register_tutor', methods=['POST'])
def register_tutor():
    tutor_data = request.json
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors WHERE name = %s", (tutor_data['name'],))
    existing_tutor = cur.fetchone()
    if existing_tutor:
        cur.close()
        return jsonify({'message': '家教已存在', 'tutor': existing_tutor}), 200
    else:
        # 家教注册逻辑
        tutor_data['subjects'] = tutor_data['subjects'].split('，')
        tutor_data['grades'] = tutor_data['grades'].split('，')
        cur.execute("INSERT INTO tutors (name, subjects, grades, rate) VALUES (%s, %s, %s, %s)",
                    (tutor_data['name'], ','.join(tutor_data['subjects']), ','.join(tutor_data['grades']), tutor_data['rate']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Tutor registered successfully'}), 201

@app.route('/check_student', methods=['POST'])
def check_student():
    data = request.get_json()
    name = data.get('name')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE name = %s", (name,))
    student = cur.fetchone()
    cur.close()
    if student:
        student_data = {
            'id': student[0],
            'name': student[1],
            'grade': student[2],
            'needs': student[3]
        }
        return jsonify({'exists': True, 'student': student_data})
    return jsonify({'exists': False})

# 学生注册，增加检查姓名是否已存在
@app.route('/register_student', methods=['POST'])
def register_student():
    student_data = request.json
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE name = %s", (student_data['name'],))
    existing_student = cur.fetchone()
    if existing_student:
        cur.close()
        return jsonify({'message': '学生已存在', 'student': existing_student}), 200
    else:
        # 学生注册逻辑
        student_data['needs'] = student_data['needs'].split('，')
        cur.execute("INSERT INTO students (name, grade, needs) VALUES (%s, %s, %s)",
                    (student_data['name'], student_data['grade'], ','.join(student_data['needs'])))
        mysql.connection.commit()
        cur.close()
        # 推荐家教逻辑
        recommended_tutors = get_recommended_tutors(student_data['grade'], student_data['needs'])
        return jsonify({'message': 'Student registered successfully', 'recommended_tutors': recommended_tutors})

@app.route('/get_recommended_tutors', methods=['GET'])
def get_recommended_tutors_route():
    needs = request.args.get('needs')
    grade = request.args.get('grade')
    recommended_tutors = get_recommended_tutors(needs, grade)
    return jsonify({'recommended_tutors': recommended_tutors})

@app.route('/deselect_tutor', methods=['POST'])
def deselect_tutor():
    student_id = request.json['student_id']
    tutor_id = request.json['tutor_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matches WHERE student_id = %s AND tutor_id = %s", (student_id, tutor_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': '家教选择已取消'})

def get_recommended_tutors(needs, grade):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors WHERE subjects LIKE %s AND grades LIKE %s", (f'%{needs}%', f'%{grade}%'))
    tutors = cur.fetchall()
    cur.close()
    recommended_tutors = [
        {'id': tutor[0], 'name': tutor[1], 'subjects': tutor[2], 'grades': tutor[3], 'rate': tutor[4]} for tutor in tutors
    ]
    return recommended_tutors


# def get_recommended_tutors(needs, grade):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM tutors WHERE subjects LIKE %s AND grades LIKE %s", (f'%{needs}%', f'%{grade}%'))
#     tutors = cur.fetchall()
#     cur.close()
#     recommended_tutors = [
#         {'id': tutor[0], 'name': tutor[1], 'subjects': tutor[2], 'grades': tutor[3], 'rate': tutor[4]} for tutor in tutors
#     ]
#     return recommended_tutors
# # 推荐家教的函数
# def find_tutors_for_student(student_id, grade, needs):
#     cur = mysql.connection.cursor()
#
#     # 构建 SQL 查询
#     sql = """
#         SELECT id, name, subjects, grades, rate
#         FROM tutors
#         WHERE FIND_IN_SET(%s, grades) > 0 AND (
#     """
#
#     # 添加 subjects 匹配条件
#     sql += ' OR '.join(['FIND_IN_SET(%s, subjects) > 0' for _ in needs])
#     sql += ")"
#
#     # 参数列表，包含 grade 和 needs
#     params = [grade] + needs
#
#     # 执行查询
#     cur.execute(sql, params)
#     tutors = cur.fetchall()
#     cur.close()
#
#     # 格式化返回的家教数据
#     return [
#         {
#             'id': tutor[0],
#             'name': tutor[1],
#             'subjects': tutor[2].split(','),
#             'grades': tutor[3].split(','),
#             'rate': tutor[4]
#         }
#         for tutor in tutors
#     ]


# 学生选择家教
@app.route('/select_tutor', methods=['POST'])
def select_tutor():
    student_id = request.json['student_id']
    tutor_id = request.json['tutor_id']
    cur = mysql.connection.cursor()
    # 检查是否已经匹配
    cur.execute("SELECT * FROM matches WHERE student_id = %s AND tutor_id = %s", (student_id, tutor_id))
    if cur.fetchone():
        cur.close()
        return jsonify({'message': '学生已经选择过该家教'}), 200
    else:
        cur.execute("INSERT INTO matches (student_id, tutor_id) VALUES (%s, %s)", (student_id, tutor_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': '家教选择成功'}), 201


@app.route('/search_tutors', methods=['GET'])
def search_tutors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutors")
    tutors = cur.fetchall()
    cur.close()
    return jsonify({'tutors': [
        {'id': tutor[0], 'name': tutor[1], 'subjects': tutor[2], 'grades': tutor[3], 'rate': tutor[4]} for tutor in
        tutors]})


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
    cur.execute('''SELECT students.name as student_name, tutors.name as tutor_name, tutors.rate as tutor_rate
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

