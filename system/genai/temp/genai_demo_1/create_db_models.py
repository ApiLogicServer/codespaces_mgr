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
    """description: Model for customer with credit limit and balance"""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL, nullable=False)

class Order(Base):
    """description: Model for orders with reference to customers"""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    notes = Column(String(300))
    date_shipped = Column(DateTime)
    amount_total = Column(DECIMAL, nullable=False)

class Item(Base):
    """description: Model for items linked to orders"""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL, nullable=False)

class Product(Base):
    """description: Model for products with unit price"""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    unit_price = Column(DECIMAL, nullable=False)


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
    customer1 = Customer(id=1, name="Acme Corp", credit_limit=5000, balance=0)
    customer2 = Customer(id=2, name="Globex Corp", credit_limit=10000, balance=0)
    customer3 = Customer(id=3, name="Soylent Corp", credit_limit=8000, balance=0)
    customer4 = Customer(id=4, name="Initech", credit_limit=6000, balance=0)
    order1 = Order(id=1, customer_id=1, notes="Urgent delivery", date_shipped=date(2023, 10, 5), amount_total=0)
    order2 = Order(id=2, customer_id=2, notes="Fragile", date_shipped=None, amount_total=0)
    order3 = Order(id=3, customer_id=3, notes="Gift package", date_shipped=date(2023, 11, 5), amount_total=0)
    order4 = Order(id=4, customer_id=4, notes="Standard delivery", date_shipped=None, amount_total=0)
    product1 = Product(id=1, name="Widget", unit_price=25)
    product2 = Product(id=2, name="Gadget", unit_price=50)
    product3 = Product(id=3, name="Doodad", unit_price=75)
    product4 = Product(id=4, name="Thingamajig", unit_price=100)
    item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=25, amount=50)
    item2 = Item(id=2, order_id=2, product_id=2, quantity=4, unit_price=50, amount=200)
    item3 = Item(id=3, order_id=3, product_id=3, quantity=1, unit_price=75, amount=75)
    item4 = Item(id=4, order_id=4, product_id=4, quantity=3, unit_price=100, amount=300)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, product1, product2, product3, product4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
