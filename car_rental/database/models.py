# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Float, ForeignKey, Integer, Numeric, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  August 01, 2026 09:58:02
# Database: sqlite:////Users/val/dev/ApiLogicServer/ApiLogicServer-dev/org_git/codespaces_mgr/car_rental/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class CarGroup(Base):  # type: ignore
    __tablename__ = 'car_group'
    _s_collection_name = 'CarGroup'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    passenger_capacity = Column(Integer)
    large_suitcase_capacity = Column(Integer)
    small_suitcase_capacity = Column(Integer)
    rental_hour_rate = Column(Numeric(10, 2), nullable=False)
    rental_day_rate = Column(Numeric(10, 2), nullable=False)
    rental_week_rate = Column(Numeric(10, 2))

    # parent relationships (access parent)

    # child relationships (access children)
    CarModelList : Mapped[List["CarModel"]] = relationship(back_populates="car_group")
    RentalList : Mapped[List["Rental"]] = relationship(back_populates="car_group")



class CarManufacturer(Base):  # type: ignore
    __tablename__ = 'car_manufacturer'
    _s_collection_name = 'CarManufacturer'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CarModelList : Mapped[List["CarModel"]] = relationship(back_populates="car_manufacturer")



class Country(Base):  # type: ignore
    __tablename__ = 'country'
    _s_collection_name = 'Country'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    iso_code = Column(Text, nullable=False, unique=True)

    # parent relationships (access parent)

    # child relationships (access children)
    OperatingCompanyList : Mapped[List["OperatingCompany"]] = relationship(back_populates="country")



class SysConfig(Base):  # type: ignore
    __tablename__ = 'sys_config'
    _s_collection_name = 'SysConfig'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, server_default=text("'system'"), nullable=False)
    discount_rate = Column(Float, server_default=text("0.05"))
    tax_rate = Column(Float, server_default=text("0.10"))
    notes = Column(Text)
    max_rental_days = Column(Integer, server_default=text("90"))
    max_additional_drivers = Column(Integer, server_default=text("3"))
    min_driver_age = Column(Integer, server_default=text("21"))
    grace_period_hours = Column(Integer, server_default=text("1"))
    bad_experience_bar_threshold = Column(Integer, server_default=text("3"))
    location_penalty_amount = Column(Numeric(10, 2), server_default=text("50.00"))

    # parent relationships (access parent)

    # child relationships (access children)
    PersonList : Mapped[List["Person"]] = relationship(back_populates="sys_config")
    RentalList : Mapped[List["Rental"]] = relationship(back_populates="sys_config")



class CarModel(Base):  # type: ignore
    __tablename__ = 'car_model'
    _s_collection_name = 'CarModel'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    car_manufacturer_id = Column(ForeignKey('car_manufacturer.id'), nullable=False)
    car_group_id = Column(ForeignKey('car_group.id'), nullable=False)
    body_style = Column(Text)
    fuel_type = Column(Text)
    passenger_capacity = Column(Integer)

    # parent relationships (access parent)
    car_group : Mapped["CarGroup"] = relationship(back_populates=("CarModelList"))
    car_manufacturer : Mapped["CarManufacturer"] = relationship(back_populates=("CarModelList"))

    # child relationships (access children)
    CarList : Mapped[List["Car"]] = relationship(back_populates="car_model")



class OperatingCompany(Base):  # type: ignore
    __tablename__ = 'operating_company'
    _s_collection_name = 'OperatingCompany'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    country_id = Column(ForeignKey('country.id'), nullable=False)

    # parent relationships (access parent)
    country : Mapped["Country"] = relationship(back_populates=("OperatingCompanyList"))

    # child relationships (access children)
    LocalAreaList : Mapped[List["LocalArea"]] = relationship(back_populates="operating_company")



