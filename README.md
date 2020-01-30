# django-example

## The problem
1. Administrators of the app should authenticate using a Google account
2. Administrators should be able to create, read, update and delete users
3. Manipulation operations on a user must be restricted to the administrator who created them
4. PostgreSQL as the database backend
5. Python 3.x as programming language
6. The less javascript possible

## Web app
The web app is a html, with the less javascript possible.
Backend is a Django application.

## The API
The API for the users manipulation is implemented using Django Rest Framework.

## Endopoints
API need to be consumed from a web application with forms, forms doesn't allow DELETE and PUT methods.

[In HTML forms, the only CRUD methods we can use are GET and POST](https://www.w3.org/TR/html52/sec-forms.html#element-attrdef-form-method)

That means that we need to implement some endpoints for the web app:

Creation from web app
* /v1/api/user/**create** [POST]

Deletion from web app
* /v1/api/user/<identifier>/**delete** [POST]

## The admins
The administrator login are made with social login.

They are created as part of the django staff, that's it, they are allowed to do login into the django admin app, but they only can view another admins, they can't create, modify or delete another admins or users.

## Configuration:
In docker-compose you need to configure the next environment variables with your own google app values:
* SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
* SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

## Run the web application
```bash
docker-compose build
docker-compose up -d
```

Go to your browser and request that URL:

[http://localhost:8000](http://localhost:8000)

Once you finish, detach with Ctrl + C and stop containers with the next command:
```bash
docker-compose stop
```

## Test
To run tests, execute next commands in a shell:

```bash
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up
```

Once the tests are finished, detach with Ctrl + C and stop containers with the next command:
```bash
docker-compose -f docker-compose.test.yml stop
```

Tests install pytest, that is placed in requirements_tests.txt, to not to install testing dependencies into the production container.

Pytest settings can be found in pytest.ini