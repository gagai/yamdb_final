![Workflow Status](https://github.com/gagai/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# YaMDb API

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

---
## Заполнение .env файла

Создайте файл .env в папке infra и заполните его по схеме:

```
DB_ENGINE=<путь до базы данных (по умолчанию - django.db.backends.postgresql)>
DB_NAME=<название БД>
POSTGRES_USER=<имя пользователя>
POSTGRES_PASSWORD=<пароль>
DB_HOST=<хост>
DB_PORT=<порт для подключения к БД>
```

---
## Установка

Из директории с файлом docker-compose.yaml

Создать и запустить связанные контейнеры в фоновом режиме
```bash
docker-compose up -d 
```

---
## Управление базами данных

Из директории с файлом docker-compose.yaml

Выполнить миграции
```bash
docker-compose exec web python manage.py migrate
```

Создать суперюзера
```bash
docker-compose exec web python manage.py createsuperuser
```

Собрать статику
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Создать бэкап базы данных в формате json
```bash
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Создать бэкап базы данных в формате dump
```bash

sudo docker exec -i <postgres_container_id> pg_dump postgres -U api_yamdb_user > api_yamdb_backup.dump
```


### Восстановление базы данных

Сохранить бэкап в контейнере
```bash
sudo docker exec <postgres_container_id> mkdir backup
sudo docker cp api_yamdb_backup.dump 012852fadd52:backup
```

Создать новую базу данных
```bash
sudo docker exec -i <postgres_container_id> psql -c 'CREATE DATABASE api_yamdb_2;' -U api_yamdb_user
```

Загрузить бэкап в новую базу данных
```bash
sudo docker exec -i <postgres_container_id> psql -d api_yamdb_2 -f backup/api_yamdb_backup.dump -U api_yamdb_user
```

---
## Алгоритм регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
- Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
- При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
---

## Пользовательские роли

**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

---

## Аутентификация
`jwt-token`

Используется аутентификация с использованием JWT-токенов

---

## Примеры запросов к API:

### Регистрация нового пользователя
```
POST   /api/v1/auth/signup/
```

### Получение JWT-токена
```
POST  /api/v1/auth/token/
```

### Получение списка всех категорий / Добавление новой категории/ Удаление категории
```
GET/POST  /api/v1/categories/
DELETE  /api/v1/categories/{slug}/
```

### Получение списка всех жанров / Добавление жанра / Удаление жанра
```
GET/POST  /api/v1/genres/
DELETE  /api/v1/genres/{slug}/
```

### Получение списка всех произведений / Добавление произведения 
```
GET/POST  /api/v1/titles/
```

### Получение информации / Частичное обновление / Удаление произведения
```
GET/PATCH/DELETE  /api/v1/titles/{titles_id}/
```

### Получение списка всех отзывов / Добавление нового отзыва
```
GET/POST  /api/v1/titles/{title_id}/reviews/)
```

### Полуение/ Частичное обновление/ Удаление отзыва по id
```
GET/PATCH/DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
```

### Получение списка всех комментариев к отзыву / Добавление комментария к отзыву
```
GET/POST  /api/v1/titles/{title_id}/reviews/{review_id}/comments/)
```

### Получение/ Частичное обновление/ Удаление комментария к отзыву
```
GET/PATCH/DELETE  /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

---
## Технологии
- Docker
- Nginx
- Gunicorn
- Django 2.2
- Python 3.7
- Django REST Framework
- ReDoc
