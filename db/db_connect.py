import pymysql


def connection():
    conn = pymysql.connect(host="localhost",
                           user="shivamdev",
                           password="shivamdev31",
                           database="fcm")

    cursor = conn.cursor()

    return cursor, conn
