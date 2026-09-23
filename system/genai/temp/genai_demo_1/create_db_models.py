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
    """description: Customer with balance and credit limit"""
    __tablename__ = 'customer'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    CreditLimit = Column(DECIMAL)
    Balance = Column(DECIMAL, default=decimal.Decimal(0))

class Order(Base):
    """description: Orders that belongs to a customer and includes total amount and shipment date"""
    __tablename__ = 'order'
    Id = Column(Integer, primary_key=True)
    CustomerId = Column(ForeignKey('customer.Id'))
    DateShipped = Column(DateTime)
    AmountTotal = Column(DECIMAL, default=decimal.Decimal(0))
    Notes = Column(String)

class Item(Base):
    """description: Items with quantity, unit price, and total amount"""
    __tablename__ = 'item'
    Id = Column(Integer, primary_key=True)
    OrderId = Column(ForeignKey('order.Id'))
    Quantity = Column(Integer)
    UnitPrice = Column(DECIMAL)
    Amount = Column(DECIMAL, default=decimal.Decimal(0))

class Product(Base):
    """description: Products with name and unit price"""
    __tablename__ = 'product'
    Id = Column(Integer, primary_key=True)
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
    customer1 = Customer(Id=1, Name="Alice", CreditLimit=Decimal(1000), Balance=Decimal(300))
    customer2 = Customer(Id=2, Name="Bob", CreditLimit=Decimal(1500), Balance=Decimal(200))
    customer3 = Customer(Id=3, Name="Carol", CreditLimit=Decimal(1200), Balance=Decimal(150))
    customer4 = Customer(Id=4, Name="Dave", CreditLimit=Decimal(800), Balance=Decimal(400))
    order1 = Order(Id=1, CustomerId=1, DateShipped=None, AmountTotal=Decimal(300), Notes="First order")
    order2 = Order(Id=2, CustomerId=2, DateShipped=date(2023, 5, 20), AmountTotal=Decimal(200), Notes="Second order")
    order3 = Order(Id=3, CustomerId=3, DateShipped=None, AmountTotal=Decimal(150), Notes="Third order")
    order4 = Order(Id=4, CustomerId=4, DateShipped=date(2023, 6, 10), AmountTotal=Decimal(400), Notes="Fourth order")
    item1 = Item(Id=1, OrderId=1, Quantity=2, UnitPrice=Decimal(150), Amount=Decimal(300))
    item2 = Item(Id=2, OrderId=2, Quantity=1, UnitPrice=Decimal(200), Amount=Decimal(200))
    item3 = Item(Id=3, OrderId=3, Quantity=3, UnitPrice=Decimal(50), Amount=Decimal(150))
    item4 = Item(Id=4, OrderId=4, Quantity=4, UnitPrice=Decimal(100), Amount=Decimal(400))
    product1 = Product(Id=1, Name="Product A", UnitPrice=Decimal(150))
    product2 = Product(Id=2, Name="Product B", UnitPrice=Decimal(200))
    product3 = Product(Id=3, Name="Product C", UnitPrice=Decimal(50))
    product4 = Product(Id=4, Name="Product D", UnitPrice=Decimal(100))
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, item1, item2, item3, item4, product1, product2, product3, product4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
