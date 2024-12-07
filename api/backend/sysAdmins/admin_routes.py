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

@admins.route('/system_admins', methods=['POST'])
def new_empty_admin():
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO system_admins DEFAULT VALUES''')
    db.get_db().commit()
    the_response = make_response(jsonify('New Blank Admin Created'))
    the_response.status_code = 200
    return the_response

@admins.route('/system_admins', methods=['PUT'])
def update_admin_last_name(new_last_name, admin_id):
    cursor = db.get_db().cursor()
    cursor.execute('''UPDATE system_admins
                   SET lastName = %s
                   WHERE id = %s''',
                   new_last_name, admin_id)
    db.get_db().commit()
    the_response = make_response(jsonify('Last name updated'))
    the_response.status_code = 200
    return the_response

@admins.route('/system_admins', methods=['DELETE'])
def delete_admin(admin_id):
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM system_admins WHERE id = %s''', (admin_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Admin Killed'))
    the_response.status_code = 200
    return the_response

@admins.route('/system_admins/<admin_id>', methods=['PUT'])
def update_admin_id(admin_id):
    new_id = request.json.get('id')
    cursor = db.get_db().cursor()
    cursor.execute('''UPDATE system_admins
                      SET id = %s
                      WHERE id = %s''',
                   (new_id, admin_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Admin ID updated'))
    the_response.status_code = 200
    return the_response
