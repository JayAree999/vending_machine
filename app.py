from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb'
db = SQLAlchemy(app)

api = Api(app)


class VendingMachine(db.Model):
    __tablename__ = "vending_machine"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    stock = db.relationship('VendingMachineStock', backref='vending_machine', lazy=True)

    def __init__(self, location, name):
        self.location = location
        self.name = name


class VendingMachineStock(db.Model):
    __tablename__ = "vending_machine_stock"
    id = db.Column(db.Integer, primary_key=True)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, vending_machine_id, name, quantity):
        self.vending_machine_id = vending_machine_id
        self.name = name
        self.quantity = quantity


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


api.add_resource(VendingMachineStockAPI, '/vending-machines/<int:vending_machine_id>/stock')


@app.route('/')
def home():
    return 'Hello, frontend'


@app.route('/vending-machines', methods=['GET', 'POST'])
def vending_machines():
    if request.method == 'GET':
        machines = VendingMachine.query.all()
        return jsonify([{'id': m.id, 'location': m.location, 'name': m.name,
                         'stock': [{'product': i.name, 'quantity': i.quantity} for i in m.stock]

                         } for m in
                        machines])

    elif request.method == 'POST':
        data = request.json
        machine = VendingMachine(data['location'], data['name'])
        db.session.add(machine)
        db.session.commit()
        return jsonify({'id': machine.id, 'location': machine.location, 'name': machine.name}), 201


with app.app_context():
    db.create_all()
