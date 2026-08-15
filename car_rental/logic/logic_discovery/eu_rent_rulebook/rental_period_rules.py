"""
Rental Period Rules (SBVR Annex G, G.7.7 Rule Set -- Rental Period Rules)

It is prohibited that the duration of each rental period is more than 90 rental days.
(max_rental_days is a SysConfig constant)

version: 1.0
"""

from logic_bank.logic_bank import Rule
from database import models
from datetime import date


def declare_logic():

    Rule.copy(derive=models.Rental.max_rental_days, from_parent=models.SysConfig.max_rental_days)

    def _rental_duration_days(row: models.Rental, old_row, logic_row):
        """Derive rental_duration_days: whole days between pickup and return (actual if set, else scheduled)."""
        start = row.actual_pickup_datetime or row.scheduled_pickup_datetime
        end = row.actual_return_datetime or row.scheduled_return_datetime
        start_date = date.fromisoformat(start[:10])
        end_date = date.fromisoformat(end[:10])
        days = (end_date - start_date).days
        return days if days > 0 else 1
    Rule.formula(derive=models.Rental.rental_duration_days, calling=_rental_duration_days)

    Rule.constraint(validate=models.Rental,
                     as_condition=lambda row: row.rental_duration_days <= row.max_rental_days,
                     error_msg="rental duration ({row.rental_duration_days} days) exceeds "
                               "the maximum of {row.max_rental_days} rental days")
