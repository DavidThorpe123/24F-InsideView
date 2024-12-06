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

@students.route('/students/<stu_id>', methods=['PUT'])
def update_student_last_name(stu_id):
    cursor = db.get_db().cursor()
    last_name = request.json['new_last_name']
    cursor.execute('''UPDATE students
                   SET lastName = %s
                   WHERE id = %s''',
                   last_name, stu_id)
    db.get_db().commit()
    the_response = make_response(jsonify('Student last name updated'))
    the_response.status_code = 200
    return the_response

@students.route('/students', methods=['POST'])
def create_student():
    student_data = request.json()
    if not all([student_data.get('advisorId'), student_data.get('collegeId')]):
        return jsonify({'error': 'Advisor ID and College ID are required'}), 400
    advisor_id = student_data['advisorId']
    college_id = student_data['collegeId']
    cursor = db.get_db().cursor()
    cursor.execute("INSERT INTO students (advisorId, collegeId) VALUES (%s, %s)",
                   (advisor_id, college_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Student created successfully'))
    the_response.status_code = 200
    return the_response

@students.route('/students/<stu_id>', methods=['DELETE'])
def kill_student(stu_id):
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM students WHERE id = %s''', (stu_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Student killed'))
    the_response.status_code = 200
    return the_response