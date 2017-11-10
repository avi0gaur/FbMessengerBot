from state_db import mdb
from nltk.corpus import wordnet as wn
''' Chat corpus to handle request from the user and to generate appropriate response from the bot '''

__author__ = 'avi0gaur'


class BotNextCorpus:

    def __init__(self):
        """
        Init db and load required data
        """
        db = mdb()
        dic = db.get_corpus("bot_data")[0]
        self.chat_data = dic["chat_data"]
        self.train_intent = dic['train_data']['intents']
        self.all_skills = dic['all_skills']
        self.train_intent_list = self.syno(dic['train_data']['intent_list'])

    def syno(self, d):
        """
        Expanding word train model by building list of synonyms
        :param d:
        :return:
        """
        for key in d.keys():
            intent_lst = []
            for synset in wn.synsets(d[key][0]):
                for lemma in synset.lemmas():
                    intent_lst.append(lemma.name())
                d[key] += intent_lst
            return d
