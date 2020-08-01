# ThingsWeNeedRedefined

This is an attempt of recreating my 2nd semester school project. It is also my first Django based project.

## How to set it up:

Prerequisites: python3, django, django-bootstrap4 and Faker
You can install them using:
```
- Python: https://www.python.org/downloads/
- Django: pip install django
- Bootstrap4: pip install django-bootstrap4
- Faker: pip install Faker
```


Firstly, clone the project
```
https://github.com/Seqrous/ThingsWeNeedRedefined.git
```

Secondly, through a terminal navigate to the ThingsWeNeed folder - the one including *manage.py* script.
Next, run the following commands in the following order:
```
python manage.py makemigrations shopping_app - to create migrations
python manage.py migrate - to apply migrations
python populate.py - to populate the database
python manage.py runserver - to run the server
```

Now, everything should be ready and you can use the app at
```
localhost:8000/login/
```
