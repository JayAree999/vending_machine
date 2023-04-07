from flask_restful import Resource
from flask import request
from models.model import VendingMachineStock, db, VendingMachine
from sqlalchemy import func


class VendingMachineTimelineAPI(Resource):
    @staticmethod
    def get(vending_machine_id):
        result = db.session.query(
            VendingMachineStock.product_name,
            func.sum(VendingMachineStock.quantity).label("quantity"),
            func.date(VendingMachineStock.timestamp).label("date"),
        ).filter_by(vending_machine_id=vending_machine_id).group_by(
            VendingMachineStock.product_name,
            func.date(VendingMachineStock.timestamp),
        ).all()

        return {
            "timeline": [
                {
                    "product_name": r.product_name,
                    "quantity": float(r.quantity),  # Convert Decimal to float
                    "date": r.date.isoformat(),
                }
                for r in result
            ]
        }

class ProductTimelineAPI(Resource):
    @staticmethod
    def get(product_name):
        result = db.session.query(
            VendingMachineStock.vending_machine_id,
            func.sum(VendingMachineStock.quantity).label("quantity"),
            func.date(VendingMachineStock.timestamp).label("date"),
        ).filter_by(product_name=product_name).group_by(
            VendingMachineStock.vending_machine_id,
            func.date(VendingMachineStock.timestamp),
        ).all()

        return {
            "timeline": [
                {
                    "vending_machine_id": r.vending_machine_id,
                    "quantity": float(r.quantity),  # Convert Decimal to float
                    "date": r.date.isoformat(),
                }
                for r in result
            ]
        }

class VendingMachineStockAPI(Resource):
    @staticmethod
    def get(vending_machine_id):
        items = VendingMachineStock.query.filter_by(
            vending_machine_id=vending_machine_id
        ).all()
        return {"items": [{"name": i.product_name, "quantity": i.quantity} for i in items]}  # Name attribute updated

    @staticmethod
    def post(vending_machine_id):
        data = request.json
        for item in data["items"]:
            stock = VendingMachineStock(
                vending_machine_id, item["name"], item["quantity"], item["price"]
            )
            db.session.add(stock)
        db.session.commit()
        return {"message": "Stock items added successfully"}, 201

    @staticmethod
    def put(vending_machine_id):
        data = request.json
        for item in data["items"]:
            stock = VendingMachineStock.query.filter_by(
                vending_machine_id=vending_machine_id, product_name=item["name"]  # Name attribute updated
            ).first()
            stock.quantity = item["quantity"]
        db.session.commit()
        return {"message": "Stock items updated successfully"}, 200

    @staticmethod
    def delete(vending_machine_id):
        data = request.json
        for item in data["items"]:
            VendingMachineStock.query.filter_by(
                vending_machine_id=vending_machine_id, product_name=item["name"]  # Name attribute updated
            ).delete()
        db.session.commit()
        return {"message": "Stock items deleted successfully"}, 200

class VendingMachineAPI(Resource):
    @staticmethod
    def get():
        machines = VendingMachine.query.all()

        # Print the fetched VendingMachine instances
        print("Fetched machines:", machines)

        return {
            "machines": [
                {
                    "id": m.id,
                    "location": m.location,
                    "name": m.name,
                    "stock": [
                        {"product": i.product_name, "quantity": i.quantity} for i in m.stocks
                    ],
                }
                for m in machines
            ]
        }


    @staticmethod
    def post():
        data = request.json
        machine = VendingMachine(data["location"], data["name"])
        db.session.add(machine)
        db.session.commit()
        return {
            "id": machine.id,
            "location": machine.location,
            "name": machine.name,
        }, 201
