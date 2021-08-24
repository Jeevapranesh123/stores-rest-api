import pymongo
import secrets
import time
client = pymongo.MongoClient('mongodb+srv://jeeva:DOCKoC2kvdHVHmzT@flask-api.atefn.mongodb.net/test')
db = client.API
Users = db.Users
Sessions = db.Sessions


def mysqlclean(a):
    return a


class Auth:

    def __init__(self, email, password=None):
        self.token = None
        self.tokenAuth = None
        self.email = None
        self.password = None
        self.username=None
        self.Tokens=None

        if password is None:
            self.token = mysqlclean(email)
            self.tokenAuth = True
        else:
            self.email = mysqlclean(email)
            self.password = mysqlclean(password)

        if self.tokenAuth:
            self.authenticate()

        else:
            x=Users.find_one({"email": self.email})
            if x is not None:
                if self.password==x['Password']:
                    self.username=x['username']
                    self.Tokens=self.addsession()
                else:
                    raise Exception('Password Mismatch')
            else:
                raise Exception('User Not Found')

    def addsession(self):
        username = self.username
        a=Sessions.find_one({'username': username,'active':1})
        if a:
            userid= a['_id']
            if self.deactivate(userid):
                token=self.newsession(username)
                if token:
                    return token
                else:
                    raise Exception('Unable to add Session')
        else:
            token=self.newsession(username)
            if token:
                return token
            else:
                raise Exception('Unable to add Session')

    def deactivate(self,con):
        # print(con)
        condition = {'_id': con}
        new = {"$set": {'active': 0}}
        if Sessions.update_one(condition, new):
            return True
        else:
            return False

    def newsession(self,username):
        self.accesstoken=self.tokengen(16)
        data={
            'username':username,
            'token':self.accesstoken,
            'created':int(time.time()),
            'active':1,
            'validity':60
        }

        if Sessions.insert_one(data):

            return self.accesstoken
        else:
            return False


    def tokengen(self,num):
        return  secrets.token_hex(num)

    def getdata(self):
        data ={
            'Username':self.username,
            'Email':self.email,
            'Token':self.Tokens
        }
        return data

    def authenticate(self):
        token=self.token
        a=Sessions.find_one({'token':token})
        if a:
            username=a['username']
            created_at=a['created']
            expiry=a['validity']
            current=time.time()
            if current<created_at+expiry:

                return True
            else:
                return False
        else:
            return False

    def valid_for_token(self):
        token=self.token
        a=Sessions.find_one({'token':token,'active':1})
        if a:
            return (a['created']+a['validity'])-time.time()
        else:
            return False






