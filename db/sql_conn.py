import sqlite3
from flask import flash


def close(conn):
    conn.close()


class DataBase:
    def __init__(self, db):
        self.database = db

    def open(self):
        conn = sqlite3.connect(self.database)
        return conn

    def query(self, sql):
        conn = self.open()
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except BaseException as e:
            flash(e.args[0], "error")
            return [], []
        else:
            description = []
            for d in cur.description:
                description.append(d[0])
            result = cur.fetchall()
            cur.close()
            close(conn)
            return description, result

    def selectAll(self, table):
        conn = self.open()
        cur = conn.cursor()
        sql = "select * from %s" % table
        try:
            cur.execute(sql)
        except BaseException as e:
            flash(e.args[0], "error")
            return [], []
        else:
            description = []
            for d in cur.description:
                description.append(d[0])
            result = cur.fetchall()
            cur.close()
            close(conn)
            return description, result

    def query2(self, table, ids, value):
        conn = self.open()
        cur = conn.cursor()
        if type(ids) in [list]:
            values = []
            for i in range(len(ids)):
                values.append("%s='%s'" % (ids[i], value[i]))
            sql = "select * from '%s' where %s" % (table, " and ".join(values))
        else:
            sql = "select * from '%s' where %s='%s'" % (table, ids, value)
        print(sql)
        try:
            cur.execute(sql)
        except BaseException as e:
            flash(e.args[0], "error")
            return [], []
        else:
            description = []
            for d in cur.description:
                description.append(d[0])
            result = cur.fetchall()
            cur.close()
            close(conn)
            return description, result

    def checkid(self, table, idname, id):
        conn = self.open()
        cur = conn.cursor()
        sql = "select * from '%s' where %s='%s'" % (table, idname, id)
        print(sql)
        try:
            cur.execute(sql)
        except BaseException as e:
            flash(e.args[0], "error")
            return []
        else:
            result = cur.fetchall()
            cur.close()
            close(conn)
            return result

    def update(self, table, data):
        conn = self.open()
        cur = conn.cursor()
        values = []
        ids = []
        idnames = data["ID"]
        print(idnames)
        for v in list(data):
            if v in idnames:
                ids.append("%s='%s'" % (v, data[v]))
            elif v != "ID":
                values.append("%s='%s'" % (v, data[v]))
        sql = "update %s set %s where %s" % (table, ",".join(values), " and ".join(ids))
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except BaseException as e:
            flash(e.args[0], "error")
        else:
            cur.close()
            close(conn)

    def insert(self, table, data):
        conn = self.open()
        cur = conn.cursor()
        values = []
        fieldnames = list(data)
        for v in fieldnames:
            values.append(data[v])
        sql = "insert into %s (%s) values (%s) " % (
            table,
            ",".join(fieldnames),
            ",".join(["?"] * len(fieldnames)),
        )
        print(sql)
        try:
            cur.execute(sql, values)
            conn.commit()
        except BaseException as e:
            flash(e.args[0], "error")
        else:
            cur.close()
            close(conn)

    def deleteById(self, table, ids, value):
        conn = self.open()
        values = []
        cur = conn.cursor()
        if type(ids) in [list]:
            for i in range(len(ids)):
                values.append("%s='%s'" % (ids[i], value[i]))
            sql = "delete from %s where %s" % (table, " and ".join(values))
            print(sql)
            try:
                cur.execute(sql)
                conn.commit()
            except BaseException as e:
                flash(e.args[0], "error")
            else:
                cur.close()
                close(conn)
        else:
            sql = "delete from %s where %s=?" % (table, ids)
            print(sql)
            try:
                cur.execute(sql, (value,))
                conn.commit()
            except BaseException as e:
                flash(e.args[0], "error")
            else:
                cur.close()
                close(conn)

    def updateAgeById(self, table, ids, value, age):
        conn = self.open()
        values = []
        cur = conn.cursor()
        if type(ids) in [list]:
            for i in range(len(ids)):
                values.append("%s='%s'" % (ids[i], value[i]))
            # sql = "delete from %s where %s" % (table, " and ".join(values))
            sql = "update %s set stu_age=%d where %s" % (
                table,
                age,
                " and ".join(values),
            )
            print(sql)
            try:
                cur.execute(sql)
                conn.commit()
            except BaseException as e:
                flash(e.args[0], "error")
            else:
                cur.close()
                close(conn)
        else:
            # sql = "delete from %s where %s=?" % (table, id)
            sql = "update %s set stu_age=%d where %s=?" % (table, age, ids)
            print(sql)
            try:
                cur.execute(sql, (value,))
                conn.commit()
            except BaseException as e:
                flash(e.args[0], "error")
            else:
                cur.close()
                close(conn)
