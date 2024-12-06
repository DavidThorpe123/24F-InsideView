########################################################
# Sample company blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
students = Blueprint('students', __name__)

@students.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, firstName, lastName, gpa, gradYear, years_exp, resume FROM students
                   WHERE students.id = %s''', (student_id))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@students.route('/students', methods=['GET'])
def get_students():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, phone, firstName, lastName, gpa, gradYear, email, years_exp FROM students
    ''')
    
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

