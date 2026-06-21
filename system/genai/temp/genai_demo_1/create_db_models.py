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
    """description: This class defines the Customer entity."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(DECIMAL)
    credit_limit = Column(DECIMAL)

class Order(Base):
    """description: This class defines the Order entity with a notes field."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    amount_total = Column(DECIMAL)
    date_shipped = Column(DateTime)
    notes = Column(String)

class Item(Base):
    """description: This class defines the Item entity."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: This class defines the Product entity for storing product information."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    customer1 = Customer(balance=Decimal('1000'), credit_limit=Decimal('5000'))
    order1 = Order(customer_id=1, amount_total=Decimal('300'), date_shipped=date(2023, 1, 1), notes="Priority order")
    item1 = Item(order_id=1, quantity=10, unit_price=Decimal('30'), amount=Decimal('300'))
    product1 = Product(unit_price=Decimal('30'))
    customer2 = Customer(balance=Decimal('1500'), credit_limit=Decimal('5000'))
    order2 = Order(customer_id=2, amount_total=Decimal('450'), date_shipped=date(2023, 2, 15), notes="Urge shipment")
    item2 = Item(order_id=2, quantity=15, unit_price=Decimal('30'), amount=Decimal('450'))
    product2 = Product(unit_price=Decimal('30'))
    customer3 = Customer(balance=Decimal('2000'), credit_limit=Decimal('5000'))
    order3 = Order(customer_id=3, amount_total=Decimal('750'), date_shipped=date(2023, 3, 10), notes="Regular shipment")
    item3 = Item(order_id=3, quantity=25, unit_price=Decimal('30'), amount=Decimal('750'))
    product3 = Product(unit_price=Decimal('30'))
    customer4 = Customer(balance=Decimal('2500'), credit_limit=Decimal('5000'))
    order4 = Order(customer_id=4, amount_total=Decimal('900'), date_shipped=date(2023, 4, 5), notes="Delayed shipment")
    item4 = Item(order_id=4, quantity=30, unit_price=Decimal('30'), amount=Decimal('900'))
    product4 = Product(unit_price=Decimal('30'))
    
    
    
    session.add_all([customer1, order1, item1, product1, customer2, order2, item2, product2, customer3, order3, item3, product3, customer4, order4, item4, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
