from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

admins = Blueprint('admins', __name__)

@admins.route('/system_admins', methods=['GET'])
def get_admins():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, firstName, lastName, email FROM system_admins''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response