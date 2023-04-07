from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class VendingMachine(db.Model):
    __tablename__ = 'vending_machines'

    id = Column(Integer, primary_key=True)
    location = Column(String(255), nullable=False)  # Make sure the 'location' attribute is present
    name = Column(String(255), nullable=True)
    stocks = relationship('VendingMachineStock', back_populates='vending_machine')

    def __init__(self, location, name=None):
        self.location = location
        self.name = name

    def __repr__(self):
        return f"<VendingMachine(id={self.id}, location='{self.location}', name='{self.name}')>"


class VendingMachineStock(db.Model):
    __tablename__ = 'vending_machine_stocks'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    vending_machine_id = Column(Integer, ForeignKey('vending_machines.id'), nullable=False)

    vending_machine = relationship('VendingMachine', back_populates='stocks')

    def __init__(self, vending_machine_id, product_name, quantity, price):
        self.vending_machine_id = vending_machine_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<VendingMachineStock(id={self.id}, product_name='{self.product_name}', quantity={self.quantity}, price={self.price}, vending_machine_id={self.vending_machine_id})>"
