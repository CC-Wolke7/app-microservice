setx DJANGO_DATABASE_NAME "local"
setx DJANGO_DATABASE_USER "root"
setx DJANGO_DATABASE_PASSWORD ""
setx DJANGO_DATABASE_HOST "127.0.0.1"
setx DJANGO_DATABASE_PORT "3306"

python app_microservice/manage.py runserver
