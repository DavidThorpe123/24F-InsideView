from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

reviews = Blueprint('reviews', __name__)

@reviews.route('/reviews', methods=['GET'])
def get_reviews_last7days():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, content, title, rating, datePosted, studentId, jobId FROM reviews
                   WHERE DATE_SUB(datePosted, INTERVAL 7 DAY) <= CURDATE()
                   ORDER BY datePosted desc''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@reviews.route('/reviews/<review_id>', methods=['PUT'])
def update_review_title(review_id):
    cursor = db.get_db().cursor()
    new_title = request.json['new_title']
    cursor.execute('''UPDATE reviews
                   SET title = %s
                   WHERE id = %s''',
                   new_title, review_id)
    db.get_db().commit()
    the_response = make_response(jsonify('Review title updated'))
    the_response.status_code = 200
    return the_response

@reviews.route('/reviews', methods=['POST'])
def create_review():
    review_data = request.json()
    if not all([review_data.get('studentId'), review_data.get('jobId')]):
        return jsonify({'error': 'Student ID and Job ID are required'}), 400
    stu_id = review_data['studentId']
    college_id = review_data['collegeId']
    cursor = db.get_db().cursor()
    cursor.execute("INSERT INTO reviews (datePosted, studentId, collegeId) VALUES (CURDATE, %s, %s)",
                   (stu_id, college_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Review template created'))
    the_response.status_code = 200
    return the_response

@reviews.route('/reviews/<rev_id>', methods=['DELETE'])
def delete_review(rev_id):
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM reviews WHERE id = %s''', (rev_id))
    db.get_db().commit()
    the_response = make_response(jsonify('Review deleted'))
    the_response.status_code = 200
    return the_response