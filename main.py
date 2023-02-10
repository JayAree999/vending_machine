import pymysql
from flask import Flask
from flask_restful import Api

from apis.api import VendingMachineAPI, VendingMachineStockAPI
from models.model import db

pymysql.connect(user="root", passwd="mypassword", host="localhost", port=3306)


def create_app():
    app = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb"

    app.config.update(
        {
            "TESTING": True,
        }
    )
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.add_resource(
        VendingMachineStockAPI, "/vending-machines/<int:vending_machine_id>/stock"
    )
    api.add_resource(VendingMachineAPI, "/vending-machines")
    return app
