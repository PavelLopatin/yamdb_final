![yamdb_workflow](https://github.com/Viktrols/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)

# REST API для сервиса YaMDb — базы отзывов
Проект построен на фреймворке Django. Дополнительные зависимости перечислены в файле requirements.txt

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

## Workflow состоит из четырёх шагов:
- Тестирование проекта (flake8 и pytest).
- Сборка и публикация образа на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.

## Установка
### Склонируйте репозиторий:
```
git clone https://github.com/PavelLopatin/yamdb_final.git
```
### Установите docker и docker-compose на сервер:
```
sudo apt install docker.io 
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
### После успешного деплоя зайдите на боевой сервер и выполните команды (только после первого деплоя):
#### Собрать статические файлы в STATIC_ROOT:
```
docker-compose exec web python3 manage.py collectstatic --noinput
```
#### Применить миграции:
```
docker-compose exec web python3 manage.py migrate --noinput
```
### Образ на DockerHub https://hub.docker.com/repository/docker/lopatyn1244/yamdb
