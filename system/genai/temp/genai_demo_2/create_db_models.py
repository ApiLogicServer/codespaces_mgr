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
    """description: Models for customer, order, items, and product."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL)


class Order:
    """description: Models for customer, order, items, and product."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(ForeignKey('customer.id'))
    notes = Column(String)
    date_shipped = Column(DateTime)
    amount_total = Column(DECIMAL)


class Item:
    """description: Models for customer, order, items, and product."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(ForeignKey('order.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL)


class Product:
    """description: Models for customer, order, items, and product."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
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
    customer1 = Customer(id=1, name="John Doe", credit_limit=2000, balance=0)
    customer2 = Customer(id=2, name="Jane Smith", credit_limit=3000, balance=0)
    customer3 = Customer(id=3, name="Alice Johnson", credit_limit=1500, balance=0)
    customer4 = Customer(id=4, name="Bob Brown", credit_limit=5000, balance=0)
    order1 = Order(id=1, customer_id=1, notes="Urgent", date_shipped=None, amount_total=0)
    order2 = Order(id=2, customer_id=2, notes="Next Day", date_shipped=None, amount_total=0)
    order3 = Order(id=3, customer_id=3, notes="Gift Wrap", date_shipped=None, amount_total=0)
    order4 = Order(id=4, customer_id=4, notes="Standard", date_shipped=None, amount_total=0)
    item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=20, amount=0)
    item2 = Item(id=2, order_id=2, product_id=2, quantity=1, unit_price=50, amount=0)
    item3 = Item(id=3, order_id=3, product_id=3, quantity=3, unit_price=30, amount=0)
    item4 = Item(id=4, order_id=4, product_id=4, quantity=4, unit_price=25, amount=0)
    product1 = Product(id=1, name="Laptop", unit_price=100)
    product2 = Product(id=2, name="Headphones", unit_price=50)
    product3 = Product(id=3, name="Monitor", unit_price=150)
    product4 = Product(id=4, name="Mouse", unit_price=30)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
