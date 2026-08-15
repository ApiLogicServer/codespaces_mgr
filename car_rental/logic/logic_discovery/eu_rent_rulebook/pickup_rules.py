"""
Rental Pick-up Rules (SBVR Annex G, G.7.2 and G.7.5)

- It is obligatory that an estimated rental price of an open rental is provisionally charged
  to a credit card that is in the name of the renter who is responsible for the rental.
- At the actual pick-up date-time of a rental it is obligatory that the fuel level of the
  rented car of the rental is full.

version: 1.0
"""

from logic_bank.logic_bank import Rule
from database import models


def declare_logic():

    Rule.constraint(validate=models.Rental,
                     as_condition=lambda row: row.status != 'open' or (
                         row.credit_card_name is not None and row.credit_card_name != ''),
                     error_msg="an open rental must have an estimated rental price provisionally "
                               "charged to a credit card in the name of the renter")

    Rule.constraint(validate=models.Rental,
                     as_condition=lambda row: row.status != 'open' or row.fuel_level_at_pickup == 'full',
                     error_msg="the fuel level of the rented car must be full at pick-up")
