import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    UPLOAD_FOLDER = os.getenv('upload_folder')
    SECRET_KEY = os.getenv('secret_key')
    DB_HOST = os.getenv('db_host')
    DB_USER = os.getenv('db_user')
    DB_PASSWORD = os.getenv('db_password')
    CSV_DIRECTORY = os.getenv('csv_directory')
    USER_DATABASE = os.getenv('user_database')

