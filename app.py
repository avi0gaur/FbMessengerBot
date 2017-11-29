import os
import json
import requests
from flask import Flask, request

from chat_bot import CrmnextChatBot
from storeState import state_mdb
from user_data import UserStateData
import json

user_db = state_mdb()
user_data = UserStateData()
# user_state = user_data.data
app = Flask(__name__)

bot = CrmnextChatBot()

app = Flask(__name__, static_url_path='')


@app.route('/privacypolicy')
def privacypolicy():
    return app.send_static_file('privacypolicy.html')

@app.route('/termofservice')
def termofservice():
    return app.send_static_file('termofservice.html')

@app.route('/', methods=['POST'])
def fb_webhook():
    """
    To get data from  the user and reponse back
    :return:
    """
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for msg in entry["messaging"]:
                if msg.get("message"):
                    sender_id = msg["sender"]["id"]
                    message_text = msg["message"]["text"]
                    u_data = get_user_state()
                    print("user_state:" + str(u_data))
                    u_state = ''
                    if sender_id in u_data.keys():
                        u_state = u_data[sender_id]
                    else:
                        u_state = u_data["0"]


                    u_state["user_text"] = message_text
                    res = bot.run_bot(u_state)
                    upd_state(sender_id, res, u_data)
                    send_message(sender_id, res['response_text'])

    return "ok", 200


@app.route('/', methods=['GET'])
def v():
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Ready to Rock!", 200

def send_message(recipient_id, message_text):
    """
    build response body to for the user id
    :param recipient_id:
    :param message_text:
    :return:
    """

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def get_user_state():

    return user_db.get_user_state("user_data")[0]

def update_user_data(us):

    return user_db.insert_user_state(us)

def upd_state(id, res, last_state):

    user_state = {"user_data": {id: {"intent_type": "", "user_text": "", "user_stage": 0, "card_type": ""}}}
    user_state = user_state["user_data"]
    user_state[id]["intent_type"] = res["user_intent"]
    user_state[id]["user_stage"] = res["user_stage"]
    user_state[id]["user_text"] = res["response_text"]
    print("update_user_data: " + str(user_state))
    if id in last_state.keys():
        last_state[id] = user_state[id]
        update_user_data(last_state)
    else:
        updated = last_state[id].update(user_state[id])
        update_user_data(updated)

if __name__ == '__main__':
    app.run(debug=True)
