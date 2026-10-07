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
    """description: Represents a customer of the system. Includes balance and credit limit."""
    __tablename__ = 'customer'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    CreditLimit = Column(DECIMAL)
    Balance = Column(DECIMAL)

class Order(Base):
    """description: Represents an order made by a customer. Includes the total amount and a notes field."""
    __tablename__ = 'order'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    CustomerId = Column(Integer, ForeignKey('customer.Id'))
    DateShipped = Column(DateTime)
    Notes = Column(String)
    AmountTotal = Column(DECIMAL)

class Item(Base):
    """description: Represents items included in an order. Stores quantity, unit price, and total amount."""
    __tablename__ = 'item'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    OrderId = Column(Integer, ForeignKey('order.Id'))
    ProductId = Column(Integer, ForeignKey('product.Id'))
    Quantity = Column(Integer)
    UnitPrice = Column(DECIMAL)
    Amount = Column(DECIMAL)

class Product(Base):
    """description: Represents products that can be ordered. Stores the unit price."""
    __tablename__ = 'product'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    UnitPrice = Column(DECIMAL)


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
    customer1 = Customer(Name="John Doe", CreditLimit=Decimal('1000.00'), Balance=Decimal('0.00'))
    customer2 = Customer(Name="Jane Smith", CreditLimit=Decimal('1500.00'), Balance=Decimal('0.00'))
    customer3 = Customer(Name="Alice Johnson", CreditLimit=Decimal('1200.00'), Balance=Decimal('0.00'))
    customer4 = Customer(Name="Bob Brown", CreditLimit=Decimal('2000.00'), Balance=Decimal('0.00'))
    order1 = Order(CustomerId=1, DateShipped=date(2023, 5, 21), Notes="Urgent", AmountTotal=Decimal('250.00'))
    order2 = Order(CustomerId=2, DateShipped=None, Notes="Deliver to office", AmountTotal=Decimal('500.00'))
    order3 = Order(CustomerId=3, DateShipped=None, Notes="Gift", AmountTotal=Decimal('300.00'))
    order4 = Order(CustomerId=4, DateShipped=date(2023, 6, 11), Notes="Return customer", AmountTotal=Decimal('450.00'))
    item1 = Item(OrderId=1, ProductId=1, Quantity=2, UnitPrice=Decimal('75.00'), Amount=Decimal('150.00'))
    item2 = Item(OrderId=2, ProductId=2, Quantity=5, UnitPrice=Decimal('50.00'), Amount=Decimal('250.00'))
    item3 = Item(OrderId=3, ProductId=3, Quantity=3, UnitPrice=Decimal('40.00'), Amount=Decimal('120.00'))
    item4 = Item(OrderId=4, ProductId=4, Quantity=4, UnitPrice=Decimal('65.00'), Amount=Decimal('260.00'))
    product1 = Product(Name="Widget A", UnitPrice=Decimal('75.00'))
    product2 = Product(Name="Widget B", UnitPrice=Decimal('50.00'))
    product3 = Product(Name="Widget C", UnitPrice=Decimal('40.00'))
    product4 = Product(Name="Widget D", UnitPrice=Decimal('65.00'))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
