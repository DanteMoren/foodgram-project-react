## Описание проекта:

* Cайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_data
docker-compose exec web python manage.py createsuperuser