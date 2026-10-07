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
    """description: Customer table with balance and credit limit."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(DECIMAL, nullable=False, default=0)
    credit_limit = Column(DECIMAL, nullable=False, default=0)

class Order(Base):
    """description: Order table with foreign key to Customer and amount_total, date_shipped fields."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    amount_total = Column(DECIMAL, nullable=False, default=0)
    date_shipped = Column(DateTime)
    notes = Column(String)

class Item(Base):
    """description: Item table linking Orders and Products with quantity, unit price, and amount."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL, nullable=False, default=0)

class Product(Base):
    """description: Product table with unit price field."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
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
    customer1 = Customer(name="John Doe", balance=Decimal('100.00'), credit_limit=Decimal('500.00'))
    customer2 = Customer(name="Jane Smith", balance=Decimal('150.00'), credit_limit=Decimal('450.00'))
    customer3 = Customer(name="Jim Beam", balance=Decimal('200.00'), credit_limit=Decimal('550.00'))
    customer4 = Customer(name="Jack Daniels", balance=Decimal('250.00'), credit_limit=Decimal('600.00'))
    product1 = Product(name="Widget A", unit_price=Decimal('20.00'))
    product2 = Product(name="Widget B", unit_price=Decimal('25.00'))
    product3 = Product(name="Widget C", unit_price=Decimal('30.00'))
    product4 = Product(name="Widget D", unit_price=Decimal('35.00'))
    order1 = Order(customer_id=1, amount_total=Decimal('0'))
    order2 = Order(customer_id=2, amount_total=Decimal('0'))
    order3 = Order(customer_id=3, amount_total=Decimal('0'))
    order4 = Order(customer_id=4, amount_total=Decimal('0'))
    item1 = Item(order_id=1, product_id=1, quantity=2, unit_price=Decimal('20.00'), amount=Decimal('40.00'))
    item2 = Item(order_id=2, product_id=2, quantity=3, unit_price=Decimal('25.00'), amount=Decimal('75.00'))
    item3 = Item(order_id=3, product_id=3, quantity=1, unit_price=Decimal('30.00'), amount=Decimal('30.00'))
    item4 = Item(order_id=4, product_id=4, quantity=4, unit_price=Decimal('35.00'), amount=Decimal('140.00'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, product1, product2, product3, product4, order1, order2, order3, order4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
