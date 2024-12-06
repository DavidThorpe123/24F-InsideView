from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

interns_bp = Blueprint('interns_bp', __name__, url_prefix='/in')

#get all students
@interns_bp.route('/students', methods=['GET'])
def get_students():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    the_response = make_response(jsonify(students))
    the_response.status_code = 200
    return the_response

#get all job postings
@interns_bp.route('/job_postings', methods=['GET'])
def get_job_postings():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM job_posting')
    job_postings = cursor.fetchall()
    the_response = make_response(jsonify(job_postings))
    the_response.status_code = 200
    return the_response

#get student skills
@interns_bp.route('/students/<int:id>/qualifications', methods=['GET'])
def get_student_qualifications(id):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT s.id, s.firstName, s.lastName, sk.skillName
        FROM students s
        JOIN student_skills ss ON s.id = ss.studentId
        JOIN skills sk ON ss.skillId = sk.id
        WHERE s.id = %s''', 
        (id,))
    skills = cursor.fetchall()
    the_response = make_response(jsonify(skills))
    the_response.status_code = 200
    return the_response

#add new student skill
@interns_bp.route('/students/<int:id>/qualifications', methods=['POST'])
def add_student_skill(id):
    data = request.get_json()
    skill_name = data.get('skillName')

    cursor = db.get_db().cursor()
    
    #check if skill exists
    cursor.execute('SELECT id FROM skills WHERE skillName = %s', (skill_name,))
    skill = cursor.fetchone()
    if not skill:
        cursor.execute('INSERT INTO skills (skillName) VALUES (%s)', (skill_name,))
        db.get_db().commit()
        skill_id = cursor.lastrowid
    else:
        skill_id = skill['id']

    #add skill to student
    cursor.execute('INSERT INTO student_skills (studentId, skillId) VALUES (%s, %s)', (id, skill_id))
    db.get_db().commit()

    the_response = make_response(jsonify({'message': f'Skill "{skill_name}" added to student {id}'}))
    the_response.status_code = 201
    return the_response

#delete a student's skill
@interns_bp.route('/students/<int:student_id>/qualifications/<int:skill_id>', methods=['DELETE'])
def delete_student_skill(student_id, skill_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM student_skills WHERE studentId = %s AND skillId = %s', (student_id, skill_id))
    db.get_db().commit()

    the_response = make_response(jsonify({'message': f'Skill with ID {skill_id} removed from student {student_id}'}))
    the_response.status_code = 204
    return the_response

#compare student qualifications by company
@interns_bp.route('/qualifications/comparison', methods=['GET'])
def compare_intern_qualifications():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''SELECT c.name AS companyName, sk.skillName, COUNT(DISTINCT s.id) AS numInternsWithSkill
            FROM companies c
            JOIN reviews r ON c.id = r.jobId
            JOIN students s ON r.studentId = s.id 
            JOIN student_skills ss ON s.id = ss.studentId
            JOIN skills sk ON ss.skillId = sk.id
            GROUP BY c.name, sk.skillName
            ORDER BY c.name, sk.skillName''')
        comparison_data = cursor.fetchall()
        the_response = make_response(jsonify(comparison_data))
        the_response.status_code = 200
        return the_response
    except Exception as e:
        logger.error(f"Error while fetching qualifications comparison: {e}")
        return make_response(jsonify({"error": "Internal server error"}), 500)
