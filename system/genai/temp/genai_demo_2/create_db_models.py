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
    """description: Represents a customer with a credit limit and balance."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL, default=0.0)

class Order(Base):
    """description: Represents an order linked to a customer with notes and shipping date."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    notes = Column(String)
    date_shipped = Column(Date)
    amount_total = Column(DECIMAL, default=0.0)

class Item(Base):
    """description: Details of items linked to orders, including quantity, unit price, and total amount."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    amount = Column(DECIMAL, default=0.0)

class Product(Base):
    """description: Product entity containing product details and unit price."""
    __tablename__ = 'product'
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
    customer1 = Customer(name="Alice", credit_limit=Decimal('1000.00'), balance=Decimal('0.00'))
    customer2 = Customer(name="Bob", credit_limit=Decimal('1500.00'), balance=Decimal('0.00'))
    customer3 = Customer(name="Charlie", credit_limit=Decimal('2000.00'), balance=Decimal('0.00'))
    customer4 = Customer(name="Diana", credit_limit=Decimal('2500.00'), balance=Decimal('0.00'))
    order1 = Order(customer_id=customer1.id, notes="Urgent delivery", date_shipped=date(2023, 10, 5), amount_total=Decimal('200.00'))
    order2 = Order(customer_id=customer1.id, notes="Standard shipping", date_shipped=None, amount_total=Decimal('0.00'))
    order3 = Order(customer_id=customer2.id, notes="Gift wrapping", date_shipped=date(2023, 10, 10), amount_total=Decimal('150.00'))
    order4 = Order(customer_id=customer3.id, notes="Fragile", date_shipped=None, amount_total=Decimal('0.00'))
    item1 = Item(order_id=order1.id, product_id=1, quantity=2, unit_price=Decimal('50.00'), amount=Decimal('100.00'))
    item2 = Item(order_id=order1.id, product_id=2, quantity=1, unit_price=Decimal('100.00'), amount=Decimal('100.00'))
    item3 = Item(order_id=order3.id, product_id=3, quantity=3, unit_price=Decimal('50.00'), amount=Decimal('150.00'))
    item4 = Item(order_id=order4.id, product_id=4, quantity=1, unit_price=Decimal('0.00'), amount=Decimal('0.00'))
    product1 = Product(name="Laptop", unit_price=Decimal('50.00'))
    product2 = Product(name="Smartphone", unit_price=Decimal('100.00'))
    product3 = Product(name="Headphones", unit_price=Decimal('50.00'))
    product4 = Product(name="Smartwatch", unit_price=Decimal('0.00'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
