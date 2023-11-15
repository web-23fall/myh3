from db.sql_conn import DataBase


db = DataBase('./db/user2.db')


def retrieveTest():
    # desp, results = db.Query("select * from student_info")
    ids = ['stu_id', 'stu_sex']
    values = ['1', '女']
    desp, results = db.Query2('student_info', ids, values)
    # db.DeleteById(id, value, 'student_info')
    assert desp
    print(desp)
    print(results)
    return len(desp), desp, results

def insertTest():
    _, results = db.selectAll('users')
    print(results)
    data = dict(
        username = '233',
        pwd = 'qwq12345'
    )
    db.Insert('users', data)
    _, results = db.selectAll('users')
    print(results)

def updateTest():
    ids = ['username', 'pwd']
    values = ['233', 'qwq12345']
    _, results = db.Query2('users', ids, values)
    print(results)
    # id 属性对应着一个 list，里面放着一（或多）个 id 的名称
    data = dict(
        id = ['username'],
        username = '233',
        pwd = '1q2w3e4r',
    )
    db.Update('users', data)
    _, results = db.Query("select * from users where username = %s" % '233')
    print(results)

def deleteByOneIdTest():
    _, results = db.Query("select * from users where username = %s" % '233')
    print(results)
    db.DeleteById('users', 'username', '233')
    _, results = db.Query("select * from users where username = %s" % '233')
    print(results)

def deleteByMultiIdTest():
    _, results = db.Query("select * from users where username = %s" % '233')
    print(results)
    # 此处 id 中的值和 value 中的值要严格对应
    ids = ['username', 'pwd']
    values = ['233', '1q2w3e4r']
    db.DeleteById('users', ids, values)
    _, results = db.Query("select * from users where username = %s" % '233')
    print(results)


retrieveTest()
insertTest()
updateTest()
deleteByOneIdTest()
# deleteByMultiIdTest()
