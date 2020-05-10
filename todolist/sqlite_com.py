import sqlite3 as sql

columns = ['ID_Code', 'title', 'expiry_date', 'tags', 'status']


def conn_cursor():
    conn = sql.connect('todolist.db')
    cursor = conn.cursor()
    return cursor, conn


def databaseBuild():
    conn = sql.connect('todolist.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE todolist (
                    ID_Code text, title text,
                    expiry_date text, tags text,
                    status int
                    )""")

        conn.commit()
        conn.close()

        return 'Database built'
    except Exception as e:
        return e


def databaseCols(columns):
    cols = []

    conn = sql.connect('todolist.db')
    c = conn.cursor()
    c.execute('SELECT * FROM todolist')

    for i in c.description:
        cols.append(i[0])

    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()

    for i in tables:
        for e in i:
            if e == 'todolist':
                c.execute('SELECT * FROM todolist')

                for i in c.description:
                    cols.append(i[0])

                if set(columns) == set(cols):
                    return True
                else:
                    print('hello')
                    return False

    return False


def dropTable():
    conn = sql.connect('todolist.db')
    c = conn.cursor()
    c.execute('DROP TABLE todolist')
    conn.commit()
    conn.close()


class SQL_EComm:
    ADD_Comm = 'INSERT INTO todolist VALUES (?, ?, ?, ?, ?)'
    EDIT_Comm = 'UPDATE todolist SET title = ?, expiry_date = ? WHERE ID_Code = ?'
    TAG_Comm = 'UPDATE todolist SET tags = ? WHERE ID_Code = ?'
    REM_Comm = 'UPDATE todolist SET status = 1 WHERE ID_Code = ?'


class SQL_RComm:
    READ_All = 'SELECT * FROM todolist'
    READ_Incomplete = 'SELECT * FROM todolist WHERE status = 0'
    READ_Complete = 'SELECT * FROM todolist WHERE status = 1'
    READ_TagComp = 'SELECT * FROM todolist WHERE tags = ? and status = 1'
    READ_TagInComp = 'SELECT * FROM todolist WHERE tags = ? and status = 0'
