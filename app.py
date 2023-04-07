from flask import Flask
from flask_restful import Api
from flask import request
from flask_sqlalchemy import SQLAlchemy
from apis.api import VendingMachineStockAPI, VendingMachineAPI
from models.model import db  # Make sure to import 'db' from your 'models' module

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb'
db.init_app(app)
api = Api(app)
api.add_resource(VendingMachineStockAPI, '/vending-machines/<int:vending_machine_id>/stock')
api.add_resource(VendingMachineAPI, '/vending-machines')

@app.before_first_request
def create_tables():
    db.drop_all()  # Add this line to drop all existing tables
    db.create_all()

@app.route('/')
def home():
    return 'Hello, frontend'

if __name__ == "__main__":
    app.run()