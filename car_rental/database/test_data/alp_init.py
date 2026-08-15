#!/usr/bin/env python
import os, logging, logging.config, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # ensure project root on path
from config import server_setup
import api.system.api_utils as api_utils
from flask import Flask
import logging
import config.config as config

os.environ["PROJECT_DIR"] = os.environ.get("PROJECT_DIR", os.path.abspath(os.path.dirname(__file__)))

app_logger = server_setup.logging_setup()
app_logger.setLevel(logging.INFO) 

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([current_path, '.'])

flask_app = Flask("API Logic Server", template_folder='ui/templates')
flask_app.config.from_object(config.Config)
flask_app.config.from_prefixed_env(prefix="APILOGICPROJECT")

args = server_setup.get_args(flask_app)

server_setup.api_logic_server_setup(flask_app, args)

from database.models import *
import safrs
from datetime import date
import os
os.environ['AGGREGATE_DEFAULTS'] = 'True'

with flask_app.app_context():
    safrs.DB.create_all()
    session = safrs.DB.session

    sys_config = session.query(SysConfig).get(1)
    print(f"sys_config: max_rental_days={sys_config.max_rental_days}, "
          f"max_additional_drivers={sys_config.max_additional_drivers}, "
          f"min_driver_age={sys_config.min_driver_age}, "
          f"grace_period_hours={sys_config.grace_period_hours}, "
          f"bad_experience_bar_threshold={sys_config.bad_experience_bar_threshold}, "
          f"location_penalty_amount={sys_config.location_penalty_amount}")

    # --- Geography / organization ---
    ch = Country(name="Switzerland", iso_code="CH"); session.add(ch)
    gb = Country(name="United Kingdom", iso_code="GB"); session.add(gb)
    session.commit()

    eu_rent_ch = OperatingCompany(name="EU-Rent CH", country_id=ch.id); session.add(eu_rent_ch)
    eu_rent_uk = OperatingCompany(name="EU-Rent UK", country_id=gb.id); session.add(eu_rent_uk)
    session.commit()

    zurich_area = LocalArea(name="Zurich Area", operating_company_id=eu_rent_ch.id); session.add(zurich_area)
    london_area = LocalArea(name="London Area", operating_company_id=eu_rent_uk.id); session.add(london_area)
    session.commit()

    zurich_airport = Branch(name="Zurich Airport", branch_type="airport", local_area_id=zurich_area.id, car_storage_capacity=150)
    zurich_city = Branch(name="Zurich City", branch_type="city", local_area_id=zurich_area.id, car_storage_capacity=30)
    heathrow_airport = Branch(name="Heathrow Airport", branch_type="airport", local_area_id=london_area.id, car_storage_capacity=200)
    london_city = Branch(name="London City", branch_type="city", local_area_id=london_area.id, car_storage_capacity=25)
    session.add_all([zurich_airport, zurich_city, heathrow_airport, london_city])
    session.commit()

    # --- Rental cars ---
    toyota = CarManufacturer(name="Toyota"); session.add(toyota)
    vw = CarManufacturer(name="Volkswagen"); session.add(vw)
    ford = CarManufacturer(name="Ford"); session.add(ford)
    session.commit()

    economy = CarGroup(name="Economy", passenger_capacity=4, large_suitcase_capacity=1, small_suitcase_capacity=1,
                        rental_hour_rate=8, rental_day_rate=45, rental_week_rate=270)
    compact = CarGroup(name="Compact", passenger_capacity=5, large_suitcase_capacity=1, small_suitcase_capacity=1,
                        rental_hour_rate=9, rental_day_rate=52, rental_week_rate=310)
    intermediate = CarGroup(name="Intermediate", passenger_capacity=5, large_suitcase_capacity=1, small_suitcase_capacity=2,
                             rental_hour_rate=10, rental_day_rate=60, rental_week_rate=360)
    standard = CarGroup(name="Standard", passenger_capacity=5, large_suitcase_capacity=2, small_suitcase_capacity=1,
                         rental_hour_rate=12, rental_day_rate=70, rental_week_rate=420)
    full_size = CarGroup(name="Full Size", passenger_capacity=5, large_suitcase_capacity=2, small_suitcase_capacity=2,
                          rental_hour_rate=15, rental_day_rate=85, rental_week_rate=510)
    premium = CarGroup(name="Premium", passenger_capacity=5, large_suitcase_capacity=2, small_suitcase_capacity=2,
                        rental_hour_rate=25, rental_day_rate=150, rental_week_rate=900)
    session.add_all([economy, compact, intermediate, standard, full_size, premium])
    session.commit()

    yaris = CarModel(name="Toyota Yaris", car_manufacturer_id=toyota.id, car_group_id=economy.id,
                      body_style="hatchback", fuel_type="gasoline", passenger_capacity=4)
    golf = CarModel(name="VW Golf", car_manufacturer_id=vw.id, car_group_id=compact.id,
                     body_style="hatchback", fuel_type="gasoline", passenger_capacity=5)
    corolla = CarModel(name="Toyota Corolla", car_manufacturer_id=toyota.id, car_group_id=intermediate.id,
                        body_style="sedan", fuel_type="gasoline", passenger_capacity=5)
    mondeo = CarModel(name="Ford Mondeo", car_manufacturer_id=ford.id, car_group_id=standard.id,
                       body_style="sedan", fuel_type="diesel", passenger_capacity=5)
    camry = CarModel(name="Toyota Camry", car_manufacturer_id=toyota.id, car_group_id=full_size.id,
                      body_style="sedan", fuel_type="gasoline", passenger_capacity=5)
    passat = CarModel(name="VW Passat", car_manufacturer_id=vw.id, car_group_id=premium.id,
                       body_style="sedan", fuel_type="gasoline", passenger_capacity=5)
    session.add_all([yaris, golf, corolla, mondeo, camry, passat])
    session.commit()

    car_yaris = Car(vin="VIN000000000YARIS", car_model_id=yaris.id, local_area_id=zurich_area.id,
                     branch_id=zurich_airport.id, odometer_reading=12000, service_mileage=15000, fuel_level="full")
    car_golf = Car(vin="VIN0000000000GOLF", car_model_id=golf.id, local_area_id=zurich_area.id,
                    branch_id=zurich_airport.id, odometer_reading=8000, service_mileage=10000, fuel_level="full")
    car_corolla = Car(vin="VIN0000000COROLLA", car_model_id=corolla.id, local_area_id=london_area.id,
                       branch_id=heathrow_airport.id, odometer_reading=20000, service_mileage=25000, fuel_level="full")
    car_mondeo = Car(vin="VIN00000000MONDEO", car_model_id=mondeo.id, local_area_id=london_area.id,
                      branch_id=london_city.id, odometer_reading=5000, service_mileage=10000, fuel_level="3/4")
    car_camry = Car(vin="VIN000000000CAMRY", car_model_id=camry.id, local_area_id=zurich_area.id,
                     branch_id=zurich_city.id, odometer_reading=30000, service_mileage=35000, fuel_level="full")
    car_passat = Car(vin="VIN00000000PASSAT", car_model_id=passat.id, local_area_id=london_area.id,
                      branch_id=heathrow_airport.id, odometer_reading=1000, service_mileage=5000, fuel_level="full")
    session.add_all([car_yaris, car_golf, car_corolla, car_mondeo, car_camry, car_passat])
    session.commit()

    # --- Persons ---
    alice = Person(first_name="Alice", last_name="Meier", email="alice@example.com",
                    birth_date="1990-05-10", driver_license_number="CH-DL-1001", driver_license_expiry="2027-01-01")
    bob = Person(first_name="Bob", last_name="Keller", email="bob@example.com",
                 birth_date="2007-01-01", driver_license_number="CH-DL-1002", driver_license_expiry="2029-01-01")  # under min age
    carla = Person(first_name="Carla", last_name="Weber", email="carla@example.com",
                    birth_date="1985-03-15", driver_license_number="CH-DL-1003", driver_license_expiry="2020-01-01")  # expired license
    david = Person(first_name="David", last_name="Smith", email="david@example.com",
                    birth_date="1995-07-20", driver_license_number="GB-DL-2001", driver_license_expiry="2028-01-01")
    emma = Person(first_name="Emma", last_name="Brown", email="emma@example.com",
                   birth_date="1998-11-02", driver_license_number="GB-DL-2002", driver_license_expiry="2027-06-01")
    frank = Person(first_name="Frank", last_name="Jones", email="frank@example.com",
                    birth_date="2000-02-14", driver_license_number="GB-DL-2003", driver_license_expiry="2029-01-01")
    grace = Person(first_name="Grace", last_name="Lee", email="grace@example.com",
                    birth_date="1992-09-09", driver_license_number="GB-DL-2004", driver_license_expiry="2027-03-01")
    henry = Person(first_name="Henry", last_name="Ford", email="henry@example.com",
                    birth_date="1988-04-04", driver_license_number="GB-DL-2005", driver_license_expiry="2027-08-01")
    session.add_all([alice, bob, carla, david, emma, frank, grace, henry])
    session.commit()

    print(f"person qualification: alice={alice.is_qualified} (expect 1), "
          f"bob(under-age)={bob.is_qualified} (expect 0), "
          f"carla(expired-license)={carla.is_qualified} (expect 0)")

    # --- Rental 1: normal open rental, no violations ---
    r1 = Rental(renter_id=alice.id, pickup_branch_id=zurich_airport.id, return_branch_id=zurich_airport.id,
                 car_group_id=compact.id, car_id=car_golf.id,
                 scheduled_pickup_datetime="2026-08-01T09:00:00", scheduled_return_datetime="2026-08-05T09:00:00",
                 actual_pickup_datetime="2026-08-01T09:15:00",
                 status="open", credit_card_name="Alice Meier", fuel_level_at_pickup="full")
    session.add(r1); session.commit()
    session.add(RentalDriver(rental_id=r1.id, person_id=alice.id, is_renter=1)); session.commit()
    print(f"R1 (normal open rental): duration_days={r1.rental_duration_days} (expect 4), "
          f"base_rental_cost={r1.base_rental_cost} (expect 208), rental_price={r1.rental_price} (expect 208)")

    # --- Rental 0 + 3 bad experiences: makes David a barred driver ---
    r0 = Rental(renter_id=david.id, pickup_branch_id=heathrow_airport.id, return_branch_id=heathrow_airport.id,
                car_group_id=economy.id, car_id=car_yaris.id,
                scheduled_pickup_datetime="2026-06-01T09:00:00", scheduled_return_datetime="2026-06-03T09:00:00",
                actual_pickup_datetime="2026-06-01T09:00:00", actual_return_datetime="2026-06-03T09:00:00",
                status="returned", credit_card_name="David Smith", fuel_level_at_pickup="full")
    session.add(r0); session.commit()
    session.add(RentalDriver(rental_id=r0.id, person_id=david.id, is_renter=1)); session.commit()
    for desc in ["unauthorized late return", "unpaid parking ticket", "damage to car during rental"]:
        session.add(BadExperience(rental_id=r0.id, driver_id=david.id, description=desc,
                                   occurred_datetime="2026-06-02T12:00:00", notification_datetime="2026-06-10T12:00:00"))
    session.commit()
    print(f"David bad_experience_count={david.bad_experience_count} (expect 3), is_barred={david.is_barred} (expect 1)")

    # --- Rental 2: DEMONSTRATION - barred driver cannot open a rental (G.7.3) ---
    r2 = Rental(renter_id=david.id, pickup_branch_id=heathrow_airport.id, return_branch_id=heathrow_airport.id,
                car_group_id=economy.id, car_id=None,
                scheduled_pickup_datetime="2026-08-10T09:00:00", scheduled_return_datetime="2026-08-12T09:00:00",
                actual_pickup_datetime="2026-08-10T09:00:00",
                status="open", credit_card_name="David Smith", fuel_level_at_pickup="full")
    r2.RentalDriverList.append(RentalDriver(person_id=david.id, is_renter=1))
    session.add(r2)
    try:
        session.commit()
        print("R2: UNEXPECTED - barred driver was allowed to open a rental")
    except Exception as e:
        session.rollback()
        print(f"R2 (expected rejection - barred driver): {e}")

    # --- Rental 3: DEMONSTRATION - rental duration exceeding 90 days (G.7.7) ---
    r3 = Rental(renter_id=emma.id, pickup_branch_id=london_city.id, return_branch_id=london_city.id,
                car_group_id=standard.id, car_id=None,
                scheduled_pickup_datetime="2026-08-01T09:00:00", scheduled_return_datetime="2026-11-15T09:00:00",
                status="reserved")
    session.add(r3)
    try:
        session.commit()
        print("R3: UNEXPECTED - 106-day rental was allowed")
    except Exception as e:
        session.rollback()
        print(f"R3 (expected rejection - exceeds max_rental_days): {e}")

    # --- Rental 4: DEMONSTRATION - more than 3 additional drivers (G.5.1) ---
    r4 = Rental(renter_id=grace.id, pickup_branch_id=heathrow_airport.id, return_branch_id=heathrow_airport.id,
                car_group_id=intermediate.id, car_id=None,
                scheduled_pickup_datetime="2026-08-15T09:00:00", scheduled_return_datetime="2026-08-18T09:00:00",
                status="reserved")
    session.add(r4); session.commit()
    session.add(RentalDriver(rental_id=r4.id, person_id=grace.id, is_renter=1)); session.commit()
    try:
        for extra_driver in [emma, frank, alice, henry]:  # 4 additional drivers, only 3 allowed
                                                           # (alice: also renter of R1 - permitted per G.7.9)
            session.add(RentalDriver(rental_id=r4.id, person_id=extra_driver.id, is_renter=0))
        session.commit()
        print("R4: UNEXPECTED - 4 additional drivers were allowed")
    except Exception as e:
        session.rollback()
        print(f"R4 (expected rejection - exceeds max_additional_drivers): {e}")

    # --- Rental 5: returned rental with a location penalty (drop-off != return branch) ---
    r5 = Rental(renter_id=henry.id, pickup_branch_id=heathrow_airport.id, return_branch_id=heathrow_airport.id,
                car_group_id=premium.id, car_id=car_passat.id,
                scheduled_pickup_datetime="2026-07-10T09:00:00", scheduled_return_datetime="2026-07-12T09:00:00",
                actual_pickup_datetime="2026-07-10T09:00:00", actual_return_datetime="2026-07-12T09:00:00",
                drop_off_branch_id=london_city.id,  # not the return_branch (heathrow_airport)
                status="returned", credit_card_name="Henry Ford", fuel_level_at_pickup="full")
    session.add(r5); session.commit()
    session.add(RentalDriver(rental_id=r5.id, person_id=henry.id, is_renter=1)); session.commit()
    print(f"R5 (location penalty): location_penalty_charge={r5.location_penalty_charge} (expect 50), "
          f"rental_price={r5.rental_price} (expect 350 = 2 days x 150 + 50 penalty)")

    # --- Rental 6: returned rental with a late return charge ---
    r6 = Rental(renter_id=frank.id, pickup_branch_id=zurich_city.id, return_branch_id=zurich_city.id,
                car_group_id=full_size.id, car_id=car_camry.id,
                scheduled_pickup_datetime="2026-07-20T10:00:00", scheduled_return_datetime="2026-07-22T10:00:00",
                actual_pickup_datetime="2026-07-20T10:00:00", actual_return_datetime="2026-07-22T15:00:00",
                status="returned", credit_card_name="Frank Jones", fuel_level_at_pickup="full")
    session.add(r6); session.commit()
    session.add(RentalDriver(rental_id=r6.id, person_id=frank.id, is_renter=1)); session.commit()
    print(f"R6 (late return): late_return_charge={r6.late_return_charge} (expect 4 hrs x 15 = 60), "
          f"rental_price={r6.rental_price} (expect 230 = 2 days x 85 + 60 late charge)")
