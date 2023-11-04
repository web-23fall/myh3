# project-23fall

实际项目中，数据库使用的是 `./db/user.db`，而不是 `./db/user2.db`，`user2.db` 仅为测试 `db_test.py` 之用。


数据库使用及维护请使用 `./db/sql_conn.py`，在根目录下的 `db_test.py` 中有对应用法的测试，可以通过此了解函数的使用方法。

TIP1：在写代码之前，请先将项目 fork 到自己的仓库（或团队的仓库）中一份，再对 fork 出的项目进行修改，而不是直接 clone 已经写好的 `project-23fall`。

TIP2：经常性地进行 git pull 是好习惯。

TIP3：确定代码无误后，请通过 `Pull Request` 的方式将代码进行合并。

Q：如何将自己写好的代码通过 git 上传？

A：在终端中 cd 到项目的根目录下，输入如下命令：
```git
git add .
git commit -m "yyyymmdd-改动的简要描述"
git push
```

