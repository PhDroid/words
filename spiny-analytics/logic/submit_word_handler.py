__author__ = 'lynx'

from word import Word

from google.appengine.ext import db
from google.appengine.ext.webapp import RequestHandler

class SubmitWordHandler(RequestHandler):
    def post(self, *args):
        word = self.request.get("word")
        translation = self.request.get("translation")
        transcription = self.request.get("transcription")
        dictionary = self.request.get("dictionary")

        entity = Word.gql("where word=:1", word).get()
        if entity is None:
            db.run_in_transaction(self.create_entity, word, dictionary, transcription, translation)
        else:
            db.run_in_transaction(self.update_usages, entity)

    def update_usages(self, entity):
        entity.usages += 1
        entity.put()

    def create_entity(self, word, dictionary, transcription, translation):
        entity = Word()
        entity.word = word
        entity.transcription = transcription
        entity.translation = translation
        entity.dictionary = dictionary
        entity.usages = 1
        entity.put()


        
