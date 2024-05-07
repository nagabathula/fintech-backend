import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Admin1234@database-1.c7sweeci81lq.us-east-1.rds.amazonaws.com:3306/final_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False