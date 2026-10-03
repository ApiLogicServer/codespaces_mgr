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
    """description: Customer class with balance and credit limit."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    balance = Column(DECIMAL)
    credit_limit = Column(DECIMAL)

class Order(Base):
    """description: Order class with note field and relationship to Customer."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    notes = Column(String)
    amount_total = Column(DECIMAL)
    date_shipped = Column(DateTime)

class Item(Base):
    """description: Item class referencing Order and Product, with calculated amount."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: Product class with unit price."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
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
    customer1 = Customer(name="Alice", balance=0, credit_limit=10000)
    customer2 = Customer(name="Bob", balance=2500, credit_limit=5000)
    customer3 = Customer(name="Charlie", balance=4500, credit_limit=10000)
    customer4 = Customer(name="Diana", balance=0, credit_limit=3000)
    order1 = Order(customer_id=1, notes="Urgent Delivery", amount_total=0, date_shipped=None)
    order2 = Order(customer_id=2, notes="Standard", amount_total=0, date_shipped=date(2023, 7, 1))
    order3 = Order(customer_id=3, notes="Priority", amount_total=0, date_shipped=None)
    order4 = Order(customer_id=1, notes="Gift", amount_total=0, date_shipped=date(2023, 9, 15))
    item1 = Item(order_id=1, product_id=1, quantity=2, unit_price=50, amount=100)
    item2 = Item(order_id=2, product_id=2, quantity=3, unit_price=30, amount=90)
    item3 = Item(order_id=3, product_id=3, quantity=1, unit_price=70, amount=70)
    item4 = Item(order_id=4, product_id=1, quantity=4, unit_price=50, amount=200)
    product1 = Product(name="Product A", unit_price=50)
    product2 = Product(name="Product B", unit_price=30)
    product3 = Product(name="Product C", unit_price=70)
    product4 = Product(name="Product D", unit_price=100)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
