import json

from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from pip._vendor import requests
from sqlalchemy import select

import constants
from db.base_db import db
from db.register_user import Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://shivamdev:shivamdev31@localhost/fcm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
db.app = app
db.init_app(app)


@app.route('/')
def users():
    try:
        users = Users.query.all()
    except Exception as e:
        print(e)
    return render_template('users.html', users=users)


@app.route('/register/', methods=['POST'])
def register():
    reg_json = request.json
    mobile_no = reg_json['mobile_no']
    reg_id = reg_json['reg_id']

    user = Users(mobile_no, reg_id)
    db.session.add(user)
    db.session.commit()

    # print('{"mobile_no":' + str(user.mobile_no) + ' , "reg_id":' + user.reg_id)
    return jsonify(reg_json)


@app.route('/send/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'GET':
        return render_template('send_message.html')
    else:
        # take the message and sent it to google server
        message_title = request.form['message_title']
        message_body = request.form['message_body']
        url = constants.GOOGLE_FCM_URL
        reg_ids = list(Users.query.with_entities(Users.reg_id))

        headers = {'Authorization': constants.FCM_SERVER_KEY, 'Content-Type': "application/json"}
        data_js = {
            'to': reg_ids,
            'data': {
                'message_title': message_title,
                'message_body': message_body
            }
        }
        print(data_js)

        # request.headers = headers
        res = requests.post(url=url, headers = headers, data=data_js)
        print("Text : " + res.text)
        print("Content : " + res.content)
        return redirect(url_for('send_message'))


if __name__ == '__main__':
    app.run()
