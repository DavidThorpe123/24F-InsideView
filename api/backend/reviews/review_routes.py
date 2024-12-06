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