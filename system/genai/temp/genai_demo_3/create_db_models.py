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
    """description: A class representing a customer, storing credit limit and balance."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL, nullable=False, default=0)

class Order(Base):
    """description: A class representing an order, includes a link to customer and notes."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    notes = Column(String(500))
    amount_total = Column(DECIMAL, default=0)
    date_shipped = Column(Date)

class Item(Base):
    """description: A class representing items within an order, referencing order and product."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL, nullable=False, default=0)

class Product(Base):
    """description: A class representing products available for orders."""
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
    customer1 = Customer(name="Alice", credit_limit=5000, balance=0)
    customer2 = Customer(name="Bob", credit_limit=3000, balance=0)
    customer3 = Customer(name="Charlie", credit_limit=7000, balance=0)
    customer4 = Customer(name="Diana", credit_limit=10000, balance=0)
    order1 = Order(customer_id=1, notes="Urgent", amount_total=0, date_shipped=None)
    order2 = Order(customer_id=2, notes="Important", amount_total=0, date_shipped=date(2023, 10, 2))
    order3 = Order(customer_id=3, notes="Regular", amount_total=0, date_shipped=None)
    order4 = Order(customer_id=4, notes="Express", amount_total=0, date_shipped=date(2023, 9, 15))
    product1 = Product(name="Laptop", unit_price=1200)
    product2 = Product(name="Monitor", unit_price=300)
    product3 = Product(name="Keyboard", unit_price=45)
    product4 = Product(name="Mouse", unit_price=30)
    item1 = Item(order_id=1, product_id=1, quantity=1, unit_price=1200, amount=1200)
    item2 = Item(order_id=2, product_id=2, quantity=3, unit_price=300, amount=900)
    item3 = Item(order_id=3, product_id=3, quantity=4, unit_price=45, amount=180)
    item4 = Item(order_id=4, product_id=4, quantity=5, unit_price=30, amount=150)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, product1, product2, product3, product4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
