from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from models.model import db  # Import 'db' from your 'models' module

app = Flask(__name__)
from apis.api import VendingMachineStockAPI, VendingMachineAPI, ProductTimelineAPI, VendingMachineTimelineAPI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb'
db.init_app(app)
api = Api(app)
api.add_resource(VendingMachineStockAPI, '/vending-machines/<int:vending_machine_id>/stock')
api.add_resource(VendingMachineAPI, '/vending-machines')
api.add_resource(ProductTimelineAPI, '/products/<string:product_name>/timeline')
api.add_resource(VendingMachineTimelineAPI, '/vending-machines/<int:vending_machine_id>/timeline')

@app.before_first_request
def create_tables():
    db.drop_all()  # Drop all existing tables
    db.create_all()

@app.route('/')
def home():
    return 'Hello, frontend'

if __name__ == "__main__":
    app.run()
