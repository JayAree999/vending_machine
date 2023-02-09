from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class VendingMachine(db.Model):
    __tablename__ = "vending_machine"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    stock = db.relationship("VendingMachineStock", backref="vending_machine", lazy=True)

    def __init__(self, location, name):
        self.location = location
        self.name = name


class VendingMachineStock(db.Model):
    __tablename__ = "vending_machine_stock"
    id = db.Column(db.Integer, primary_key=True)
    vending_machine_id = db.Column(
        db.Integer, db.ForeignKey("vending_machine.id"), nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, vending_machine_id, name, quantity):
        self.vending_machine_id = vending_machine_id
        self.name = name
        self.quantity = quantity
