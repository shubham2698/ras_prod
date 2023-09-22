import pymysql

def connect_database(dbname):
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=f"{dbname}")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()