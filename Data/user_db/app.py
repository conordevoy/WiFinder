from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserDBv01.db'

db =SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
	app.run()