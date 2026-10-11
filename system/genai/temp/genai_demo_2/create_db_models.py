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
    """description: Customer table storing customer information."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    credit_limit = Column(DECIMAL, nullable=False)
    balance = Column(DECIMAL)

class Order(Base):
    """description: Order table containing the customer orders."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date_shipped = Column(DateTime)
    notes = Column(String(200))
    amount_total = Column(DECIMAL)

class Item(Base):
    """description: Item table linking products with orders. Each item has price, quantity, and derived amount."""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL)
    amount = Column(DECIMAL)

class Product(Base):
    """description: Product table storing product details."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
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
    customer1 = Customer(id=1, name="Alice Wonderland", credit_limit=Decimal('10000.00'), balance=Decimal('0.00'))
    customer2 = Customer(id=2, name="Bob Builder", credit_limit=Decimal('5000.00'), balance=Decimal('0.00'))
    customer3 = Customer(id=3, name="Charlie Chocolate", credit_limit=Decimal('2000.00'), balance=Decimal('0.00'))
    customer4 = Customer(id=4, name="Dora Explorer", credit_limit=Decimal('3000.00'), balance=Decimal('0.00'))
    order1 = Order(id=1, customer_id=1, date_shipped=None, notes="Urgent delivery", amount_total=Decimal('0.00'))
    order2 = Order(id=2, customer_id=2, date_shipped=date(2023, 1, 15), notes="Gift wrap", amount_total=Decimal('0.00'))
    order3 = Order(id=3, customer_id=3, date_shipped=None, notes="No rush", amount_total=Decimal('0.00'))
    order4 = Order(id=4, customer_id=4, date_shipped=date(2023, 3, 1), notes="Handle with care", amount_total=Decimal('0.00'))
    product1 = Product(id=1, name="Widget", unit_price=Decimal('199.99'))
    product2 = Product(id=2, name="Gadget", unit_price=Decimal('299.99'))
    product3 = Product(id=3, name="Thingamajig", unit_price=Decimal('99.99'))
    product4 = Product(id=4, name="Doodad", unit_price=Decimal('49.99'))
    item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=Decimal('199.99'), amount=Decimal('399.98'))
    item2 = Item(id=2, order_id=2, product_id=2, quantity=1, unit_price=Decimal('299.99'), amount=Decimal('299.99'))
    item3 = Item(id=3, order_id=3, product_id=3, quantity=5, unit_price=Decimal('99.99'), amount=Decimal('499.95'))
    item4 = Item(id=4, order_id=4, product_id=4, quantity=3, unit_price=Decimal('49.99'), amount=Decimal('149.97'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, product1, product2, product3, product4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
