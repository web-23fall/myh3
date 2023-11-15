import sqlite3


def Close(conn):
    conn.close()


class DataBase:
    def __init__(self, db):
        self.database = db

    def Open(self):
        conn = sqlite3.connect(self.database)
        return conn

    def Query(self, sql):
        conn = self.Open()
        cur = conn.cursor()
        cur.execute(sql)

        description = []
        for d in cur.description:
            description.append(d[0])
        result = cur.fetchall()

        cur.close()
        Close(conn)
        return description, result

    def selectAll(self, table):
        conn = self.Open()
        cur = conn.cursor()
        sql = "select * from %s" % table
        print(sql)
        cur.execute(sql)

        description = []
        for d in cur.description:
            description.append(d[0])
        result = cur.fetchall()

        cur.close()
        Close(conn)
        return description, result

    def Query2(self, table, ids, value):
        conn = self.Open()
        cur = conn.cursor()
        values = []
        for i in range(len(ids)):
            values.append("%s='%s'" % (ids[i], value[i]))
        sql = "select * from %s where %s" % (table, " and ".join(values))
        print(sql)
        cur.execute(sql)

        description = []
        for d in cur.description:
            description.append(d[0])
        result = cur.fetchall()

        cur.close()
        Close(conn)
        return description, result

    def username_exists(self, username):
        conn = self.Open()
        cur = conn.cursor()
        sql = "select * from users where username = %s" % username
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        Close(conn)
        return result

    def Update(self, table, data):
        conn = self.Open()
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
        cur.execute(sql)
        conn.commit()
        Close(conn)

    def Insert(self, table, data):
        conn = self.Open()
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
        cur.execute(sql, values)
        conn.commit()
        Close(conn)

    def DeleteById(self, table, ids, value):
        # print(type(id))
        conn = self.Open()
        values = []
        cur = conn.cursor()
        if type(ids) in [list]:
            for i in range(len(ids)):
                values.append("%s='%s'" % (ids[i], value[i]))
            sql = "delete from %s where %s" % (table, " and ".join(values))
            print(sql)
            cur.execute(sql)
            conn.commit()
        else:
            sql = "delete from %s where %s=?" % (table, ids)
            print(sql)
            cur.execute(sql, (value,))
            conn.commit()
        Close(conn)

    def UpdateAgeById(self, table, ids, value, age):
        conn = self.Open()
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
            cur.execute(sql)
            conn.commit()
        else:
            # sql = "delete from %s where %s=?" % (table, id)
            sql = "update %s set stu_age=%d where %s=?" % (table, age, ids)
            print(sql)
            cur.execute(sql, (value,))
            conn.commit()
        Close(conn)
