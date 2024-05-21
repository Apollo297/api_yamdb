# api_yamdb

### Описание:
Проект собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». </br>
Реализована самостоятельную регистрацию пользователей с отправкой кода подтверждения на указанный адрес email.

### Цель проекта:
В проекте api_yamdb развиваются навыки работы в команде и использования GitHub для совместной работы над проектом. Используются на практике:

- API интерфейс
- Серилизация при обмене и преодбразовании данных
- Создание моделей с установкой зависимостей между моделями
- Фильтрация, поиск и контроль за вводом данных на примере модуля Follow
- Приложение Postman для тестирования и отладки проекта
- JWT-аутентификация
- Права доступа и сегрегация прав доступа по статусу пользователей
- GitHub

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Apollo297/api_yamdb.git
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

**Импорт csv файлов:**
```
python manage.py import_csv_db
```

**Базовые эндопоинты API:**
```
"auth": "http://127.0.0.1:8000/api/v1/auth/",
"categories": "http://127.0.0.1:8000/api/v1/categories/",
"genres": "http://127.0.0.1:8000/api/v1/genres/",
"genres": "http://127.0.0.1:8000/api/v1/genres/",
"titles": "http://127.0.0.1:8000/api/v1/titles/",
"reviews": "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/",
"comments": "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/",
```

```
После запуска проекта полная документация для API api_yamdb интерфейса
доступна по адресу //127.0.0.1:8000/redoc/ 
```

### Примеры запросов к API:

```
Все запросы направляются на http://127.0.0.1:8000
```

```
POST /auth/signup/

Payload
{
"email": "user@example.com",
"username": "string"
}
Response samples
200400
{
"email": "string",
"username": "string"
}
```


```
POST /titles/{title_id}/reviews/
Payload
{
"text": "string",
"score": 1
}
Response samples
201400
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
```

```
GET /titles/{title_id}/reviews/{review_id}/
Response samples
200
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
```

```
PATCH /titles/{title_id}/reviews/{review_id}/
Request samples
Payload
{
"text": "string",
"score": 1
}
Response samples
200400
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
```
##### Авторы:

Лидер команды. Авторизация и аутентификация, права доступа, пользователи - Алексей Нечепуренко .
https://github.com/Apollo297/

Модели, view для произведений, категорий, жанров, импорт данных из csv файлов - Иван Грибачев.
https://github.com/Elegium

Модели, view для отзывов, комментариев, рейтингов - Евгений Рыбалко.
https://github.com/rybaevg



