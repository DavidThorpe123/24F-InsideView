########################################################
# Sample job postings blueprint of endpoints
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
jobPostings = Blueprint('jobPostings', __name__)

@jobPostings.route('/jobPostings/<company_id>', methods=['GET'])
def get_jobPostings(company_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT jp.id, jp.name, jp.description, jp.location, jp.datePosted, cc.firstName, cc.lastName, cc.email, cc.phone
                      FROM job_posting jp
                      JOIN company_contact cc ON jp.contactId = cc.id
                      WHERE jp.companyId = %s''', (company_id,))

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings', methods=['GET'])
def get_jobPostings_last7days():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT jp.id, jp.name, jp.description, jp.location, jp.datePosted, cc.firstName, cc.lastName, cc.email, cc.phone
                   FROM job_posting jp
                   JOIN company_contact cc ON jp.contactId = cc.id
                   WHERE DATE_SUB(jp.datePosted, INTERVAL 7 DAY) <= CURDATE()
                   ORDER BY jp.datePosted DESC''')
    theData = cursor.fetchall() 
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings/reviews/<selected_job_id>', methods=['GET'])
def get_reviews(selected_job_id):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT content, title, rating, datePosted
                      FROM reviews
                      WHERE jobId = %s''', (selected_job_id,))

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# gets the number of applications for a given job posting
@jobPostings.route('/jobPostings/applications/<selected_job_id>', methods=['GET'])
def get_app_count(selected_job_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''SELECT COUNT(job_application.studentId) AS num_apps
                    FROM job_posting  
                    LEFT JOIN job_application ON job_posting.id = job_application.jobId
                    WHERE job_posting.id = %s
                    GROUP BY job_posting.id, job_posting.name''', (selected_job_id,))

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# gets the average rating for a given job posting
@jobPostings.route('/jobPostings/rating/<selected_job_id>', methods=['GET'])
def get_avg_rating(selected_job_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''SELECT AVG(reviews.rating) AS avg_rating
                    FROM job_posting  
                    LEFT JOIN reviews ON job_posting.id = reviews.jobId
                    WHERE job_posting.id = %s
                    GROUP BY job_posting.id, job_posting.name''', (selected_job_id,))

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings/<job_posting_id>', methods=['DELETE'])
def delete_jobPosting(job_posting_id):
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM job_posting WHERE id = %s''', (job_posting_id,))
    db.get_db().commit()

    the_response = make_response(jsonify('Job Posting Deleted'))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings/reviews/<job_posting_id>', methods=['POST'])
def add_review(job_posting_id):
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO students (firstName, middleName, lastName, advisorId, collegeId)
                      VALUES ('Guest', '', 'User', 1, 1)''')
    new_student_id = cursor.lastrowid

    cursor.execute('''INSERT INTO reviews (content, title, rating, studentId, jobId)
                      VALUES (%s, %s, %s, %s, %s)''', 
                   (request.json['content'], request.json['title'], request.json['rating'], new_student_id, job_posting_id))

    db.get_db().commit()

    the_response = make_response(jsonify('Review Added'))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings/reviews/<review_title>', methods=['PUT'])
def update_review(review_title):
    cursor = db.get_db().cursor()
    cursor.execute('''UPDATE reviews
                      SET content = %s
                      WHERE title = %s''', 
                   (request.json['edited_review'], review_title))

    db.get_db().commit()

    the_response = make_response(jsonify('Review Updated'))
    the_response.status_code = 200
    return the_response

@jobPostings.route('/jobPostings/submit_app/<job_posting_id>', methods=['POST'])
def submit_application(job_posting_id):
    cursor = db.get_db().cursor()

    # Check if application already exists for this student
    cursor.execute('''SELECT * FROM job_application WHERE studentId = 4 AND jobId = %s''', (job_posting_id,))
    if cursor.fetchone():
        the_response = make_response(jsonify('Application already submitted'))
        the_response.status_code = 400
        return the_response

    # The fourth student is a Guest. For our purposes, 
    # they are the only one submitting apps (no auth system)
    cursor.execute('''INSERT INTO job_application (studentId, jobId)
                      VALUES (4, %s)''', (job_posting_id,))

    db.get_db().commit()

    the_response = make_response(jsonify('Application Submitted'))
    the_response.status_code = 200
    return the_response
