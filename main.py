#-*- encoding:utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import  Flask, url_for, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Users, Questions, Comments
from check import validate
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