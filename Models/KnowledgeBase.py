from Models.Base import *

class KnowledgeBase(Base):
    id = PrimaryKeyField()
    query = CharField(max_length=255)
    response = TextField()
    text_query = CharField()
