import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

"""ROUTES"""
'''
@TODO implement endpoint
    GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    """Retreive all drinks with short form representation."""
    drinks = Drink.query.all()

    if drinks is None:
        abort(404, 'There is no drinks data.')

    drinks_short = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_short
    }), 200

'''
@TODO implement endpoint
    GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    """Retreive all drinks with long form representation."""
    drinks = Drink.query.all()

    if drinks is None:
        abort(404, 'There is no drinks data.')

    drinks_long = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_long
    }), 200

'''
@TODO implement endpoint
    POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    """Create a new drink."""
    try:
        if request.method != 'GET' and request.method != 'POST':
            abort(405)
        data = request.get_json()
        title = data.get('title')
        recipe = data.get('recipe')

        """Convert recipe into JSON."""
        drink = Drink(title=title, recipe=json.dumps(recipe))

        drink.insert()
    except:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
        db.session.close()

'''
@TODO implement endpoint
    PATCH /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(jwt, drink_id):
    """Update a drink info (title and recipe)."""

    data = request.get_json()
    title = data.get('title')
    recipe = data.get('recipe')

    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404, 'There is no such a drink.')

    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
    except:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
        db.session.close()

'''
@TODO implement endpoint
    DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    """Delete a drink."""
    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404, 'There is no such a drink.')

    try:
        drink.delete()
    except:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'delete': drink_id
        }), 200
        db.session.close()

"""Error Handling"""
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def internal_sever_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(Exception)
def exception_error_handler(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error_handler(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
