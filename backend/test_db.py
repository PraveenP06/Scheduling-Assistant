from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Run a basic query to confirm connection
        result = db.session.execute(text('SELECT 1'))
        print("✅ Connection to the database was successful.")
except Exception as e:
    print("❌ Connection failed:")
    print(e)
