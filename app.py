from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@127.0.0.1:3306/mydb'
db = SQLAlchemy(app)


class VendingMachine(db.Model):
    __tablename__ = "vending_machine"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), unique=True)
    stock = db.relationship('VendingMachineStock', backref='vending_machine', lazy=True)
    name = db.Column(db.String(80))

    def __init__(self, location, name):
        self.location = location
        self.name = name

    def update_stock(self):
        # Make a REST API call to get the current stock
        # of the vending machine
        response = request.get(f'https://vending-machine-tracker.com/api/{self.id}/stock')
        data = response.json()

        # Delete the current stock
        VendingMachineStock.query.filter_by(vending_machine_id=self.id).delete()

        # Add the new stock
        for item in data['items']:
            stock = VendingMachineStock(item['name'], item['quantity'], self.id)
            db.session.add(stock)
        db.session.commit()


class VendingMachineStock(db.Model):
    __tablename__ = "vending_machine_stock"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'), nullable=False)

    def __init__(self, name, quantity, vending_machine_id):
        self.name = name
        self.quantity = quantity
        self.vending_machine_id = vending_machine_id


@app.route('/')
def home():
    return 'Hello, frontend'


@app.route('/vending-machines', methods=['GET', 'POST'])
def vending_machines():
    if request.method == 'GET':
        machines = VendingMachine.query.all()
        return jsonify([{'id': m.id, 'location': m.location,
                         'inventory': [{'name': i.name, 'quantity': i.quantity} for i in m.stock]} for m in
                        machines])
    elif request.method == 'POST':
        data = request.json
        machine = VendingMachine(data['location'])
        db.session.add(machine)
        db.session.commit()
        return jsonify({'id': machine.id, 'location': machine.location}), 201


@app.route('/vending-machines/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def vending_machine(id):
    machine = VendingMachine.query.get(id)
    if not machine:
        return jsonify({'error': 'Vending machine not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': machine.id, 'location': machine.location,
                        'inventory': [{'name': i.name, 'quantity': i.quantity} for i in machine.stock]})
    elif request.method == 'PUT':
        data = request.json
        machine.location = data.get('location', machine.location)
        db.session.commit()
        return jsonify({'id': machine.id, 'location': machine.location}), 200

    elif request.method == 'DELETE':
        db.session.delete(machine)
        db.session.commit()
        return jsonify({'message': 'Vending machine deleted'}), 200


@app.route('/vending-machines/int:id/stock', methods=['GET', 'PUT'])
def vending_machine_stock(id):
    machine = VendingMachine.query.get(id)
    if not machine:
        return jsonify({'error': 'Vending machine not found'}), 404
    if request.method == 'GET':
        return jsonify([{'name': i.name, 'quantity': i.quantity} for i in machine.stock])
    elif request.method == 'PUT':
        machine.update_stock()
        return jsonify({'message': 'Inventory updated'}), 200


with app.app_context():
    db.create_all()
