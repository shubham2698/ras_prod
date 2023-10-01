import pymysql
import re
import zipfile
import os
from run import app

def zip_csv_files(csv_directory, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(csv_directory):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)



def connection_mysql_server():
    try:
        connection1 = pymysql.connect(host=app.config['DB_HOST'], user=app.config['DB_USER'], passwd=app.config['DB_PASSWORD'])
        mysql_server_connection = connection1.cursor()
        return mysql_server_connection
    except:
        print("\033[91mFAILED TO CONNECT MYSQL SERVER\033[0m")
        exit()


def connect_database(dbname):
    try:
        connection = pymysql.connect(host=app.config['DB_HOST'], user=app.config['DB_USER'], passwd=app.config['DB_PASSWORD'], database=f"{dbname}")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()



def is_valid_password(psd,cpsd,phone):
    phone_pattern = r'^[789]\d{9}$'
    if psd != cpsd:
        return False
    if len(psd) < 8:
        return False
    if not re.match(phone_pattern,phone):
        return False
    if not (re.search(r'[A-Z]', psd) and
            re.search(r'[a-z]', psd) and
            re.search(r'\d', psd) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', psd)):
        return False
    
    return True



def is_pdf(filename):
    return filename.lower().endswith('.pdf')

