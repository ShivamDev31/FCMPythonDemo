from db.base_db import db
from db.json_serializer import Serializer


class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mobile_no = db.Column(db.String(10), unique=True)
    reg_id = db.Column(db.String(200), unique=True)

    def __init__(self, mobile_no, reg_id):
        self.mobile_no = mobile_no
        self.reg_id = reg_id