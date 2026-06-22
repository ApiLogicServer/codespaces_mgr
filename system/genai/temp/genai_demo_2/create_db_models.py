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
    """description: Customer Class"""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    credit_limit = Column(DECIMAL)
    balance = Column(DECIMAL, default=0)

class Order(Base):
    """description: Order Class"""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    amount_total = Column(DECIMAL, default=0)
    date_shipped = Column(DateTime, nullable=True)
    notes = Column(String)

class Item(Base):
    """description: Item Class"""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    amount = Column(DECIMAL)
    unit_price = Column(DECIMAL)

class Product(Base):
    """description: Product Class"""
    __tablename__ = 'product'
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
    customer1 = Customer(name="Alice Johnson", credit_limit=Decimal("10000"), balance=Decimal("2000"))
    customer2 = Customer(name="Bob Smith", credit_limit=Decimal("15000"), balance=Decimal("4000"))
    customer3 = Customer(name="Catherine Wright", credit_limit=Decimal("20000"), balance=Decimal("6000"))
    customer4 = Customer(name="David Brown", credit_limit=Decimal("25000"), balance=Decimal("8000"))
    order1 = Order(customer_id=customer1.id, amount_total=Decimal("500"), date_shipped=None, notes="Urgent delivery")
    order2 = Order(customer_id=customer2.id, amount_total=Decimal("1200"), date_shipped=None, notes="Fast delivery")
    order3 = Order(customer_id=customer3.id, amount_total=Decimal("300"), date_shipped=date(2023, 10, 10), notes="Return requested")
    order4 = Order(customer_id=customer4.id, amount_total=Decimal("350"), date_shipped=date(2023, 10, 11), notes="Priority")
    item1 = Item(order_id=order1.id, product_id=1, quantity=2, amount=Decimal("600"), unit_price=Decimal("300"))
    item2 = Item(order_id=order2.id, product_id=2, quantity=4, amount=Decimal("200"), unit_price=Decimal("50"))
    item3 = Item(order_id=order3.id, product_id=1, quantity=1, amount=Decimal("250"), unit_price=Decimal("250"))
    item4 = Item(order_id=order4.id, product_id=3, quantity=3, amount=Decimal("450"), unit_price=Decimal("150"))
    product1 = Product(name="Laptop", unit_price=Decimal("800"))
    product2 = Product(name="Mouse", unit_price=Decimal("20"))
    product3 = Product(name="Keyboard", unit_price=Decimal("30"))
    product4 = Product(name="Monitor", unit_price=Decimal("150"))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
