#-*- encoding:utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import  Flask, url_for, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from models import db, Users, Questions, Comments, MySession
from check import validate, validate1
from werkzeug.security import generate_password_hash
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    db.create_all()


@app.context_processor
def my_context_processor():
    user = session.get('username')
    if user:
        return {'login_user': user}
    return {}


@app.route('/usercenter/',methods=['GET','POST'])
def user_center():
    user=Users.query.filter(Users.username==session.get('username')).first()
    return render_template('user.html',user=user)

@app.route('/usercenter/security/',methods=['GET','POST'])
def security():
    if request.method == 'GET':
        return render_template('security.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message=validate1(username,password1,password2)
        flash(message)
        if '修改成功' in message:
            user = Users.query.filter(Users.username == session.get('username')).first()
            user.password = password2
            db.session.commit()

            flash(message)
            return redirect(url_for('logout'))
        else:
            return render_template('security.html')

@app.route('/details/<question_id>/', methods=['GET', 'POST'])
def details(question_id):
    question_obj = Questions.query.filter(Questions.id == question_id).first()
    if request.method == 'GET':
        user = session.get('username')
        if user:
            return render_template('details.html', question=question_obj)
        else:
            flash('请先登录！')
            return render_template('login.html')
    else :
        comments_content=request.form.get('comment_desc')
        author_id = Users.query.filter(Users.username == session.get('username')).first().id
        new_comments=Comments(content=comments_content, question_id=question_id, author_id=author_id)
        db.session.add(new_comments)
        db.session.commit()
        return redirect(url_for('hello'))

@app.route('/search',methods=['GET'])
def search():
    # 获取GET数据，注意和获取POST数据的区别
    keyword = request.args.get('keyword')
    result = Questions.query.filter(or_(Questions.title.contains(keyword),
                                    Questions.content.contains(keyword))).order_by(
                                    Questions.create_time.desc()).all()
    if result:
        return render_template('hello.html', questions=result)
    else:
        return 'Not Found'

@app.route('/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        user = session.get('username')
        if user:
            return render_template('question.html')
        else :
            flash('请先登录！')
            return render_template('login.html')
    else:
            question_title = request.form.get('question_title')
            question_desc = request.form.get('question_desc')
            author_id = Users.query.filter(Users.username == session.get('username')).first().id
            new_question = Questions(title=question_title, content=question_desc, author_id=author_id)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('hello'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print password
        message = validate(username, password)
        if '成功' in message:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('hello'))
        else:
            flash(message)
            if '用户名不存在'in message:
                return render_template('register.html')
            elif '密码错误' in message:
                return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('hello'))

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message=validate(username,password1,password2)
        flash(message)
        if '注册成功' in message:
            new_user=Users(username=username, password=password1, register_time=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')

@app.route('/')
def hello():
    questions = Questions.query.order_by(Questions.create_time.desc()).all()
    return render_template('hello.html',questions=questions)

if __name__ == '__main__':
    app.run(debug=True)