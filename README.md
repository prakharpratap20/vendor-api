# DJANGO REST API

Django project with a RESTful API using Django REST Framework.

## Prerequisites

- Python(version 3.x recommended)
- Django
- Django REST Framework

## Install Dependencies

- pip3 install django
- pip3 install djangorestframework

## Superuser creation and Token generation

- python manage.py createsuperuser
- curl -X POST -d "username=your_superuser_username&password=your_superuser_password" http://localhost:8000/api-token-auth/

## Run the server

- python manage.py runserver

## Access Django Admin:

Open the Django admin at http://127.0.0.1:8000/admin/ and log in using the superuser credentials. this is to access the database as a admin user.

## how to run a api endpoint:

- first make sure that you migrated the models to database
- start the server using "python manage.py runserver" command.

!(https://github.com/prakharpratap20/vendor-api/blob/main/screenshots/api_token.png?raw=true)

https://github.com/prakharpratap20/vendor-api/blob/main/screenshots/create_vendor.png
