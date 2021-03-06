# Дипломный проект Яндекс.Практикум - Foodgram  ![example workflow](https://github.com/DanteMoren/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание:
Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Инструкция к api (после запуска проекта): http://localhost/api/redoc/

### Используемые технологии:
- **Python**
- **Django REST Framework**
- **Docker**
- **PostgreSQL**
- **Nginx**
- **Gunicorn**
- **Git**
- **Djoser (аутентификация на основе токенов)**


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:dantemoren/foodgram-project-react.git
cd foodgram-project-react/
```
Подготовить файл с переменными окружения (описание переменных в .env.template)
```bash
cd infra/
cp .env.template .env
```
Запустите docker-compose и выполните необходимые команды: 
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_data
```
По желанию можно создать суперпользователя (администратора)
```bash
docker-compose exec web python manage.py createsuperuser
```
