
from flask import Flask,render_template,Markup

app= Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.route('/login/')
def login():
    return 'LOGIN'

@app.route('/profile/<int:uid>/',methods=['GET', 'POST'])
def profile(uid):
    colors={'red','green'}
    dict={'now':'1.213213','google':'2.2332','baidu':'3.321312'}

    return render_template('user.html',uid=uid,colors=colors,dict=dict)
if __name__ == '__main__':

    app.run(debug=True)