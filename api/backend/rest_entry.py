from flask import Flask

from backend.db_connection import db
from backend.customers.customer_routes import customers
from backend.products.products_routes import products
from backend.simple.simple_routes import simple_routes
from backend.companies.company_routes import companies
from backend.commonQuestions.commonQuestions_routes import commonQuestions
from backend.interns.interns import interns_bp
from backend.jobPostings.jobPostings_routes import jobPostings
# from backend.interns import interns
from backend.students.student_routes import students
<<<<<<< HEAD
from backend.reviews.review_routes import reviews
=======
from backend.sysAdmins.admin_routes import admins

>>>>>>> main
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(simple_routes)
    app.register_blueprint(companies,   url_prefix='/co')
    app.register_blueprint(commonQuestions, url_prefix='/cq')
    app.register_blueprint(interns_bp, url_prefix='/in')
    app.register_blueprint(jobPostings, url_prefix='/jp')
    app.register_blueprint(students, url_prefix='/st')
<<<<<<< HEAD
    app.register_blueprint(reviews, url_prefix='/rv')
=======
    app.register_blueprint(admins, url_prefix='/ad')
>>>>>>> main
    # app.register_blueprint(interns, url_prefix='/in')

    
    # Don't forget to return the app object
    return app

