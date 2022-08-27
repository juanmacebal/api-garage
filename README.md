# API Garage
This project create a simple API for a garage just for learning purpose, using:
- Auth JWT with [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)
- Query filters with [django-filter](https://github.com/carltongibson/django-filter)
- Swagger with [drf-spectacular](https://github.com/tfranzel/drf-spectacular)
- Testing and [coverage](https://github.com/nedbat/coveragepy)
- Standarized errors with [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors)
- Code verification with [Flake8](https://github.com/pycqa/flake8) 

## Install
- First install and run [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Go to the project folder ```cd api-garage```
- Run the command ```docker-compose up```
- Run migrations, open the web container terminal and run: ```python manage.py migrate```
- Create super user, open the web container terminal and run ```python manage.py createsuperuser```
- Open the admin [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Add or remove packages
After add or remove a package in Pipfile run the following command to build Pipfile.lock.

```pipenv lock```

Update the container

```docker-compose build```

## Extra documentation
- Oficial Django documentation [docs.djangoproject.com](https://docs.djangoproject.com/en/4.1/) 
- Oficial DRF documentation [django-rest-framework.org](https://www.django-rest-framework.org/) 
- Detailed descriptions, with full methods and attributes [cdrf.com](https://www.cdrf.co/)
- Effectively Using Django REST Framework Serializers [testdriven.io/blog/drf-serializers](https://testdriven.io/blog/drf-serializers/)


## Tests

Run the tests checking the coverage and generate a html report.

`coverage run --source='.' manage.py test && coverage html`

Look your test report in `/htmlcov/index.html`
