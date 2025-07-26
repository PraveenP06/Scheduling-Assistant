from models.activity_models import Activity 
from extensions import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from routes.activity_routes import activity_bp
import os


load_dotenv()
app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
print("DATABASE_URL =", os.getenv("DATABASE_URL"))

db.init_app(app)
app.register_blueprint(activity_bp)

with app.app_context():
    db.create_all()
    print("Database tables created or already exist.")
if __name__ == '__main__':
    app.run(debug=True)
