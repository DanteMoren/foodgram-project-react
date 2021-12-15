# praktikum_new_diplom
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py load_data
docker-compose exec web python manage.py createsuperuser