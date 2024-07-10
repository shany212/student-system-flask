import flask
import csv
from io import StringIO
from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from model.check_login import is_existed,exist_user,is_null,is_admin
from model.check_regist import add_user
from model.insert_grade import insert_grade
from model.search_info import search_by_id,search_by_kch
from model.updata_grade import updata_by_kch,updata_by_id
from model.delete_stu import delete_by_id

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            admin_message = "管理员登录"
            visitor_message = "游客登陆"
            if(is_admin(username)):
                return render_template('index.html', username=username, message=admin_message)
            else:
                return render_template('index.html', username=username, message=visitor_message)
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'] )
            return render_template('index.html', username=username)
    return render_template('register.html')


@app.route("/grade",methods=["GET","POST"])
def grade():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student_class_id = request.form['student_class_id']
        grade = request.form['grade']
        insert_grade(student_id,student_class_id,grade)
    return render_template("grade.html")

@app.route("/grade_info",methods=["GET","POST"])
def grade_info():
    result = []
    if request.method == 'POST':
        opt = request.form['selected_one']
        type = request.form['query']
        print(opt,type)
        if opt == "学号":
            result=search_by_id(type)
        else:
            result=search_by_kch(type)

        print(result)
    return render_template("grade_infos.html",results=result)


@app.route('/grade_infos_vis',methods=['GET','POST'])
def grade_infos_vis():
    result = []
    if request.method == 'POST':
        opt = request.form['selected_one']
        type = request.form['query']
        print(opt, type)
        if opt == "学号":
            result = search_by_id(type)
        else:
            result = search_by_kch(type)
    return render_template('grade_infos_vis.html',results=result)

@app.route('/upload_grades', methods=['POST'])
def upload_grades():
    try:
        file = flask.request.files['file']
        csv_data = StringIO(file.read().decode('utf-8'))
        csv_reader = csv.reader(csv_data)
        next(csv_reader)
        print(csv_reader)
        for row in csv_reader:
            insert_grade(row[0],row[1],row[2])
        return flask.render_template('result.html', success = "True",message="成绩批量导入成功")
    except Exception as e:
        return flask.render_template('result.html', success = "False",message=str(e))

@app.route('/grade_updata',methods=["GET","POST"])
def grade_updata():
    if request.method == 'POST':
        opt = request.form['selected_one']
        type = request.form['query']
        grade = request.form['last_query']
        print(opt, type ,grade)
        if opt == "学号":
            updata_by_id(type,grade)
        else:
            updata_by_kch(type,grade)

    return render_template("grade_updata.html")


@app.route('/grade_delete',methods=["GET","POST"])
def grade_delete():
    if request.method == 'POST':
        type = request.form['query']
        delete_by_id(type)
    return render_template("grade_delete.html")



if __name__=="__main__":
    app.run(debug=True)
