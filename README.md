![yamdb_workflow](https://github.com/Viktrols/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)

# REST API для сервиса YaMDb — базы отзывов
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории (книги, фильмы и тд) Произведению может быть присвоен жанр из списка предустановленных (сказка, драма, артхаус и тд)

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Пользователи оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения. К каждому отзыву можно оставить комментарий.

## Workflow состоит из четырёх шагов:
- Тестирование проекта (flake8 и pytest).
- Сборка и публикация образа на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.

## Подготовка и запуск проекта
### Склонируйте репозиторий на локальную машину:
```
git clone https://github.com/Viktrols/yamdb_final
```
### Выполните вход на свой удаленный сервер

### Установите docker на сервер:
```
sudo apt install docker.io 
```
### Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
### Примените разрешения для исполняемого файла к двоичному файлу:
```
sudo chmod +x /usr/local/bin/docker-compose
```
### Отредактируйте файл nginx/default.conf и в строке server_name впишите свой IP
### Скопируйте файлы docker-compose.yaml и nginx/default.conf из проекта на сервер:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
### Создайте на сервере файл pg.env для работы с контейнером postgres и поместите в него значения переменных окружения (или создайте этот файл локально и скопируйте файл по аналогии с предыдущим пунктом):
```
POSTGRES_PASSWORD=<пароль для базы данных> - обязательный параметр
DB_NAME=<название базы данных> - необязательный параметр (по умолчанию будет postgres)
POSTGRES_USER=<имя пользователя> - необязательный параметр (по умолчанию будет postgres)
```
### Добавьте в Secrets GitHub переменные окружения для работы:
```
SECRET_KEY=<secret key django проекта>
DB_ENGINE=django.db.backends.postgresql
DB_HOST=db
DB_NAME=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DB_USER=postgres

DOCKER_PASSWORD=<Docker password>
DOCKER_USERNAME=<Docker username>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ>

TG_CHAT_ID=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
### После успешного деплоя зайдите на боевой сервер и выполните команды (только после первого деплоя):
#### Собрать статические файлы в STATIC_ROOT:
```
docker-compose exec web python3 manage.py collectstatic --noinput
```
#### Применить миграции:
```
docker-compose exec web python3 manage.py migrate --noinput
```
#### Заполнить базу данных:
```
docker-compose exec web python3 manage.py loaddata fixtures.json
```
#### Создать суперпользователя Django:
```
docker-compose exec web python manage.py createsuperuser
```
### Для ревью проект доступен по адресу http://84.252.139.162/api/v1/
### Документация API http://84.252.139.162/redoc/
### Образ на DockerHub https://hub.docker.com/repository/docker/viktrols/yamdb
