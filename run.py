from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Admin1234@database-1.c7sweeci81lq.us-east-1.rds.amazonaws.com:3306/final_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from routes import *


if __name__ == '__main__':
    #db.create_all()  # Create database tables for our data models
    app.run(debug=True)
