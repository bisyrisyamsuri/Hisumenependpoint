import mysql.connector


def conn(user="root", password="", host="localhost", database="hisumenep"):

    conn = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    return conn


def select(query, values, conn):
    my = conn.cursor()
    my.execute(query, values)
    row = [x[0] for x in my.description]
    result = my.fetchall()
    json_data = []
    for r in result:
        json_data.append(dict(zip(row, r)))
    return json_data