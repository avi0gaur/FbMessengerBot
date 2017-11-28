from storeState import state_mdb

class UserStateData():

    def __init__(self):
        self.data = {"id": "", "intent_type": "", "user_text": "", 'user_stage': 0, "card_type":""}
        self.db = state_mdb()
        self.updatedb()


    def updatedb(self):
        self.db.insert_user_state(self.data)

