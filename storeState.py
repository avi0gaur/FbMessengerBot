from pymongo import MongoClient

from chat_logger import BotLogger


__author__ = 'avi0gaur'

log = BotLogger()

class state_mdb:

    def __init__(self):

        try:
            client = MongoClient("mongodb://:@ds027295.mlab.com:27295/chatbot")

            self.db = client.chatbot
        except Exception as ex:
            log.log_error(ex)

    def insert_user_state(self, cr):
        """
        Def to insert data into db with user state
        :param cr:
        :return:
        """
        try:
            self.delete_col()
            self.db.user_state.insert_one(
                cr
               )
            print("Inside insert_user_state "+ str(cr))
            print('\nInserted data successfully\n')
        except Exception as e:
            log.log_error(e)

    def delete_col(self):
        try:
            self.db.user_state.delete_many({})
        except Exception as e:
            print(e)

    def get_user_state(self, k):
        """
        Def to load bot corpus from db
        :param k, db:
        :return:
        """
        try:
            cr = self.db.user_state.distinct(k)
            print("Inside get_User_state: " + str(cr))
        except Exception as e:
            print(e)
        return cr

    def update_user_stage(self, key, value, data):
        """
        provide json part with elements data need to update with desired user id/uuid/sessionID
        :param str_upd:
        :param uuid:
        :return:
        """
        try:
            print("update_user_stage: >>"+data)
            self.db.user_state.update_one(
                {
                    key: value
                }, {'$set': data
            }, upsert=True)
        except Exception as e:
            print(e)
        print("\nRecords updated successfully\n")

    def delete(self, cr):
        try:
            self.db.chatbot.delete_many({"id": cr})
            print('\nDeletion successful\n')
        except Exception as e:
            print(e)

