from flask_restful import Resource
from flask import request, jsonify

from models import VendingMachineStock, db, VendingMachine


class VendingMachineStockAPI(Resource):
    @staticmethod
    def get(vending_machine_id):
        items = VendingMachineStock.query.filter_by(vending_machine_id=vending_machine_id).all()
        return {'items': [{'name': i.name, 'quantity': i.quantity} for i in items]}

    @staticmethod
    def post(vending_machine_id):
        data = request.json
        for item in data['items']:
            stock = VendingMachineStock(vending_machine_id, item['name'], item['quantity'])
            db.session.add(stock)
        db.session.commit()
        return {'message': 'Stock items added successfully'}, 201

    @staticmethod
    def put(vending_machine_id):
        data = request.json
        for item in data['items']:
            stock = VendingMachineStock.query.filter_by(vending_machine_id=vending_machine_id,
                                                        name=item['name']).first()
            stock.quantity = item['quantity']
        db.session.commit()
        return {'message': 'Stock items updated successfully'}, 200

    @staticmethod
    def delete(vending_machine_id):
        data = request.json
        for item in data['items']:
            VendingMachineStock.query.filter_by(vending_machine_id=vending_machine_id, name=item['name']).delete()
        db.session.commit()
        return {'message': 'Stock items deleted successfully'}, 200


class VendingMachineAPI(Resource):
    @staticmethod
    def get():
        machines = VendingMachine.query.all()
        return jsonify([{'id': m.id, 'location': m.location, 'name': m.name,
                         'stock': [{'product': i.name, 'quantity': i.quantity} for i in m.stock]

                         } for m in
                        machines])

    @staticmethod
    def post():
        data = request.json
        machine = VendingMachine(data['location'], data['name'])
        db.session.add(machine)
        db.session.commit()
        return jsonify({'id': machine.id, 'location': machine.location, 'name': machine.name}), 201
