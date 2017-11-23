from storeState import state_mdb

class UserStateData():

    def __init__(self):
        self.data = { "id": "", "intent_type": "", "user_text": "", 'user_stage': 0 }
        self.db = state_mdb()
        self.updatedb(self.data)


    def updatedb(self, data):
        self.db.update_user_stage(self.data)

