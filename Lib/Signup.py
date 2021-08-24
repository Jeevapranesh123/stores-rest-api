import pymongo

client = pymongo.MongoClient('mongodb+srv://jeeva:DOCKoC2kvdHVHmzT@flask-api.atefn.mongodb.net/test')
db=client.API
Users=db.Users


class Signup:

    def __init__(self):
        pass

    def createuser(self, username,email, password):
        data = {
            'username':username,
            'email': email,
            'Password': password
        }
        a = Users.find()
        # print(a)
        for i in a:
            # print(i)
            if i['email'] == email:
                print('Email already exists')
                return False
        else:
            Users.insert_one(data)
            return True

    def verifytoken(self,username,password):
        pass




