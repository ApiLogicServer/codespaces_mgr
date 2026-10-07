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
    """description: Customer model including credit limit and balance."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    credit_limit = Column(DECIMAL)
    balance = Column(DECIMAL)

class Order(Base):
    """description: Order model containing note field and shipped date."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    amount_total = Column(DECIMAL)
    notes = Column(String)
    date_shipped = Column(Date)

class Item(Base):
    """description: Item model storing quantity, unit price, and total amount."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: Product model with unit price."""
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
    customer1 = Customer(name="Customer A", credit_limit=Decimal('1000.00'), balance=Decimal('500.00'))
    customer2 = Customer(name="Customer B", credit_limit=Decimal('2000.00'), balance=Decimal('1500.00'))
    customer3 = Customer(name="Customer C", credit_limit=Decimal('3000.00'), balance=Decimal('2500.00'))
    customer4 = Customer(name="Customer D", credit_limit=Decimal('4000.00'), balance=Decimal('3500.00'))
    order1 = Order(customer_id=customer1.id, amount_total=Decimal('500.00'), notes="First Order", date_shipped=None)
    order2 = Order(customer_id=customer2.id, amount_total=Decimal('1500.00'), notes="Second Order", date_shipped=date(2023, 10, 1))
    order3 = Order(customer_id=customer3.id, amount_total=Decimal('2500.00'), notes="Third Order", date_shipped=None)
    order4 = Order(customer_id=customer4.id, amount_total=Decimal('3500.00'), notes="Fourth Order", date_shipped=date(2023, 10, 5))
    item1 = Item(order_id=order1.id, product_id=1, quantity=2, unit_price=Decimal('250.00'), amount=Decimal('500.00'))
    item2 = Item(order_id=order2.id, product_id=2, quantity=3, unit_price=Decimal('500.00'), amount=Decimal('1500.00'))
    item3 = Item(order_id=order3.id, product_id=3, quantity=5, unit_price=Decimal('500.00'), amount=Decimal('2500.00'))
    item4 = Item(order_id=order4.id, product_id=4, quantity=7, unit_price=Decimal('500.00'), amount=Decimal('3500.00'))
    product1 = Product(name="Product A", unit_price=Decimal('250.00'))
    product2 = Product(name="Product B", unit_price=Decimal('500.00'))
    product3 = Product(name="Product C", unit_price=Decimal('500.00'))
    product4 = Product(name="Product D", unit_price=Decimal('500.00'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
