import json
import random
import re

from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from chat_logger import BotLogger
from Corpus import BotNextCorpus

__author__ = 'avi0gaur'


class CrmnextChatBot:

    def __init__(self):
        """
        Init for logger Intent engine Corpus
        """
        self.engine = IntentDeterminationEngine()
        self.bot = BotLogger()
        self.cr = BotNextCorpus()
        self.first_time = True
        self.intent = []
        self.train_data = {'intent': "", 'user_text': "", 'bot_response': ""}
        self.train_intent()
        self.senti = SentimentIntensityAnalyzer()

    def train_intent(self):
        """
        Training intent engine to classify text intent
        :return:
        """
        for k in self.cr.train_intent_list.keys():
            for w in self.cr.train_intent_list[k]:
                self.engine.register_entity(w, k)

        for w in self.cr.train_intent.keys():
            self.intent.append(IntentBuilder(w) \
                    .require(self.cr.train_intent[w]) \
                    .build())
        for obj in self.intent:
            self.engine.register_intent_parser(obj)

    def run_bot(self, conv):
        """
        Thread starts from here.
        :return:
        """
        self.bot.log_debug("Received Json in run_bot: {}".format(conv))
        msg = conv["user_text"]
        isFirst = True if conv["intent_type"] == "" else False

        if self.sent(msg):
            if isFirst:
                try:
                    intent = json.loads(self.intent_parser(msg))
                except Exception:
                    intent = {
                            "intent_type": "",
                            "Card": "",
                            "CardLost": "",
                            "target": "",
                            "confidence": 0.0
                            }
                conv["intent_type"] = intent["intent_type"]
                return self.p_flow(self.cr.chat_data, conv)
            else:
                return self.p_flow(self.cr.chat_data, conv)
        else:
            return self.neg_res(self.cr.chat_data, conv)

    def intent_parser(self, conv):
        """
        Method to get intent of user text.
        :param conv: user data
        :return:
        """
        for intent in self.engine.determine_intent(conv):
            if intent.get('confidence') > 0:
                return json.dumps(intent, indent=4)
            else:
                pass

    def p_flow(self, corpus, ud):
        """
        Method to implement process for user.
        :param corpus: It provides data for chatbot
        :param ud: User related data.
        :return: response
        """
        response = dict(userId="123", user_intent="", response_text="", card_type="",
                        recommendation=[],entities=[],user_stage=0)

        self.bot.log_debug("User Data: {}".format(ud))
        p_data = corpus[ud['intent_type']][ud['user_stage']]
        user_txt = self.clean_text(ud['user_text'])
        if user_txt in p_data.keys():
            response['response_text'] = random.choice(p_data[user_txt])
            response['card_type'] = ""

        elif user_txt in p_data['user_text']:
            print("p_data: >>" + str(p_data))
            response = self.update_res(response, p_data)

        elif user_txt == 'quit':
            q_data = corpus['EXIT'][0]
            response['user_intent'] = q_data['intent_type']
            response['user_stage'] = q_data['user_stage']
            response['response_text'] = random.choice(q_data['response'])
            response['card_type'] = q_data['card_type']

        else:
            self.build_train_cr(ud)
            if 'default_speech' in p_data.keys() and p_data['default_speech'] is not '':
                response['response_text'] = random.choice(p_data['default_speech'])
            else:
                response['response_text'] = "Please select below option to move forward"
            response['card_type'] = "#IntentOptions"
            response['user_stage'] = ud['user_stage']
            response['user_intent'] = ud['intent_type']
            if len(p_data['recommendation']) == 0:
                response['recommendation'] = self.cr.all_skills
            else:
                response['recommendation'] = p_data['recommendation']
        print("response: "+str(response))
        return response

    def update_res(self, response, p_data):
        """
        :param response:
        :param p_data:
        :return:
        """
        response['response_text'] = random.choice(p_data['response'])
        response['user_intent'] = p_data['intent_type']
        response['card_type'] = p_data['card_type']
        response['user_stage'] = p_data['user_stage']
        response['entities'] = p_data['entities']

        return response

    def neg_res(self, cr_data, conv):
        """
        Generate response if sentiment is -ve
        :param cr_data:
        :param conv:
        :return:
        """
        neg_data = cr_data["neg_sent"][0]
        return dict(user_intent="", response_text=random.choice(neg_data["response"]),user_stage=0, card_type='', recommendation=[])

    def sent(self, conv):
        """
        Polarity is considered pos if > -0.2 (for tuning our scenario)
        :param conv:
        :return:
        """
        t = TextBlob(conv)
        vs = self.senti.polarity_scores(conv)
        return False if t.polarity < - 0.3 else True

    def clean_text(self, statement):
        """
        Remove any consecutive whitespace characters from the statement text.
        """
        return re.sub(r'[^a-zA-Z0-9 ]', r'', statement).rstrip().lower()

    def build_train_cr(self, ud):
        intent = ud['intent_type']
        if intent is not '':
            self.train_data['intent'] = intent
            self.train_data['user_text'] = ud['user_text']
        else:
            self.train_data['intent'] = ""
            self.train_data['user_text'] = ud['user_text']

        with open('train_data.json', 'a') as f:
            json.dump(self.train_data, f, indent=True)





# bot = CrmnextChatBot()
# user_stage = 0
# intent = ''
# print(bot.clean_text("Hi I am #avinash ?  "))
# while True:
#
#     text = input("Enter text: ")
#     reconnect = input('re-connect: ')
#     print(bool(reconnect))
#     data = {'userId': '123', "intent_type":intent, "user_text": text, 'user_name': 'Avinash Gaur',
#             'contactNumber': '89892398128', 'cardCount': 2, 'user_stage': user_stage, 're_connect': bool(reconnect)}
#     print(data)
#     print(user_stage)
#     print(intent)
#     d = bot.run_bot(data)
#     intent = d['user_intent']
#     user_stage = d['user_stage']
#
#
#     print(d)