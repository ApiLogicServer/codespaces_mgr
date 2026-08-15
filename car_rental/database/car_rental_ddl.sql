-- car_rental schema, distilled from OMG SBVR Annex G (EU-Rent Example)
-- Keep sys_config; add domain columns (Step 4a constants)

ALTER TABLE sys_config ADD COLUMN max_rental_days INTEGER DEFAULT 90;
ALTER TABLE sys_config ADD COLUMN max_additional_drivers INTEGER DEFAULT 3;
ALTER TABLE sys_config ADD COLUMN min_driver_age INTEGER DEFAULT 21;
ALTER TABLE sys_config ADD COLUMN grace_period_hours INTEGER DEFAULT 1;
ALTER TABLE sys_config ADD COLUMN bad_experience_bar_threshold INTEGER DEFAULT 3;
ALTER TABLE sys_config ADD COLUMN location_penalty_amount NUMERIC(10,2) DEFAULT 50.00;

-- Geography / organization (G.6.4)

CREATE TABLE country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso_code TEXT NOT NULL UNIQUE
);

CREATE TABLE operating_company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country_id INTEGER NOT NULL REFERENCES country(id)
);

CREATE TABLE local_area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    operating_company_id INTEGER NOT NULL REFERENCES operating_company(id)
);

CREATE TABLE branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch_type TEXT NOT NULL,              -- airport | city | agency
    local_area_id INTEGER NOT NULL REFERENCES local_area(id),
    car_storage_capacity INTEGER,
    is_eu_rent_owned INTEGER DEFAULT 1
);

-- Rental cars (G.6.5)

CREATE TABLE car_manufacturer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE car_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,              -- Economy/Compact/Intermediate/Standard/Full Size/Premium
    passenger_capacity INTEGER,
    large_suitcase_capacity INTEGER,
    small_suitcase_capacity INTEGER,
    rental_hour_rate NUMERIC(10,2) NOT NULL,
    rental_day_rate NUMERIC(10,2) NOT NULL,
    rental_week_rate NUMERIC(10,2)
);

CREATE TABLE car_model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    car_manufacturer_id INTEGER NOT NULL REFERENCES car_manufacturer(id),
    car_group_id INTEGER NOT NULL REFERENCES car_group(id),
    body_style TEXT,                        -- convertible/coupe/hatchback/sedan
    fuel_type TEXT,                         -- diesel/electricity/gasoline/LPG
    passenger_capacity INTEGER
);

CREATE TABLE car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT NOT NULL UNIQUE,
    car_model_id INTEGER NOT NULL REFERENCES car_model(id),
    local_area_id INTEGER NOT NULL REFERENCES local_area(id),   -- owner (rental car owner)
    branch_id INTEGER REFERENCES branch(id),                    -- stored at (nullable while in transit)
    odometer_reading INTEGER DEFAULT 0,
    service_mileage INTEGER DEFAULT 5000,
    fuel_level TEXT DEFAULT 'full'
);

-- Customers / drivers (G.6.6)

CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    birth_date TEXT NOT NULL,
    driver_license_number TEXT,
    driver_license_expiry TEXT,
    sys_config_id INTEGER REFERENCES sys_config(id) DEFAULT 1,
    min_driver_age INTEGER,                 -- Rule.copy from sys_config
    bad_experience_bar_threshold INTEGER,   -- Rule.copy from sys_config
    bad_experience_count INTEGER DEFAULT 0, -- Rule.count of bad_experience
    is_qualified INTEGER DEFAULT 0,         -- Rule.formula: age + license
    is_barred INTEGER DEFAULT 0             -- Rule.formula: bad_experience_count >= threshold
);

-- Rentals (G.6.8)

CREATE TABLE rental (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    renter_id INTEGER NOT NULL REFERENCES person(id),
    pickup_branch_id INTEGER NOT NULL REFERENCES branch(id),
    return_branch_id INTEGER NOT NULL REFERENCES branch(id),
    car_group_id INTEGER NOT NULL REFERENCES car_group(id),     -- reserved car group
    car_id INTEGER REFERENCES car(id),                          -- rented car (nullable until assigned)
    scheduled_pickup_datetime TEXT NOT NULL,
    scheduled_return_datetime TEXT NOT NULL,
    actual_pickup_datetime TEXT,
    actual_return_datetime TEXT,
    drop_off_branch_id INTEGER REFERENCES branch(id),
    status TEXT NOT NULL DEFAULT 'reserved',                    -- reserved/assigned/open/returned
    credit_card_name TEXT,
    fuel_level_at_pickup TEXT,
    sys_config_id INTEGER REFERENCES sys_config(id) DEFAULT 1,
    max_rental_days INTEGER,                -- Rule.copy from sys_config
    max_additional_drivers INTEGER,         -- Rule.copy from sys_config
    grace_period_hours INTEGER,             -- Rule.copy from sys_config
    location_penalty_amount NUMERIC(10,2),  -- Rule.copy from sys_config
    additional_driver_count INTEGER DEFAULT 0,   -- Rule.count of rental_driver (is_renter=0)
    barred_driver_count INTEGER DEFAULT 0,       -- Rule.count of rental_driver where person.is_barred
    rental_duration_days INTEGER DEFAULT 0,      -- Rule.formula
    base_rental_cost NUMERIC(10,2) DEFAULT 0,    -- Rule.formula
    late_return_charge NUMERIC(10,2) DEFAULT 0,  -- Rule.formula
    location_penalty_charge NUMERIC(10,2) DEFAULT 0, -- Rule.formula
    total_additional_charges NUMERIC(10,2) DEFAULT 0, -- Rule.formula
    rental_price NUMERIC(10,2) DEFAULT 0         -- Rule.formula
);

CREATE TABLE rental_driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER NOT NULL REFERENCES rental(id),
    person_id INTEGER NOT NULL REFERENCES person(id),
    is_renter INTEGER DEFAULT 0             -- 1 = the renter row, 0 = additional driver
);

CREATE TABLE bad_experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER NOT NULL REFERENCES rental(id),
    driver_id INTEGER NOT NULL REFERENCES person(id),
    description TEXT,
    occurred_datetime TEXT,
    notification_datetime TEXT
);
