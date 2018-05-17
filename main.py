from flask import  Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Users, Questions, Comments
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    db.drop_all()
    db.create_all()

@app.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(username, password1, password2)
        return ' '
@app.route('/')
def hello():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)