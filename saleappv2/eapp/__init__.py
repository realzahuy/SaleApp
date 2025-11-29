import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "zahuytop1"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/saledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
db = SQLAlchemy(app=app)
login = LoginManager(app=app)

cloudinary.config(cloud_name='zhcloud',
                  api_key='583985617519356',
                  api_secret='WxOV6N6KQcs-ySMFqLUi5KRwbzI')