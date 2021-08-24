import time
from flask import Blueprint,request
from Lib.Signup import *
from Lib.Auth import Auth
import json
auth_api = Blueprint('auth_api',__name__)


def mysqlclean(a):
    return a


@auth_api.route('/auth/signup',methods=['POST'])
def signup():
    request_data = request.form
    username = mysqlclean(request_data.get('username'))
    email = mysqlclean(request_data.get('email'))
    password = mysqlclean(request_data.get('password'))
    a = Signup()
    if a.createuser(username, email, password):
        data={
            'Message': 'Signup Success',
            'Username': username,
            'Email': email,

        }
        return json.dumps(data),200
    else:
        data = {
            'Error':'Signup Failure',
            'Message':'Email already exists',
        }
        return json.dumps(data),409


@auth_api.route('/auth/login',methods=['POST'])
def login():

    request_data = request.form
    email = mysqlclean(request_data.get('email'))
    password = mysqlclean(request_data.get('password'))

    if email and password:

        try:
            start = time.time()
            a=Auth(email,password)
            end=time.time()
            data={
                'Message':'login Success',
                'Data':a.getdata(),
                'time':end-start
            }
            return json.dumps(data),200

        except Exception as e:
            data={
                'Error':e
            }
            return json.dumps(data),403

    else:
        data={
            'Error':'Invalid Request'
        }
        return json.dumps(data),400

@auth_api.route('/auth/isvalid', methods=['POST'])
def is_valid():
    request_data = request.form
    token = mysqlclean(request_data.get('token'))
    if token:
        a=Auth(token)
    else:
        return {'Error':'No data Input'},400
    if a.authenticate():
        data={
            'Valid': True,
            'Valid_for':a.valid_for_token()
        }
        return json.dumps(data),200
    else:
        data={
            'Error':'Invalid Token'
        }
        return json.dumps(data),400