class Person(Base):  # type: ignore
    __tablename__ = 'person'
    _s_collection_name = 'Person'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text)
    birth_date = Column(Text, nullable=False)
    driver_license_number = Column(Text)
    driver_license_expiry = Column(Text)
    sys_config_id = Column(ForeignKey('sys_config.id'), server_default=text("1"))
    min_driver_age = Column(Integer)
    bad_experience_bar_threshold = Column(Integer)
    bad_experience_count = Column(Integer, server_default=text("0"))
    is_qualified = Column(Integer, server_default=text("0"))
    is_barred = Column(Integer, server_default=text("0"))

    # parent relationships (access parent)
    sys_config : Mapped["SysConfig"] = relationship(back_populates=("PersonList"))

    # child relationships (access children)
    RentalList : Mapped[List["Rental"]] = relationship(back_populates="renter")
    BadExperienceList : Mapped[List["BadExperience"]] = relationship(back_populates="driver")
    RentalDriverList : Mapped[List["RentalDriver"]] = relationship(back_populates="person")



class LocalArea(Base):  # type: ignore
    __tablename__ = 'local_area'
    _s_collection_name = 'LocalArea'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    operating_company_id = Column(ForeignKey('operating_company.id'), nullable=False)

    # parent relationships (access parent)
    operating_company : Mapped["OperatingCompany"] = relationship(back_populates=("LocalAreaList"))

    # child relationships (access children)
    BranchList : Mapped[List["Branch"]] = relationship(back_populates="local_area")
    CarList : Mapped[List["Car"]] = relationship(back_populates="local_area")



class Branch(Base):  # type: ignore
    __tablename__ = 'branch'
    _s_collection_name = 'Branch'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    branch_type = Column(Text, nullable=False)
    local_area_id = Column(ForeignKey('local_area.id'), nullable=False)
    car_storage_capacity = Column(Integer)
    is_eu_rent_owned = Column(Integer, server_default=text("1"))

    # parent relationships (access parent)
    local_area : Mapped["LocalArea"] = relationship(back_populates=("BranchList"))

    # child relationships (access children)
    CarList : Mapped[List["Car"]] = relationship(back_populates="branch")
    RentalList : Mapped[List["Rental"]] = relationship(foreign_keys='[Rental.drop_off_branch_id]', back_populates="drop_off_branch")
    pickupRentalList : Mapped[List["Rental"]] = relationship(foreign_keys='[Rental.pickup_branch_id]', back_populates="pickup_branch")
    returnRentalList : Mapped[List["Rental"]] = relationship(foreign_keys='[Rental.return_branch_id]', back_populates="return_branch")



class Car(Base):  # type: ignore
    __tablename__ = 'car'
    _s_collection_name = 'Car'  # type: ignore

    id = Column(Integer, primary_key=True)
    vin = Column(Text, nullable=False, unique=True)
    car_model_id = Column(ForeignKey('car_model.id'), nullable=False)
    local_area_id = Column(ForeignKey('local_area.id'), nullable=False)
    branch_id = Column(ForeignKey('branch.id'))
    odometer_reading = Column(Integer, server_default=text("0"))
    service_mileage = Column(Integer, server_default=text("5000"))
    fuel_level = Column(Text, server_default=text("'full'"))

    # parent relationships (access parent)
    branch : Mapped["Branch"] = relationship(back_populates=("CarList"))
    car_model : Mapped["CarModel"] = relationship(back_populates=("CarList"))
    local_area : Mapped["LocalArea"] = relationship(back_populates=("CarList"))

    # child relationships (access children)
    RentalList : Mapped[List["Rental"]] = relationship(back_populates="car")



