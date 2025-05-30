import os
import csv
import datetime
from io import StringIO
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.utils import secure_filename

# Import models
from model.user import authenticate_user, register_user, is_admin
from model.student import get_all_students, get_student_by_id, create_student, update_student, delete_student
from model.course import get_all_courses, get_course_by_id, create_course, update_course, delete_course
from model.grade import (get_grades_by_student, get_grades_by_course, add_grade, update_grade,
                         delete_grade, delete_student_grades, get_student_average, import_grades_from_csv)
from database.db_config import execute_query

app = Flask(__name__)
app.secret_key = 'student_management_system_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录', 'error')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('此功能需要管理员权限', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            error = '用户名和密码不能为空'
        else:
            user = authenticate_user(username, password)
            if user:
                session['username'] = user['username']
                session['is_admin'] = user['is_admin']
                flash(f'欢迎回来，{username}！', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = '用户名或密码错误'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            error = '用户名和密码不能为空'
        elif password != confirm_password:
            error = '两次输入的密码不一致'
        else:
            success, message = register_user(username, password)
            if success:
                flash('注册成功，请登录', 'success')
                return redirect(url_for('login'))
            else:
                error = message
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get dashboard statistics
    student_count_result = execute_query("SELECT COUNT(*) as count FROM students")
    course_count_result = execute_query("SELECT COUNT(*) as count FROM courses")
    grade_count_result = execute_query("SELECT COUNT(*) as count FROM grades")
    avg_grade_result = execute_query("SELECT AVG(score) as avg FROM grades")
    
    student_count = student_count_result[0]['count'] if student_count_result else 0
    course_count = course_count_result[0]['count'] if course_count_result else 0
    grade_count = grade_count_result[0]['count'] if grade_count_result else 0
    avg_grade = avg_grade_result[0]['avg'] if avg_grade_result and avg_grade_result[0]['avg'] else 0
    
    # Get course average grades for chart
    course_avg_result = execute_query("""
        SELECT c.name, AVG(g.score) as avg_score
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        GROUP BY g.course_id, c.name
        ORDER BY c.name
    """)
    
    course_names = [row['name'] for row in course_avg_result]
    course_avgs = [float(row['avg_score']) for row in course_avg_result]
    
    # Get grade distribution for chart
    grade_dist_result = execute_query("""
        SELECT 
            SUM(CASE WHEN score < 60 THEN 1 ELSE 0 END) as fail,
            SUM(CASE WHEN score >= 60 AND score < 80 THEN 1 ELSE 0 END) as pass,
            SUM(CASE WHEN score >= 80 AND score < 90 THEN 1 ELSE 0 END) as good,
            SUM(CASE WHEN score >= 90 THEN 1 ELSE 0 END) as excellent
        FROM grades
    """)
    
    grade_dist = [
        grade_dist_result[0]['fail'] if grade_dist_result else 0,
        grade_dist_result[0]['pass'] if grade_dist_result else 0,
        grade_dist_result[0]['good'] if grade_dist_result else 0,
        grade_dist_result[0]['excellent'] if grade_dist_result else 0
    ]
    
    return render_template(
        'dashboard.html',
        username=session['username'],
        is_admin=session['is_admin'],
        student_count=student_count,
        course_count=course_count,
        grade_count=grade_count,
        avg_grade=avg_grade,
        course_names=course_names,
        course_avgs=course_avgs,
        grade_dist=grade_dist
    )

# Student routes
@app.route('/students')
@login_required
def students_list():
    students = get_all_students()
    return render_template('students/list.html', students=students, is_admin=session['is_admin'])

@app.route('/students/view/<student_id>')
@login_required
def student_view(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash('学生不存在', 'error')
        return redirect(url_for('students_list'))
    
    grades = get_grades_by_student(student_id)
    average = get_student_average(student_id)
    return render_template('students/view.html', student=student, grades=grades, average=average, is_admin=session['is_admin'])

@app.route('/students/add', methods=['GET', 'POST'])
@admin_required
def student_add():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        gender = request.form['gender']
        birthday = request.form.get('birthday') or None
        email = request.form.get('email') or None
        phone = request.form.get('phone') or None
        address = request.form.get('address') or None
        
        success, message = create_student(student_id, name, gender, birthday, email, phone, address)
        if success:
            flash('学生添加成功', 'success')
            return redirect(url_for('students_list'))
        else:
            flash(message, 'error')
    
    return render_template('students/add.html')

@app.route('/students/edit/<student_id>', methods=['GET', 'POST'])
@admin_required
def student_edit(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash('学生不存在', 'error')
        return redirect(url_for('students_list'))
    
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birthday = request.form.get('birthday') or None
        email = request.form.get('email') or None
        phone = request.form.get('phone') or None
        address = request.form.get('address') or None
        
        success, message = update_student(student_id, name, gender, birthday, email, phone, address)
        if success:
            flash('学生信息更新成功', 'success')
            return redirect(url_for('student_view', student_id=student_id))
        else:
            flash(message, 'error')
    
    return render_template('students/edit.html', student=student)

@app.route('/students/delete/<student_id>', methods=['POST'])
@admin_required
def student_delete(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash('学生不存在', 'error')
    else:
        # Delete student grades first (cascade would handle this, but being explicit)
        delete_student_grades(student_id)
        # Delete student
        success, message = delete_student(student_id)
        if success:
            flash('学生已删除', 'success')
        else:
            flash(message, 'error')
    
    return redirect(url_for('students_list'))

@app.route('/students/crud')
@login_required
def student_crud_example():
    students = get_all_students()
    return render_template('students/crud_example.html', students=students, is_admin=session['is_admin'])

# Course routes
@app.route('/courses')
@login_required
def courses_list():
    courses = get_all_courses()
    return render_template('courses/list.html', courses=courses, is_admin=session['is_admin'])

@app.route('/courses/view/<course_id>')
@login_required
def course_view(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash('课程不存在', 'error')
        return redirect(url_for('courses_list'))
    
    grades = get_grades_by_course(course_id)
    return render_template('courses/view.html', course=course, grades=grades, is_admin=session['is_admin'])

@app.route('/courses/add', methods=['GET', 'POST'])
@admin_required
def course_add():
    if request.method == 'POST':
        course_id = request.form['course_id']
        name = request.form['name']
        credit = request.form['credit']
        description = request.form.get('description') or None
        
        success, message = create_course(course_id, name, credit, description)
        if success:
            flash('课程添加成功', 'success')
            return redirect(url_for('courses_list'))
        else:
            flash(message, 'error')
    
    return render_template('courses/add.html')

@app.route('/courses/edit/<course_id>', methods=['GET', 'POST'])
@admin_required
def course_edit(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash('课程不存在', 'error')
        return redirect(url_for('courses_list'))
    
    if request.method == 'POST':
        name = request.form['name']
        credit = request.form['credit']
        description = request.form.get('description') or None
        
        success, message = update_course(course_id, name, credit, description)
        if success:
            flash('课程信息更新成功', 'success')
            return redirect(url_for('course_view', course_id=course_id))
        else:
            flash(message, 'error')
    
    return render_template('courses/edit.html', course=course)

@app.route('/courses/delete/<course_id>', methods=['POST'])
@admin_required
def course_delete(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash('课程不存在', 'error')
    else:
        success, message = delete_course(course_id)
        if success:
            flash('课程已删除', 'success')
        else:
            flash(message, 'error')
    
    return redirect(url_for('courses_list'))

@app.route('/courses/crud')
@login_required
def course_crud_example():
    courses = get_all_courses()
    return render_template('courses/crud_example.html', courses=courses, is_admin=session['is_admin'])

# Grade routes
@app.route('/grades/add', methods=['GET', 'POST'])
@admin_required
def grade_add():
    students = get_all_students()
    courses = get_all_courses()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        score = request.form['score']
        semester = request.form['semester']
        
        success, message = add_grade(student_id, course_id, score, semester)
        if success:
            flash('成绩添加成功', 'success')
            return redirect(url_for('student_view', student_id=student_id))
        else:
            flash(message, 'error')
    
    return render_template('grades/add.html', students=students, courses=courses)

@app.route('/grades/edit/<grade_id>', methods=['GET', 'POST'])
@admin_required
def grade_edit(grade_id):
    # This would need a function to get grade by ID in the grade model
    # For now, let's redirect to a view where grades can be edited
    flash('请在学生或课程详情页面修改成绩', 'info')
    return redirect(url_for('dashboard'))

@app.route('/grades/update', methods=['POST'])
@admin_required
def grade_update_ajax():
    grade_id = request.form.get('grade_id')
    score = request.form.get('score')
    
    if not grade_id or not score:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    try:
        success, message = update_grade(grade_id, score)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/grades/delete/<grade_id>', methods=['POST'])
@admin_required
def grade_delete(grade_id):
    success, message = delete_grade(grade_id)
    if success:
        flash('成绩已删除', 'success')
    else:
        flash(message, 'error')
    
    # Redirect back to previous page
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/grades/import', methods=['GET', 'POST'])
@admin_required
def import_grades():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Process CSV file
            try:
                csv_data = StringIO(file.read().decode('utf-8'))
                reader = csv.DictReader(csv_data)
                
                grades_data = []
                for row in reader:
                    grades_data.append(row)
                
                success_count, error_count = import_grades_from_csv(grades_data)
                
                if success_count > 0:
                    flash(f'成功导入 {success_count} 条成绩记录', 'success')
                if error_count > 0:
                    flash(f'导入失败 {error_count} 条记录', 'warning')
                
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f'导入失败: {str(e)}', 'error')
        else:
            flash('不支持的文件类型', 'error')
    
    return render_template('grades/import.html')

if __name__ == '__main__':
    app.run(debug=True) 