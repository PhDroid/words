__author__ = 'lynx'

from google.appengine.ext import db

class Word(db.Model):
    word = db.StringProperty()
    transcription = db.StringProperty()
    dictionary = db.StringProperty()
    translation = db.TextProperty()
    usages = db.IntegerProperty()