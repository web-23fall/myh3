from flask import Flask, request, session, redirect, url_for, render_template
from db.sql_conn import DataBase


app = Flask(__name__)
app.secret_key = "qwq"

db = DataBase('./db/user.db')


def checkLogin():
    return True if 'username' in session else False


@app.route('/', methods=['GET'])
def index():
    if not checkLogin():
        return redirect(url_for('login'))
    desp, results = db.selectAll('student_info')
    print(desp)
    print(results)
    return render_template('show.html', results=results, desp=desp)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = ['username', 'pwd']
        value = [request.form['username'], request.form['pwd']]
        _, results = db.Query2('users', id, value)
        assert _
        if results:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
