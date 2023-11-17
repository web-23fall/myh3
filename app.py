from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template,
    flash,
    jsonify,
)
from db.sql_conn import DataBase
from hand_utils.util import generate_equation, generate_image, paging
from flask_socketio import SocketIO, emit

import bcrypt, hashlib, os, shutil, threading


app = Flask(__name__)
app.secret_key = "qwq"

db = DataBase("./db/user.db")
code_sha1 = ""

socketio = SocketIO(app)
logging_in_users = 0
THRESHOLD_USERS = 5
EXECUTE_TIME = 600


def checkLogin():
    return True if "username" in session else False


def createTimer():
    t = threading.Timer(EXECUTE_TIME, repeat)
    t.start()


def repeat():
    global logging_in_users
    if logging_in_users <= THRESHOLD_USERS:
        if os.path.exists("./static/images"):
            shutil.rmtree("./static/images")
            os.mkdir("./static/images")
    createTimer()


@socketio.on("connect")
def handle_connect():
    global logging_in_users
    logging_in_users += 1


@socketio.on("disconnect")
def handle_disconnect():
    global logging_in_users
    logging_in_users -= 1


# @app.before_request
# def before_request():
#     pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
#     if request.method == "GET":
#         data = request.args
#     else:
#         data = request.json
#     for v in data.values():
#         v = str(v).lower()
#         r = re.search(pattern, v)
#         if r:
#             return "请输入规范的参数！"


@app.route("/code", methods=["POST"])
def generate_code():
    data = request.form.get("request_code")
    last_image_path = request.form.get("last_image_path")
    if data == "true":
        eqt, _ = generate_equation()
        global code_sha1
        code_sha1 = _
        if last_image_path != "":
            if not os.path.exists(last_image_path):
                server_error_json = {
                    "code": "server_error",
                    "path": "",
                    "status": "failed",
                }
                return jsonify(server_error_json)
            else:
                os.remove(last_image_path)
        img_path = generate_image(eqt)
        code_json = {"code": eqt, "path": img_path, "status": "success"}
        return jsonify(code_json)
    else:
        error_json = {"code": "error", "path": "", "status": "failed"}
        return jsonify(error_json)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username", type=str).strip()
        pwd = request.form.get("pwd", type=str).strip()

        if db.username_exists(username):
            flash("用户名已被注册，请选择不同的用户名。", "error")
            return redirect(url_for("register"))
        # print(db.username_exists(username))
        salt = bcrypt.gensalt()
        spwd = bcrypt.hashpw(pwd.encode("utf-8"), salt)
        # print(username," ",spwd," ",salt)
        data = dict(
            username=username, pwd=spwd.decode("utf-8"), salt=salt.decode("utf-8")
        )
        db.insert("users", data)
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if not os.path.exists("./static/images"):
        os.mkdir("./static/images")
    if request.method == "GET":
        return render_template("login.html")
    else:
        ids = ["username"]
        username = request.form.get("username", type=str).strip()
        value = [username]
        _, userinfo = db.query2("users", ids, value)
        print(userinfo)
        pwd = request.form.get("pwd", type=str).strip()
        code_get = request.form.get("code").strip()
        vfc_sha1 = hashlib.sha1()
        vfc_sha1.update(code_get.encode("utf-8"))
        if code_sha1 == vfc_sha1.hexdigest():
            if userinfo:
                if bcrypt.checkpw(pwd.encode("utf-8"), userinfo[0][1].encode("utf-8")):
                    session["username"] = username
                    return redirect(url_for("index"))
                else:
                    flash("密码不正确", "error")
            else:
                flash("用户名不存在", "error")
        else:
            flash("验证码错误", "error")
        return render_template("login.html")


@app.route("/", methods=["GET"])
def index():
    if not checkLogin():
        return redirect(url_for("login"))
    page = request.args.get("page", 1, type=int)
    ids = []
    values = []
    if "id" in request.args:
        ids.append("stu_id")
        stu_id = request.args.get("id", type=int)
        if stu_id != "" or stu_id is not None:
            values.append(stu_id)
    if "name" in request.args:
        ids.append("stu_name")
        stu_name = request.args.get("name", type=str)
        if stu_name != "" or stu_name is not None:
            values.append(stu_name.strip())

    if len(ids) != 0:
        desp, result = db.query2("student_info", ids, values)
    else:
        desp, result = db.selectAll("student_info")
    if len(result) == 0:
        flash("查询结果为空，请检查查询条件", "error")
    results, pagination = paging(result, page, per_page=20)

    return render_template(
        "show.html", results=results, desp=desp, pagination=pagination, page=page
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if not checkLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        _, results = db.selectAll("student_profession")
        return render_template("add.html", pros=results)

    data = dict(
        stu_id=request.form.get("stu_id", type=int),
        stu_name=request.form.get("stu_name", type=str).strip(),
        stu_sex=request.form.get("stu_sex", type=str).strip(),
        stu_age=request.form.get("stu_age", type=int),
        stu_origin=request.form.get("stu_origin", type=str).strip(),
        stu_profession=request.form.get("stu_profession", type=str).strip(),
    )
    db.insert("student_info", data)
    return redirect(url_for("index"))


@app.route("/update", methods=["GET", "POST"])
def update():
    if not checkLogin():
        return redirect(url_for("login"))

    if request.method == "GET":
        ids = ["stu_id"]
        stu_id = request.args.get("id", type=int)
        values = [stu_id]
        _, stu = db.query2("student_info", ids, values)
        _, pros = db.selectAll("student_profession")
        return render_template("update.html", stu=stu[0], pros=pros)

    data = dict(
        ID=["stu_id"],
        stu_id=request.form.get("stu_id", type=int),
        stu_name=request.form.get("stu_name", type=str).strip(),
        stu_sex=request.form.get("stu_sex", type=str).strip(),
        stu_age=request.form.get("stu_age", type=int),
        stu_origin=request.form.get("stu_origin", type=str).strip(),
        stu_profession=request.form.get("stu_profession", type=str).strip(),
    )
    db.update("student_info", data)
    return redirect(url_for("index"))


@app.route("/delete/<int:ids>", methods=["GET"])
def delete(ids):
    if not checkLogin():
        return redirect(url_for("login"))
    db.deleteById("student_info", "stu_id", ids)
    return redirect(url_for("index"))


@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    return redirect(url_for("login"))


@app.route("/delete_all", methods=["GET", "POST"])
def deleteAll():
    if not checkLogin():
        return redirect(url_for("login"))
    print(request.form)
    idlist = request.form.getlist("ids[]")
    print(idlist)
    for stuId in idlist:
        db.deleteById("student_info", "stu_id", stuId)

    return redirect(url_for("index"))


@app.route("/updateAge", methods=["GET", "POST"])
def updateAge():
    if not checkLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        desp, result = db.selectAll("student_info")

        results, pagination = paging(result, page, per_page=20)

        return render_template(
            "updateAge.html",
            results=results,
            desp=desp,
            pagination=pagination,
            page=page,
        )

    stu_age = int(request.form.get("age"))
    # stu_age = request.args.get("age", type=int)
    idlist = request.form.getlist("ids")
    for stuId in idlist:
        db.updateAgeById("student_info", "stu_id", stuId, stu_age)
    return redirect(url_for("index"))


createTimer()

if __name__ == "__main__":
    # When deploying the project on a cloud server, you need to change the value of "host" in the parameters.
    # Linux server can check the intranet IP address through the "ifconfig" command.
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
