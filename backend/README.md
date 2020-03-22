# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## Error Handling

Errors are returned as JSON objects in the following formats:

```
{
    'success': False,
    'error': 400,
    'message': "bad request"
}

or

{
    'code': 'unauthorized',
    'description': 'Permission not found.'
}
```

The API will return five error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Sever Error

## Endpoints

### GET /drinks

- General: Retrieve all drinks.
    - Permission: Public
    - Request Arguments: None.
    - Return: success value and a list of drinks with short form representation.
- Sample: `{{host}}/drinks`
    - Please use postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

### GET /drinks-detail

- General: Retrieve all drinks.
    - Permission: Barista and Manager
    - Request Arguments: JWT token.
    - Return: success value and a list of drinks with long form representation.
- Sample: `{{host}}/drinks-detail`
    - Please use postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

### POST /drinks

- General: Create a new drink.
    - Permission: Manager
    - Request Arguments: JWT token.
    - Return: success value and a dictionary of the created drink with long form representation.
- Sample: `{{host}}/drinks`
    - Please use postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json
```
{
    "drinks": {
        "id": null,
        "recipe": [
            {
                "color": "blue",
                "name": "Water",
                "parts": 1
            }
        ],
        "title": "Water3"
    },
    "success": true
}
```

### PATCH /drinks/{drinks_id}

- General: Update drink using a drink ID.
    - Permission: Manager
    - Request Arguments: JWT token and an ID of a drink to update.
    - Return: success value and a list of the updated drink with long form representation.
- Sample: `{{host}}/drinks/1`
    - Please use postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": null,
            "title": "Water5"
        }
    ],
    "success": true
}
```

### DELETE /drinks/{drinks_id}

- General: Delete drink using a drink ID.
    - Permission: Manager
    - Request Arguments: JWT token and an ID of a drink to delete.
    - Return: success value and the ID of a deleted drink.
- Sample: `{{host}}/drinks/1`
    - Please use postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json
```
{
    "delete": 1,
    "success": true
}
```
