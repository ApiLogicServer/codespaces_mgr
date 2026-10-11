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
    """description: Customer data model with a balance column derived from unpaid orders."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL, default=0)

class Order(Base):
    """description: Order data model with a note and total amount derived from items."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date_shipped = Column(DateTime)
    notes = Column(String)
    amount_total = Column(DECIMAL, default=0)

class Item(Base):
    """description: Item data model with unit price copied from product and amount derived."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: Product data model holding basic product information."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
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
    customer1 = Customer(name='Acme Corp', credit_limit=Decimal('10000.00'), balance=Decimal('5000.00'))
    customer2 = Customer(name='Beta Corp', credit_limit=Decimal('15000.00'), balance=Decimal('3000.00'))
    customer3 = Customer(name='Gamma Inc', credit_limit=Decimal('12000.00'), balance=Decimal('6200.00'))
    customer4 = Customer(name='Delta LLC', credit_limit=Decimal('20000.00'), balance=Decimal('1000.00'))
    order1 = Order(customer_id=1, date_shipped=None, notes='Urgent shipment', amount_total=Decimal('2500.00'))
    order2 = Order(customer_id=2, date_shipped=date(2023, 2, 15), notes='Handle with care', amount_total=Decimal('800.00'))
    order3 = Order(customer_id=3, date_shipped=None, notes='Deliver by next week', amount_total=Decimal('420.00'))
    order4 = Order(customer_id=4, date_shipped=date(2023, 3, 1), notes='Gift wrapping included', amount_total=Decimal('500.00'))
    item1 = Item(order_id=1, product_id=1, quantity=5, unit_price=Decimal('500.00'), amount=Decimal('2500.00'))
    item2 = Item(order_id=2, product_id=2, quantity=10, unit_price=Decimal('80.00'), amount=Decimal('800.00'))
    item3 = Item(order_id=3, product_id=1, quantity=3, unit_price=Decimal('140.00'), amount=Decimal('420.00'))
    item4 = Item(order_id=4, product_id=3, quantity=2, unit_price=Decimal('250.00'), amount=Decimal('500.00'))
    product1 = Product(name='Widget A', unit_price=Decimal('500.00'))
    product2 = Product(name='Gadget B', unit_price=Decimal('80.00'))
    product3 = Product(name='Thing C', unit_price=Decimal('250.00'))
    product4 = Product(name='Device D', unit_price=Decimal('300.00'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
