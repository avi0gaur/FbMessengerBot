import os
import json
import requests


class CustomPayload:

    def __init__(self):
        pass

    def quick_reply(self,senderId, res):
        botRes ="Avi hi" #res["response_text"]
        listOfReply = res #res["recommendation"]
        quickReply = []


        for qrly in listOfReply:
            temp = {
                "content_type": "text",
                "title": "",
                "payload": ""
            }
            temp["title"] = qrly
            temp["payload"] = qrly
            quickReply.append(temp)

        msg = {
            "text": botRes,
            "quick_replies": quickReply
        }

        self.send(senderId, msg)


    def normalReply(self, senderId, res):
        temp = {
            "text": res['response_text']
        }

        self.send(senderId, temp)


    def send(self, recipient_id, message_text):

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
            "message": message_text
        })
        return requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers,
                                     data=data)

    def payloadManager(self, senderId, res):
        if len(res["recommendation"]) == 0:
            return self.normalReply(senderId, res)
        else:
           return self.quick_reply(senderId, res)


p = CustomPayload()
# def send_message(senderId, res):
#     return p.payloadManager(senderId, res)
p.quick_reply("1233", ["I want to appply for", "I need to apply for"])