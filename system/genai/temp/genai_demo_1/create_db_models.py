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
    """description: This class represents a customer in the system, including financial information."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(DECIMAL)
    credit_limit = Column(DECIMAL)

class Order(Base):
    """description: This class represents an order linked to a customer with additional details and total spending."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date_shipped = Column(DateTime)
    amount_total = Column(DECIMAL)
    notes = Column(String)

class Item(Base):
    """description: The class represents order items with details on quantity and pricing."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: This class represents products available in the system."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
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
    customer1 = Customer(id=1, name="John Doe", balance=Decimal('0.00'), credit_limit=Decimal('1000.00'))
    customer2 = Customer(id=2, name="Jane Smith", balance=Decimal('150.75'), credit_limit=Decimal('2000.00'))
    order1 = Order(id=1, customer_id=1, date_shipped=date(2023, 8, 10), amount_total=Decimal('200.00'), notes="Urgent delivery requested.")
    order2 = Order(id=2, customer_id=2, date_shipped=None, amount_total=Decimal('50.50'), notes="Needs gift wrapping.")
    item1 = Item(id=1, order_id=1, product_id=1, quantity=5, unit_price=Decimal('40.00'), amount=Decimal('200.00'))
    item2 = Item(id=2, order_id=2, product_id=2, quantity=1, unit_price=Decimal('50.50'), amount=Decimal('50.50'))
    product1 = Product(id=1, name="Widget A", unit_price=Decimal('40.00'))
    product2 = Product(id=2, name="Widget B", unit_price=Decimal('50.50'))
    
    
    
    session.add_all([customer1, customer2, order1, order2, item1, item2, product1, product2])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
