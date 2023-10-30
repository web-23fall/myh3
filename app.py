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
        value = [request.form.get('username', type=str), request.form.get('pwd', type=str)]
        _, results = db.Query2('users', id, value)
        assert _
        if results:
            session['username'] = request.form.get('username', type=str)
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
        stu_id = request.args.get("id", type=int)
        if stu_id != "":
            values.append(stu_id)
    if "name" in request.args:
        ids.append('stu_name')
        stu_name = request.args.get("name", type=str)
        if stu_name != "":
            values.append(stu_name)

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
        stu_id=request.form.get('stu_id', type=int),
        stu_name=request.form.get('stu_name', type=str),
        stu_sex=request.form.get('stu_sex', type=str),
        stu_age=request.form.get('stu_age', type=int),
        stu_origin=request.form.get('stu_origin', type=str),
        stu_profession=request.form.get('stu_profession', type=str)
    )
    db.Insert('student_info', data)
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if not checkLogin():
        return redirect(url_for('login'))

    if request.method == 'GET':
        ids = ['stu_id']
        stu_id = request.args.get('id', type=str)
        values = [stu_id]
        _, stu = db.Query2('student_info', ids, values)
        _, pros = db.selectAll('student_profession')
        return render_template('update.html', stu=stu[0], pros=pros)

    data = dict(
        ID=['stu_id'],
        stu_id=request.form.get('stu_id', type=int),
        stu_name=request.form.get('stu_name', type=str),
        stu_sex=request.form.get('stu_sex', type=str),
        stu_age=request.form.get('stu_age', type=int),
        stu_origin=request.form.get('stu_origin', type=str),
        stu_profession=request.form.get('stu_profession', type=str)
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
