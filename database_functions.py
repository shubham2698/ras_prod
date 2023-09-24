import pymysql


def connection_mysql_server():
    try:
        connection1 = pymysql.connect(host="localhost", user="root", passwd="")
        mysql_server_connection = connection1.cursor()
        return mysql_server_connection
    except:
        print("\033[91mFAILED TO CONNECT MYSQL SERVER\033[0m")
        exit()


def connect_database(dbname):
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=f"{dbname}")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()