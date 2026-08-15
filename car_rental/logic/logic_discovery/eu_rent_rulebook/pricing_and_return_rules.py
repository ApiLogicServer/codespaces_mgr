"""
Return and Pricing Rules (SBVR Annex G, G.7.6 Rule Set -- Return Rules, G.6.9 Rental Pricing)

- If the actual return date-time of a rental is after the end date-time of the grace period
  of the rental then it is obligatory that the rental incurs a late return charge.
- It is obligatory that a rental incurs a location penalty charge if the drop-off branch of
  the rental is not the return branch of the rental.
- Base rental cost is the rental duration times the car group's rental day rate; rental price
  is the base rental cost plus additional charges (late return + location penalty).

version: 1.0
"""

from logic_bank.logic_bank import Rule
from database import models
from datetime import datetime, timedelta
from decimal import Decimal


def declare_logic():

    Rule.copy(derive=models.Rental.grace_period_hours, from_parent=models.SysConfig.grace_period_hours)
    Rule.copy(derive=models.Rental.location_penalty_amount, from_parent=models.SysConfig.location_penalty_amount)

    def _late_return_charge(row: models.Rental, old_row, logic_row):
        """Derive late_return_charge: hourly rate x hours past the grace period end, else 0."""
        actual_return_value = row.actual_return_datetime
        if actual_return_value is None:
            return Decimal('0')
        actual_return = datetime.fromisoformat(actual_return_value)
        scheduled_return = datetime.fromisoformat(row.scheduled_return_datetime)
        grace_end = scheduled_return + timedelta(hours=row.grace_period_hours)
        if actual_return <= grace_end:
            return Decimal('0')
        late_hours = Decimal((actual_return - grace_end).total_seconds() / 3600).quantize(Decimal('1'), rounding='ROUND_UP')
        return late_hours * row.car_group.rental_hour_rate
    Rule.formula(derive=models.Rental.late_return_charge, calling=_late_return_charge)

    Rule.formula(derive=models.Rental.location_penalty_charge,
                 as_expression=lambda row: row.location_penalty_amount
                 if (row.drop_off_branch_id is not None and row.drop_off_branch_id != row.return_branch_id)
                 else Decimal('0'))

    Rule.formula(derive=models.Rental.base_rental_cost,
                 as_expression=lambda row: row.rental_duration_days * row.car_group.rental_day_rate)

    Rule.formula(derive=models.Rental.total_additional_charges,
                 as_expression=lambda row: row.late_return_charge + row.location_penalty_charge)

    Rule.formula(derive=models.Rental.rental_price,
                 as_expression=lambda row: row.base_rental_cost + row.total_additional_charges)
