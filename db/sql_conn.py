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

    def Query2(self, table, id, value):
        conn = self.Open()
        cur = conn.cursor()
        values = []
        for i in range(len(id)):
            values.append("%s='%s'" % (id[i], value[i]))
        sql = "select * from %s where %s" % (table, ' and '.join(values))
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
        idNames = data['ID']
        print(idNames)
        for v in list(data):
            if v in idNames:
                ids.append("%s='%s'" % (v, data[v]))
            elif v != 'ID':
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
        fieldNames = list(data)
        for v in fieldNames:
            values.append(data[v])
        sql = "insert into %s (%s) values (%s) " % (table, ",".join(fieldNames), ",".join(["?"] * len(fieldNames)))
        print(sql)
        cur.execute(sql, values)
        conn.commit()
        Close(conn)

    def DeleteById(self, table, id, value):
        # print(type(id))
        conn = self.Open()
        values = []
        cur = conn.cursor()
        if type(id) in [list]:
            for i in range(len(id)):
                values.append("%s='%s'" % (id[i], value[i]))
            sql = "delete from %s where %s" % (table, " and ".join(values))
            print(sql)
            cur.execute(sql)
            conn.commit()
        else:
            sql = "delete from %s where %s=?" % (table, id)
            print(sql)
            cur.execute(sql, (value,))
            conn.commit()
        Close(conn)
