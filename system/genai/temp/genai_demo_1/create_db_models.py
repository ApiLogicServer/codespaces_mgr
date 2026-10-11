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
    """description: Customer model storing customer information and derived balance."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)
    credit_limit = Column(Integer)

class Order(Base):
    """description: Order model storing order details, associated with a customer."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    amount_total = Column(Integer)
    date_shipped = Column(DateTime)
    notes = Column(String)

class Item(Base):
    """description: Item model storing items included in an order."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    amount = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Integer)

class Product(Base):
    """description: Product model with information on available products."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_price = Column(Integer)


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
    customer1 = Customer(id=1, name="Customer A", balance=100, credit_limit=1000)
    customer2 = Customer(id=2, name="Customer B", balance=200, credit_limit=500)
    customer3 = Customer(id=3, name="Customer C", balance=300, credit_limit=1200)
    customer4 = Customer(id=4, name="Customer D", balance=400, credit_limit=800)
    order1 = Order(id=1, customer_id=1, amount_total=50, date_shipped=None, notes="First Order")
    order2 = Order(id=2, customer_id=2, amount_total=150, date_shipped=date(2023, 3, 10), notes="Shipped Order")
    order3 = Order(id=3, customer_id=3, amount_total=200, date_shipped=None, notes="Pending Order")
    order4 = Order(id=4, customer_id=4, amount_total=250, date_shipped=None, notes="New Order")
    item1 = Item(id=1, order_id=1, product_id=1, amount=50, quantity=5, unit_price=10)
    item2 = Item(id=2, order_id=1, product_id=2, amount=100, quantity=10, unit_price=10)
    item3 = Item(id=3, order_id=2, product_id=3, amount=75, quantity=5, unit_price=15)
    item4 = Item(id=4, order_id=2, product_id=4, amount=150, quantity=10, unit_price=15)
    product1 = Product(id=1, name="Product A", unit_price=10)
    product2 = Product(id=2, name="Product B", unit_price=20)
    product3 = Product(id=3, name="Product C", unit_price=15)
    product4 = Product(id=4, name="Product D", unit_price=30)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
