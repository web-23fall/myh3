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
        # print(sql)
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

    def Update(self, data, table):
        conn = self.Open()
        cur = conn.cursor()
        values = []
        idName = list(data)[0]
        for v in list(data)[1:]:
            values.append("%s='%s'" % (v, data[v]))
        sql = "update %s set %s where %s = '%s'" % (table, ",".join(values), idName, data[idName])
        print(sql)
        cur.execute(sql)
        conn.commit()
        Close(conn)

    def Insert(self, data, table):
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

    def DeleteById(self, id, value, table):
        conn = self.Open()
        values = []
        cur = conn.cursor()
        sql = "delete from %s where %s=?" % (table, id)
        print(sql)
        cur.execute(sql, (value,))
        conn.commit()
        Close(conn)