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

class Customer:
    """description: Model representing a Customer with an auto-generated ID, name, credit limit, and a derived balance attribute."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    credit_limit = Column(DECIMAL)
    balance = Column(DECIMAL)

class Order:
    """description: Model representing an Order with a relationship back to a Customer, a notes field, and a derived amount total attribute."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    notes = Column(String)
    date_shipped = Column(DateTime, nullable=True)
    amount_total = Column(DECIMAL)

class Item:
    """description: Model representing an Item associated with an Order and Product, with derived amount attribute based on quantity and unit price."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product:
    """description: Model for representing Products with a Product ID, name, and unit price."""
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
    customer1 = Customer(id=1, name='John Doe', credit_limit=Decimal('5000.00'), balance=Decimal('0.00'))
    order1 = Order(id=1, customer_id=1, notes='First Order', date_shipped=None, amount_total=Decimal('0.00'))
    item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=Decimal('20.00'), amount=Decimal('40.00'))
    product1 = Product(id=1, name='Product A', unit_price=Decimal('20.00'))
    
    
    
    session.add_all([customer1, order1, item1, product1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
