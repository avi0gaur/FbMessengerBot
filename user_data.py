from storeState import state_mdb

class UserStateData():

    def __init__(self):
        self.data = {"user_data":[{"0":{ "intent_type": "",
              "user_text": "", "user_stage": 0, "card_type":""
    }

}]
}
        self.db = state_mdb()
        self.updatedb()


    def updatedb(self):
        print("Inside UpdatedB: "+ self.data)
        self.db.insert_user_state(self.data)

