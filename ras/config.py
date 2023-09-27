class Config:
    UPLOAD_FOLDER = 'PDF'
    SECRET_KEY = 'raspibm'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
