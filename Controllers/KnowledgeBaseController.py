from Models.KnowledgeBase import KnowledgeBase
from bcrypt import hashpw,gensalt,checkpw
import hashlib # встроенная библиотека хеширования
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
        data = text_query.encode('utf-8')  # переменной data передаём text_query в формате 'utf-8'
        hash = hashlib.sha256(data).hexdigest()  # хэшируем аргумент text и передаём переменной hash
        result =  KnowledgeBase.get_or_none(KnowledgeBase.query == hash) # result передаю результат поиска ввудённого и превращённого в хэш аргумента text_query - это None/Объект
        print("результат поиска", result)
        if result  is None:
            KnowledgeBase.create(
                query = hash,
                response = response,
                text_query = text_query
            )
    list = []
    @classmethod
    def hash(cls,text):
        data = text.encode('utf-8') # переменной data передаём text в формате 'utf-8'
        hash = hashlib.sha256(data).hexdigest() # хэшируем аргумент text и передаём переменной hash
        print(hash)


    # 982d9e3eb996f559e633f4d194def3761d909f5a3b647d1a851fead67c32c9d1
    @classmethod
    def delete(cls,id):
        KnowledgeBase.delete().where(KnowledgeBase.id == id).execute()
if __name__ == "__main__":
    KnowledgeBaseController.add(
        text_query='Что такое файл ',
        response='это именованная область диска'
    )
    # KnowledgeBaseController.delete(9)
    for row in KnowledgeBaseController.get():
        print(
           row.id,
           row.query,
           row.response,
           row.text_query,
        )
    # KnowledgeBaseController.hash('text-')