class Rental(Base):  # type: ignore
    __tablename__ = 'rental'
    _s_collection_name = 'Rental'  # type: ignore

    id = Column(Integer, primary_key=True)
    renter_id = Column(ForeignKey('person.id'), nullable=False)
    pickup_branch_id = Column(ForeignKey('branch.id'), nullable=False)
    return_branch_id = Column(ForeignKey('branch.id'), nullable=False)
    car_group_id = Column(ForeignKey('car_group.id'), nullable=False)
    car_id = Column(ForeignKey('car.id'))
    scheduled_pickup_datetime = Column(Text, nullable=False)
    scheduled_return_datetime = Column(Text, nullable=False)
    actual_pickup_datetime = Column(Text)
    actual_return_datetime = Column(Text)
    drop_off_branch_id = Column(ForeignKey('branch.id'))
    status = Column(Text, server_default=text("'reserved'"), nullable=False)
    credit_card_name = Column(Text)
    fuel_level_at_pickup = Column(Text)
    sys_config_id = Column(ForeignKey('sys_config.id'), server_default=text("1"))
    max_rental_days = Column(Integer)
    max_additional_drivers = Column(Integer)
    grace_period_hours = Column(Integer)
    location_penalty_amount = Column(Numeric(10, 2))
    additional_driver_count = Column(Integer, server_default=text("0"))
    barred_driver_count = Column(Integer, server_default=text("0"))
    rental_duration_days = Column(Integer, server_default=text("0"))
    base_rental_cost = Column(Numeric(10, 2), server_default=text("0"))
    late_return_charge = Column(Numeric(10, 2), server_default=text("0"))
    location_penalty_charge = Column(Numeric(10, 2), server_default=text("0"))
    total_additional_charges = Column(Numeric(10, 2), server_default=text("0"))
    rental_price = Column(Numeric(10, 2), server_default=text("0"))

    # parent relationships (access parent)
    car_group : Mapped["CarGroup"] = relationship(back_populates=("RentalList"))
    car : Mapped["Car"] = relationship(back_populates=("RentalList"))
    drop_off_branch : Mapped["Branch"] = relationship(foreign_keys='[Rental.drop_off_branch_id]', back_populates=("RentalList"))
    pickup_branch : Mapped["Branch"] = relationship(foreign_keys='[Rental.pickup_branch_id]', back_populates=("pickupRentalList"))
    renter : Mapped["Person"] = relationship(back_populates=("RentalList"))
    return_branch : Mapped["Branch"] = relationship(foreign_keys='[Rental.return_branch_id]', back_populates=("returnRentalList"))
    sys_config : Mapped["SysConfig"] = relationship(back_populates=("RentalList"))

    # child relationships (access children)
    BadExperienceList : Mapped[List["BadExperience"]] = relationship(back_populates="rental")
    RentalDriverList : Mapped[List["RentalDriver"]] = relationship(back_populates="rental")



class BadExperience(Base):  # type: ignore
    __tablename__ = 'bad_experience'
    _s_collection_name = 'BadExperience'  # type: ignore

    id = Column(Integer, primary_key=True)
    rental_id = Column(ForeignKey('rental.id'), nullable=False)
    driver_id = Column(ForeignKey('person.id'), nullable=False)
    description = Column(Text)
    occurred_datetime = Column(Text)
    notification_datetime = Column(Text)

    # parent relationships (access parent)
    driver : Mapped["Person"] = relationship(back_populates=("BadExperienceList"))
    rental : Mapped["Rental"] = relationship(back_populates=("BadExperienceList"))

    # child relationships (access children)



class RentalDriver(Base):  # type: ignore
    __tablename__ = 'rental_driver'
    _s_collection_name = 'RentalDriver'  # type: ignore

    id = Column(Integer, primary_key=True)
    rental_id = Column(ForeignKey('rental.id'), nullable=False)
    person_id = Column(ForeignKey('person.id'), nullable=False)
    is_renter = Column(Integer, server_default=text("0"))

    # parent relationships (access parent)
    person : Mapped["Person"] = relationship(back_populates=("RentalDriverList"))
    rental : Mapped["Rental"] = relationship(back_populates=("RentalDriverList"))

    # child relationships (access children)
