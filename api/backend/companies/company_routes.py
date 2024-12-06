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
companies = Blueprint('companies', __name__)

@companies.route('/companies', methods=['GET'])
def get_companies():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, name FROM companies
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companiesSpecific', methods=['GET'])
def get_companiesSpecific():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT 
    c.name AS CompanyName,
                   c.id as id,
    AVG(r.rating) AS AverageRating
FROM 
    reviews r
JOIN 
    job_posting jp ON r.jobId = jp.id
JOIN 
    companies c ON jp.companyId = c.id
GROUP BY 
    c.name, jp.companyId
ORDER BY 
    averageRating DESC;''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT
    students.id AS StudentId, 
    students.firstName AS FirstName,
    students.lastName AS LastName,
    reviews.title AS ReviewTitle,
    reviews.content AS ReviewContent,
    reviews.rating
FROM 
    reviews
JOIN 
    job_posting ON reviews.jobId = job_posting.id
JOIN 
    companies ON job_posting.companyId = companies.id
JOIN 
    students ON reviews.studentId = students.id
WHERE companies.id = %s''', (company_id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companies/<company_id>/count_applicants', methods=['GET'])
def get_company_count_applicants(company_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT 
    COUNT(DISTINCT ja.studentId) AS AmountOfApplicants
FROM companies c
JOIN job_posting jp ON c.id = jp.companyId
                   JOIN job_application ja ON jp.id = ja.jobId
WHERE c.id = %s''', (company_id,))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companies/match_description/<key_word>', methods=['GET'])
def get_companies_match_description(key_word):

    cursor = db.get_db().cursor()
    cursor.execute('''
SELECT 
    c.id AS CompanyId,
    c.name AS CompanyName,
                   jp.name AS JobName,
    jp.description AS Description 
FROM companies c
JOIN job_posting jp ON c.id = jp.companyId
WHERE jp.description LIKE %s OR c.name LIKE %s OR jp.location LIKE %s
''', (f"%{key_word}%", f"%{key_word}%", f"%{key_word}%"))

    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companies/avg_gpa_past_employee/<company_id>', methods=['GET'])
def get_companies_avg_gpa_past_employee(company_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT ROUND(AVG(s.gpa), 2) AS AverageGPA, cc.firstName, cc.lastName, cc.phone, cc.email   
                   FROM students s
JOIN reviews r ON s.id = r.studentId
JOIN job_posting jp ON r.jobId = jp.id
JOIN companies c ON jp.companyId = c.id
                   JOIN company_contact cc ON c.id = cc.companyId
WHERE c.id = %s
                   GROUP BY cc.firstName, cc.lastName, cc.phone, cc.email
                ''', (company_id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@companies.route('/companies/avg_rating/<company_id>', methods=['GET'])
def get_companies_avg_rating(company_id):

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT 
                        AVG(r.rating) AS AvgRating
                    FROM
                        reviews r
                    JOIN
                        job_posting jp ON r.jobId = jp.id
                    JOIN
                        companies c ON jp.companyId = c.id
                    WHERE
                        c.id = %s   
                    GROUP BY
                        c.name
                    ''', (company_id,))
    
    theData = cursor.fetchone()

    avg_rating = theData['AvgRating'] if theData else None

    the_response = make_response(jsonify({'AvgRating': avg_rating}))
    the_response.status_code = 200
    return the_response