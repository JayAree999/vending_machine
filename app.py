from flask import Flask
from flask_restful import Api

from api.api import VendingMachineStockAPI, VendingMachineAPI
from model.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb'
db.init_app(app)
api = Api(app)
api.add_resource(VendingMachineStockAPI, '/vending-machines/<int:vending_machine_id>/stock')
api.add_resource(VendingMachineAPI, '/vending-machines')


@app.route('/')
def home():
    return 'Hello, frontend'


if __name__ == "__main__":
    app.run()
