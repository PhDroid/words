import urllib

__author__ = 'lynx'

from word import Word

from google.appengine.ext import db
from google.appengine.ext.webapp import RequestHandler
from django.utils import simplejson as json

class SubmitWordHandler(RequestHandler):
    def post(self, *args):
        body = json.loads(self.request.body)

        word = urllib.unquote(body["word"].encode('ascii')).decode('utf8')
        translation = urllib.unquote(body["translation"].encode('ascii')).decode('utf8')
        transcription = urllib.unquote(body["transcription"].encode('ascii')).decode('utf8')
        dictionary = urllib.unquote(body["dictionary"].encode('ascii')).decode('utf8')
        
        entity = Word.gql("where word=:1", word).get()
        if entity is None:
            db.run_in_transaction(self.create_entity, word, dictionary, transcription, translation)
        else:
            db.run_in_transaction(self.update_usages, entity, translation)

    def update_usages(self, entity, translation):
        entity.translation = translation
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


        
