# project-23fall

## 项目开发说明

实际项目中，数据库使用的是 `./db/user.db`，而不是 `./db/user2.db`，`user2.db` 仅为测试 `db_test.py` 之用。


数据库使用及维护请使用 `./db/sql_conn.py`，在根目录下的 `db_test.py` 中有对应用法的测试，可以通过此了解函数的使用方法。

TIP1：在写代码之前，请先将项目 fork 到自己的仓库（或团队的仓库）中一份，再对 fork 出的项目进行修改，而不是直接 clone 已经写好的 `project-23fall`。

TIP2：经常性地进行 `git pull` 是好习惯。

TIP3：确定代码无误后，请通过 `Pull Request` 的方式将代码进行合并。

Q：如何将自己写好的代码通过 git 上传？

A：在终端中 cd 到项目的根目录下，输入如下命令：
```git
git add .
git commit -m "yyyymmdd-改动的简要描述"
git push
```
--------------

## 项目说明

本项目为 2023 年秋季学期《Web 技术》课程大作业项目。

运行方式为：`git clone` 本项目到本地后，进入项目根目录，运行如下命令：
```
pip install -r requirements.txt
flask run
```

之后在浏览器中访问 `http://localhost:5000` 即可。

测试用户名为 `12345qwq!`，测试密码为 `123abc!`。

如果需要进行自动化测试，则在项目根目录下运行如下命令：
```
pip install -r requirements.txt
pip install pyvirtualdisplay
```
之后在当前终端中运行 `flask run`，再另一个终端中，进入项目根目录，运行 `pytest ./static/test` 即可。

注意，您可能需要手动下载 Google Chrome 浏览器。