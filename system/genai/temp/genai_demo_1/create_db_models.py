# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Customer(Base):
    """description: Represents a customer in the system with their balance and credit limit."""
    __tablename__ = 'customer'
    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String(100))
    balance = Column(DECIMAL, default=0)
    credit_limit = Column(DECIMAL)

class Order(Base):
    """description: Represents an order placed by a customer, with details such as total amount, shipping date, and notes."""
    __tablename__ = 'order'
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    amount_total = Column(DECIMAL, default=0)
    notes = Column(String(500))
    date_shipped = Column(DateTime)

class Item(Base):
    """description: Represents an item in an order, including the quantity and unit price copied from the associated product."""
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL, default=0)

class Product(Base):
    """description: Represents a product available for sale, with details such as the name and unit price."""
    __tablename__ = 'product'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(200))
    unit_price = Column(DECIMAL)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    customer1 = Customer(id=1, name="Alice", balance=1000, credit_limit=5000)
    customer2 = Customer(id=2, name="Bob", balance=2000, credit_limit=6000)
    customer3 = Customer(id=3, name="Charlie", balance=1500, credit_limit=4000)
    customer4 = Customer(id=4, name="David", balance=2500, credit_limit=5500)
    product1 = Product(id=1, name="Laptop", unit_price=200)
    product2 = Product(id=2, name="Phone", unit_price=100)
    product3 = Product(id=3, name="Tablet", unit_price=150)
    product4 = Product(id=4, name="Monitor", unit_price=250)
    order1 = Order(id=1, customer_id=1, amount_total=0, date_shipped=None, notes="Urgent")
    order2 = Order(id=2, customer_id=2, amount_total=0, date_shipped=None, notes="Normal")
    order3 = Order(id=3, customer_id=3, amount_total=0, date_shipped=None, notes="Express")
    order4 = Order(id=4, customer_id=4, amount_total=0, date_shipped=None, notes="Standard")
    item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=200, amount=400)
    item2 = Item(id=2, order_id=2, product_id=2, quantity=3, unit_price=100, amount=300)
    item3 = Item(id=3, order_id=3, product_id=3, quantity=1, unit_price=150, amount=150)
    item4 = Item(id=4, order_id=4, product_id=4, quantity=5, unit_price=250, amount=1250)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, product1, product2, product3, product4, order1, order2, order3, order4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
