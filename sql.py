def sqlSELECT(sql):
    import pymysql

    connection = pymysql.connect(
        host="localhost",
        db="mydb",
        user="root",
        password="daradara",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    sqlout = cursor.fetchall()

    cursor.close()
    connection.close()

    return sqlout

def sqlUPDATE(sql):
    import pymysql

    connection = pymysql.connect(
        host="localhost",
        db="mydb",
        user="root",
        password="daradara",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()

    return