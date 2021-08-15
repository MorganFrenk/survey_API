#  Survey API App

### Технологии:
- Python 3.8.10
- Django 3.2.6
- Django REST framework 3.12.4
- База данных: PostgreSQL 
- Инструмент тестирования: pytest 6.2.4
- Docker 20.10.7

#### Функционал по ТЗ:
- Пользователи могут создавать опросы.
- Также создавать вопросы к этим опросам, с выбором готовых ответов.
- Пользователи могут отвечать на вопросы.
- Удалять и изменять запросы может только автор.
- Полный набор CRUD действий с вопросами/опросами/ответами.
- Статистика количества ответов.
- Использование API возможно через браузер.
- База данных и приложение запускаются в докер-контейнерах.

### Установка:
* Склонировать репозитарий:
```
https://github.com/MorganFrenk/Trood_test_task.git
```
* Перейти в папку проекта:
```
cd Trood_test_task
```
* Собрать и запустить докер контейнер ('Continue with the new image?' - нажать "y"):
```
docker-compose up --build
```
* Сделать миграции базы данных (при запущенном контейнере):
```
docker-compose exec web python manage.py migrate
```
* Добавить админ-юзера:
```
docker-compose exec web python manage.py createsuperuser
```
* Опционально можно протестировать:
```
docker-compose exec web pytest
```
### Использование
#### Получить токен для аутентификации:
* Получить токен. Метод POST.
```
http://127.0.0.1:8000/api-token-auth/
```
* Body: 
    * username: 
    * password: 
* Пример:
```
curl --location --request POST 'http://127.0.0.1:8000/api-token-auth/' --form 'username=<>' --form 'password=<>'
```

#### Опросы:
_List URL._
```
http://127.0.0.1:8000/api/surveys/
```
_Detail URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/
```
* GET - получение списка всех опросов (_List URL_).
* POST - создание опроса (_List URL_).
* PUT - обновить опрос (_Detail URL_).
* DELETE - удалить опрос (_Detail URL_).
* Header:
   *  Authorization: user token.
* Body:
    * name: название опроса.
    * description: краткое описание.
* Пример создание опроса: 
```
curl --location --request POST 'http://localhost:8000/api/surveys/' \
--header 'Authorization: Token <user token>' \
--form 'name=<>' --form 'description=<>'
```

#### Вопросы:
_List URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/
```
_Detail URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/<question id>/
```
* GET - получение списка всех вопросов указанного опроса (_List URL_).
* POST - создание вопроса (_List URL_).
* PUT - обновить вопрос (_Detail URL_).
* DELETE - удалить вопрос (_Detail URL_).
* Header:
   *  Authorization: user token.
* Body:
    * text: текст вопроса.
* Пример создание вопроса: 
```
curl --location --request POST 'http://localhost:8000/api/surveys/1/questions/' \
--header 'Authorization: Token <user token>' \
--form 'text=<>'
```

#### Варианты ответов:
_List URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/<question id>/choices/
```
_Detail URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/<question id>/choices/<choice id>/
``` 
* GET - получение списка всех вариантов ответа указанного вопроса (_List URL_).
* POST - создание варианта ответа (_List URL_).
* PUT - обновить вариант ответа (_Detail URL_).
* DELETE - удалить вариант ответа (_Detail URL_).
* Header:
   *  Authorization: user token.
* Body:
    * text: текст варианта ответа.
* Пример создания варианта ответа: 
```
curl --location --request POST 'http://localhost:8000/api/surveys/1/questions/1/choices/' \
--header 'Authorization: Token <user token>' \
--form 'text=<>'
```

#### Ответы на вопросы:
_List URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/<question id>/answers/
```
_Detail URL._
```
http://127.0.0.1:8000/api/surveys/<survey id>/questions/<question id>/answers/<answer id>/
```
* GET - получение списка всех ответов указанного вопроса (_List URL_).
* POST - создание ответа (_List URL_).
* PUT - обновить ответ (_Detail URL_).
* DELETE - удалить ответ (_Detail URL_).
* Header:
   *  Authorization: user token.
* Body:
    * choice: id выбранного варианта ответа.
* Пример создания ответа: 
```
curl --location --request POST 'http://localhost:8000/api/surveys/1/questions/1/answers/' \
--header 'Authorization: Token <user token>' \
--form 'choice=<choice id>'
```
