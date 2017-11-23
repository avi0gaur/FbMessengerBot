from pymongo import MongoClient

from chat_logger import BotLogger


__author__ = 'avi0gaur'

log = BotLogger()

class state_mdb:

    def __init__(self):

        try:
            client = MongoClient("mongodb://avi0gaur:avi123123@ds027295.mlab.com:27295/chatbot")

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
            self.db.user_state.insert_one(
                cr
               )
            print('\nInserted data successfully\n')
        except Exception as e:
            log.log_error(e)



    def get_corpus(self, k):
        """
        Def to search based on uuid or session id of user for that instance.
        Take care we are searching for updating state of user based on current conversation.
        :param cr:
        :return:
        """
        try:
          cr = self.db.chat_corpus.distinct(k)
        except Exception as e:
            log.log_error(e)
        return cr

    def get_user_state(self, id):
        """
        Def to search based on uuid or session id of user for that instance.
        Take care we are searching for updating state of user based on current conversation.
        :param cr:
        :return:
        """
        try:
          cr = self.db.user_stage.find({"id":id})
        except Exception as e:
            log.log_error(e)
        return cr

    def update_user_stage(self, key, value, data):
        """
        provide json part with elements data need to update with desired user id/uuid/sessionID
        :param str_upd:
        :param uuid:
        :return:
        """
        try:
            self.db.user_stage.update(
                {
                    key: value
                }, data,
                {upsert: true}
            )
        except Exception as e:
            print(e)
        print("\nRecords updated successfully\n")

    def delete(self, cr):
        try:
            self.db.chatbot.delete_many({"id": cr})
            print('\nDeletion successful\n')
        except Exception as e:
            print(e)

