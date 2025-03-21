from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        response = {
            'success': False,
            'error': {
                'code': error.code,
                'name': error.name,
                'description': error.description,
            }
        }
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        response = {
            'success': False,
            'error': {
                'code': 500,
                'name': 'Internal Server Error',
                'description': str(error),
            }
        }
        return jsonify(response), 500
