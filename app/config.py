import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql+pymysql://root:@db:3306/themapp_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
