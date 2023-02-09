from flask import Flask
from flask_restful import Api

from apis.api import VendingMachineAPI, VendingMachineStockAPI
from models.model import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.add_resource(VendingMachineStockAPI, "/vending-machines/<int:vending_machine_id>/stock")
    api.add_resource(VendingMachineAPI, "/vending-machines")
    return app
