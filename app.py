import os
import json
import requests
from flask import Flask, request

from chat_bot import CrmnextChatBot

app = Flask(__name__)

bot = CrmnextChatBot()

app = Flask(__name__, static_url_path='')

user_stage = 0
intent = ''
reconnect = True

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
                    data = {'userId': '123', "intent_type": intent, "user_text": message_text, 'user_name': 'Avinash Gaur',
                                      'contactNumber': '89892398128', 'cardCount': 2, 'user_stage': user_stage, 're_connect': reconnect}
                    res = bot.run_bot(data)
                    user_stage = res['user_stage']
                    intent = res['user_intent']
                    if intent is not '':
                        reconnect = False
                    else:
                        reconnect = True
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


if __name__ == '__main__':
    app.run(debug=True)
