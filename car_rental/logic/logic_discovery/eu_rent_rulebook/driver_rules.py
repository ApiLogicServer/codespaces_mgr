"""
Driver Rules (SBVR Annex G, G.7.3 Rule Set -- Driver Rules)

1. It is obligatory that each driver who is authorized for a rental is qualified.
   (driver is qualified: over min_driver_age and has a current, non-expired driver license)
2. It is prohibited that a rental is open if a driver who is authorized for the rental is barred.
   (a barred driver is one with at least bad_experience_bar_threshold bad experiences)

version: 1.0
"""

from logic_bank.logic_bank import Rule
from database import models
from datetime import datetime, date


def declare_logic():

    Rule.copy(derive=models.Person.min_driver_age, from_parent=models.SysConfig.min_driver_age)
    Rule.copy(derive=models.Person.bad_experience_bar_threshold, from_parent=models.SysConfig.bad_experience_bar_threshold)

    def _is_qualified(row: models.Person, old_row, logic_row):
        """Derive is_qualified: 1 if driver is at least min_driver_age and license is not expired."""
        birth = date.fromisoformat(row.birth_date)
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        expiry = row.driver_license_expiry
        license_ok = (expiry is None) or (date.fromisoformat(expiry) >= today)
        return 1 if (age >= row.min_driver_age and license_ok) else 0
    Rule.formula(derive=models.Person.is_qualified, calling=_is_qualified)

    Rule.count(derive=models.Person.bad_experience_count, as_count_of=models.BadExperience)

    Rule.formula(derive=models.Person.is_barred,
                 as_expression=lambda row: 1 if row.bad_experience_count >= row.bad_experience_bar_threshold else 0)

    Rule.constraint(validate=models.RentalDriver,
                     as_condition=lambda row: row.person.is_qualified == 1,
                     error_msg="driver {row.person.first_name} {row.person.last_name} is not qualified "
                               "(must be at least min_driver_age with a current driver license)")

    Rule.count(derive=models.Rental.barred_driver_count, as_count_of=models.RentalDriver,
               where=lambda row: row.person.is_barred == 1)

    Rule.constraint(validate=models.Rental,
                     as_condition=lambda row: row.status != 'open' or row.barred_driver_count == 0,
                     error_msg="rental cannot be open - a driver authorized for the rental is barred")

    Rule.copy(derive=models.Rental.max_additional_drivers, from_parent=models.SysConfig.max_additional_drivers)

    Rule.count(derive=models.Rental.additional_driver_count, as_count_of=models.RentalDriver,
               where=lambda row: row.is_renter == 0)

    Rule.constraint(validate=models.Rental,
                     as_condition=lambda row: row.additional_driver_count <= row.max_additional_drivers,
                     error_msg="rental authorizes at most {row.max_additional_drivers} additional drivers")
