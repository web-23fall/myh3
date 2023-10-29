from flask import Flask, request, session, redirect, url_for, render_template
from db.sql_conn import DataBase


app = Flask(__name__)
app.secret_key = "qwq"

db = DataBase('./db/user.db')


def checkLogin():
    return True if 'username' in session else False


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


@app.route('/', methods=['GET'])
def index():
    if not checkLogin():
        return redirect(url_for('login'))
    ids = []
    values = []
    if "id" in request.args:
        ids.append('stu_id')
        if request.args["id"] != "":
            values.append(request.args["id"])
    if "name" in request.args:
        ids.append('stu_name')
        if request.args["name"] != "":
            values.append(request.args["name"])

    if len(ids) != 0:
        desp, results = db.Query2('student_info', ids, values)
    else:
        desp, results = db.selectAll('student_info')
    return render_template('show.html', results=results, desp=desp)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if not checkLogin():
        return redirect(url_for('login'))
    if request.method == 'GET':
        _, results = db.selectAll('student_profession')
        return render_template('add.html', pros=results)

    data = dict(
        stu_id=request.form['stu_id'],
        stu_name=request.form['stu_name'],
        stu_sex=request.form['stu_sex'],
        stu_age=request.form['stu_age'],
        stu_origin=request.form['stu_origin'],
        stu_profession=request.form['stu_profession']
    )
    db.Insert('student_info', data)
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if not checkLogin():
        return redirect(url_for('login'))

    if request.method == 'GET':
        ids = ['stu_id']
        values = [request.args['id']]
        _, stu = db.Query2('student_info', ids, values)
        _, pros = db.selectAll('student_profession')
        return render_template('update.html', stu=stu[0], pros=pros)

    data = dict(
        ID=['stu_id'],
        stu_id=request.form['stu_id'],
        stu_name=request.form['stu_name'],
        stu_sex=request.form['stu_sex'],
        stu_age=request.form['stu_age'],
        stu_origin=request.form['stu_origin'],
        stu_profession=request.form['stu_profession']
    )
    db.Update('student_info', data)
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if not checkLogin():
        return redirect(url_for('login'))
    db.DeleteById('student_info', 'stu_id', id)
    return redirect(url_for('index'))


@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
