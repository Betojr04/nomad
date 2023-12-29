from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Configure your DB
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!

jwt = JWTManager(app)



# CONFIGURATION FOR SQLITE DATABASE IN DEVELOPMENT MODE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
