# eu_rent_rulebook — requirements

Source: OMG SBVR v1.5, Annex G "EU-Rent Example" (`docs/requirements/prompt.pdf`).
Verbatim excerpts implemented as LogicBank rules in `logic/logic_discovery/eu_rent_rulebook/`.

## G.7.3 Rule Set -- Driver Rules

> It is obligatory that each driver who is authorized for a rental is qualified.
> ... "driver is qualified": the driver is over 21 years old and has a current driver license
> and is not under any pending legal action that could adversely affect his driver license or
> insurability. [simplified to: age >= min_driver_age and license not expired]

> It is prohibited that a rental is open if a driver who is authorized for the rental is barred.
> ... "driver being barred": a person known to EU-Rent as a driver ... who has at least 3 bad
> experiences.

> Each rental authorizes at most 3 additional drivers. [G.6.6 `rental authorizes additional driver`]

Implemented in: `logic/logic_discovery/eu_rent_rulebook/driver_rules.py`

## G.7.7 Rule Set -- Rental Period Rules

> It is prohibited that the duration of each rental period is more than 90 rental days.

Implemented in: `logic/logic_discovery/eu_rent_rulebook/rental_period_rules.py`

## G.7.2 / G.7.5 -- Charging and Pick-up Rules

> It is obligatory that an estimated rental price of an open rental is provisionally charged to a
> credit card that is in the name of the renter who is responsible for the rental.

> At the actual pick-up date-time of a rental it is obligatory that the fuel level of the rented
> car of the rental is full.

Implemented in: `logic/logic_discovery/eu_rent_rulebook/pickup_rules.py`

## G.7.6 Rule Set -- Return Rules, G.6.9 Rental Pricing

> If the actual return date-time of a rental is after the end date-time of the grace period of the
> rental then it is obligatory that the rental incurs a late return charge.
> ... The grace period of a rental ends one hour after the rental's scheduled return date-time or
> at close of business of the return branch, whichever is earlier. [simplified: fixed grace_period_hours,
> branch closing time not modeled]

> It is obligatory that a rental incurs a location penalty charge if the drop-off branch of the
> rental is not the return branch of the rental.

> Rental prices start with a base price ... based on rental time units (RTUs) ... For each RTU
> there are rates ... for each car group. [simplified: base_rental_cost = rental_duration_days x
> car_group.rental_day_rate; the full RTU month/week/3-day/day tiered calculation and per-country
> rate matrix from G.6.9.3 are not implemented]

Implemented in: `logic/logic_discovery/eu_rent_rulebook/pricing_and_return_rules.py`

See `docs/requirements/prompt.pdf` for the complete original document; see
`../../ad-libs.md` for every simplification and omission made against the full spec.
