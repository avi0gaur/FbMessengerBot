import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

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
                    send_message(sender_id, "I am saying "+message_text)

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
