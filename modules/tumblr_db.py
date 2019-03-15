from pymongo import MongoClient
from modules.tumblrEmail import EmailChecker
from config import Config


class ProfileExistence:

    def __init__(self):

        self.client = MongoClient(Config.DATABASE_CONFIG['host'], Config.DATABASE_CONFIG['port'])
        db = self.client.tumblr_db
        self.collection = db.data
        self.dict = {}

    def db_check(self, emailId):

        # for i in self.collection.find({'num'}):
        #     pprint.pprint(i['num'])

        # if database consists the profile
        if self.collection.find_one({'profile': emailId}):

            for doc in self.collection.find({'profile':  emailId}):
                # print(doc)
                self.dict['profileExists'] = doc['profileExists']
                self.dict['profile'] = doc['profile']

                return self.dict

        # when profile isn't in database
        else:
            obj = EmailChecker()
            data_from_fb = obj.checker(emailId)
            # print(data_from_fb)
            self.db_loader(data_from_fb)
            return data_from_fb

    def db_loader(self, data):

        # print(data)
        if data['profileExists'] is False:
            pass
        else:

            d = {"profileExists": data['profileExists'],
                 "profile": data['profile']
                 }
            self.collection.insert_one(d)

            # close db connection
            self.client.close()

    # pprint.pprint(self.collection.find({'num'}))
    # else:
    #     print('**')
    #     print(self.obj.caller_data(number))

    # print(self.collection.count())
    # pprint.pprint(collection.find_one({}))
    # for i in self.collection.find():
    #     # pprint.pprint(i['num'])
    #     if number == i['num']:
    #         print(i['num'])
    #         return i['result']
    #     else:
    #         return self.obj.caller_data(number)


if __name__ == '__main__':
    obj = ProfileExistence()
    print(obj.db_check(""))

