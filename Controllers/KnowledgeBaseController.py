from Models.KnowledgeBase import KnowledgeBase
from bcrypt import hashpw,gensalt,checkpw
import hashlib
class KnowledgeBaseController:
    '''
        Создание записей в таблицу База знаний
    '''
    @classmethod
    def get(cls):
        return KnowledgeBase.select()
    @classmethod
    def add(cls,text_query,response):
        '''

        :param query: запрос от пользователя в базу знаний, должен быть захэширован
        :param response: ответ - текст ответа, пока записываю вручную, потом с помощью нейросети
        :param text_query: запрос в виде текста
        :return:

        '''

        hech_query = hashpw(text_query.encode('utf-8'), gensalt())
        KnowledgeBase.create(
            query = hech_query,
            response = response,
            text_query = text_query
        )
    @classmethod
    def delete(cls,id):
        KnowledgeBase.delete().where(KnowledgeBase.id == id).execute()
if __name__ == "__main__":
    KnowledgeBaseController.add(
        text_query='Что такое файл',
        response='это именованная область диска'
    )
    for row in KnowledgeBaseController.get():
        print(
           row.id,
           row.query,
           row.response,
           row.text_query,
        )
    # KnowledgeBaseController.delete(4)
