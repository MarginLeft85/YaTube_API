# Проект «API для Yatube»
## Описание
Yatube это платформа для организации публичных или корпоративных "Сообществ"
Платформа позволяет пользователям публиковать посты, комментировать посты и подписыватся на авторов. 

Платформа полностью готова к работе и может быть быстро развернута как на внутренних корпоративных ресурсах так и в публичном облаке.

Доступ к платформе осуществляется через REST API

## Использованные технологии
В проекте использованы технологии:

>Python 3.7  
Django 2.2.16  
Django REST framework (DRF) 3.12.4  
Djoser 2.1.0  
Django-filter 22.1  
Django REST framework Simple JWT 4.7.2  
SQLight 3  

По умолчанию при развертывании приложения создается встроенная база данных SQLight, но при необходимости можно использовать стороннюю SQL БД

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```commandline
git clone https://github.com/as-devhub/api_final_yatube.git
```

```commandline
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```commandline
python3 -m venv venv
```

```commandline
source venv/bin/activate
```

```commandline
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```commandline
pip install -r requirements.txt
```

Выполнить миграции:

```commandline
python3 manage.py migrate
```

Запустить проект:

```commandline
python3 manage.py runserver
```
## Описание API

>**Подробное описание API проекта доступно по адресу:** `http://<host>:8000/redoc/` 
или в формате OpenAPI:  
в папке проекта:  
`yatube_api/static/redoc.yaml`  
на GitHub:  
`https://github.com/as-devhub/api_final_yatube/blob/a844543e5ef15d2d693fc1dcc0e2f5f1905111c1/yatube_api/static/redoc.yaml`

### API версия 1 _(текущая)_

#### Доступные эндпоинты
`/api/v1/posts/` Управление публикациями  

Доступные методы
- GET - Получение публикаций
- POST - Создание публикации  

`/api/v1/posts/{id}/` Управление публикацией
- GET - Получение публикации по id
- PUT - Обновление публикации
- PATCH - Частичное обновление публикации
- DEL - Удаление публикации

`/api/v1/posts/{post_id}/comments/` Управление комментариями
- GET - Получение всех комментариев к публикации
- POST - Добавление нового комментария к публикации

`/api/v1/posts/{post_id}/comments/{id}/` Управление коментарием
- GET - Получение комментария к публикации по id.
- PUT - Обновление комментария
- PATCH - Частичное обновление комментария
- DEL - Удаление комментария

`/api/v1/groups/` Список сообществ
- GET - Получение списка доступных сообществ  

`/api/v1/groups/{id}/` Информация о сообществе
- GET - Получение информации о сообществе по id

`/api/v1/follow/` Управление подписками
- GET - Возвращает все подписки пользователя, сделавшего запрос
- POST - Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса

`/api/v1/jwt/` Управление JWT-токенами пользователя
- POST `/api/v1/jwt/create/` - Получение JWT-токена
- POST `/api/v1/jwt/refresh/`- Обновление JWT-токена.
- POST `/api/v1/jwt/verify/`- Проверка JWT-токена

#### Права доступа и безопасность

_Неавторизованный пользователь_ может просматривать следующую информацию:
- Все публикации и детали выбранной публикации
- Комментарии к публикациям 
- Список и подробную информацию о сообществах

_Авторизованный пользователь_ может:
- Просматривать все материал, что и неавторизованный пользователь
- Создавать, а так же редактировать и удалять свои публикации
- Создавать, а так же редактировать и удалять свои комментарии
- Видеть все свои подписки
- Подписываться на другого автора

Управление списком сообществ и пользователями осуществляется через web интерфейс администратора `http://<host>:8000/admin/` 

#### Примеры запросов

Получить список всех публикаций. При указании параметров limit и offset выдача должна работать с пагинацией.  

_Запрос_  
```http request
GET http://127.0.0.1:8000/api/v1/posts/
```

_Ответ  json_
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.  

_Запрос_  
```http request
POST http://127.0.0.1:8000/api/v1/posts/
```
Payload / json:
```json        
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

_Ответ  json_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

Добавление нового комментария к публикации. Анонимные запросы запрещены.  

_Запрос_  
```json
POST http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
Payload / json:
```json
{
  "text": "string"
}
```

_Ответ  json_
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса. Анонимные запросы запрещены.  

_Запрос_  
```json
http://127.0.0.1:8000/api/v1/follow/
```
Payload / json:
```json
{
  "following": "string"
}
```

_Ответ  json_
```json
{
  "user": "string",
  "following": "string"
}
```

Получение JWT-токена  

_Запрос_  
```json
http://127.0.0.1:8000/api/v1/jwt/create/
```
Payload / json:
```json
{
  "username": "string",
  "password": "string"
}
```

_Ответ  json_
```json
{
  "refresh": "string",
  "access": "string"
}
```
--------------------------------------------------------------------------
## Автор
**Андрей Смирнов**   
Студент Яндекс Практикум  
GitHub: `https://github.com/smirnov-andrey/`  