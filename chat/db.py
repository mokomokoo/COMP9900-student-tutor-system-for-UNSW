from mongoengine import *
import json
from threading import Lock

#connect('chatbot',username= 'unswAiFriend', #password='unswAiFriend',host='54.252.222.253',port=27017)
# this is the database to store the knowledge-based concept 

# connect to remote mongodb 
connect(
    db='chatbot',
    username='unswAiFriend',
    password='unswAiFriend',
    host='mongodb://unswAiFriend:unswAiFriend@54.252.222.253/chatbot'
)
doc_lock = Lock()

# >>mongo -u unswAiFriend -p unswAiFriend 54.252.222.253/chatbot

# structure of the database: two columns 
# topic | content
class Doc(Document):
    topic = StringField(required=True, primary_key=True)
    content = StringField()

    def __str__(self):
        return self.to_json()
    
    # Return a json for use
    def get_answer(self):
        js = json.loads(self.to_json())
        return js

    # Thread-safe constructor
    @classmethod
    def create_doc(cls, *args, **kwargs):
        # print("cls method")
        doc_lock.acquire()
        # save the record
        doc = cls(*args, **kwargs).save()
        doc_lock.release()
        return doc

