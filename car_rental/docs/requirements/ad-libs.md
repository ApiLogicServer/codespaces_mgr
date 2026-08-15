# car_rental — ad-libs (every assumption/guess made beyond the spec)

## Scope reduction (the big one)

The source is a 90-page formal SBVR specification annex whose primary purpose is to *illustrate
SBVR notation* (communities, vocabularies, designation contexts, categorization types, the OMG
Date-Time Vocabulary) — not to be read as a literal database schema. Implementing it literally
would mean building an SBVR meta-model interpreter, not a car rental system. I extracted the
concrete business entities and the rulebook's (G.7) most illustrative behavioral rules, and
**omitted entirely**:

- **Car movements / transfers** (G.6.7): planned vs. walk-in movements, local/in-country/
  international movement, car-ownership transfer between local areas on movement. No
  `car_movement` or `car_transfer` table exists.
- **Scheduled service** (G.6.5.3, G.7.8): service depots, service scheduling, the "odometer
  reading must not exceed service_mileage + 500 miles" rule. `car.service_mileage` and
  `car.odometer_reading` columns exist but no rule reads them.
- **Insurer rule** (G.7.1): "each operating company has at least one insurer" — no `insurer` table.
- **Corporate customers / corporate rental agreements** (G.6.6): negotiated rates, accreditation
  of corporate renters. Only individual `person` renters are modeled.
- **Loyalty club / points rentals** (G.5.1, G.6.9.3): `club_point`, `points_rental_rate`,
  redemption. Only cash rentals are modeled.
- **Rental bookings as a separate entity from rentals** (G.6.8): the spec distinguishes
  `rental_booking` (the reservation) from `rental` (the resulting contract). This project
  collapses them into a single `rental` row with a `status` lifecycle (`reserved` → `assigned` →
  `open` → `returned`), rather than two linked entities.
- **Rental period non-overlap constraint** ("a renter must not have two overlapping rentals",
  G.7.7): this is a sibling-row comparison (compare this rental's date range against the same
  renter's *other* rentals), which doesn't fit LogicBank's parent/child dependency model without
  a `session.query()` inside a formula — the anti-pattern the project's own training material
  (`docs/training/logic_bank_api.md`) explicitly warns against for staleness reasons. Not
  implemented; flagging rather than building a known-stale rule.
- **Car exchange / breakdown / recovery charge** (G.6.8.5.1, G.6.8.5.5): not modeled.
- **Vehicle sale at end of rental life**, **currency conversion**, **multi-language vocabulary**
  (G.6.2, G.6.9.5, G.8): not modeled — single currency, single language.
- **Enforcement-level taxonomy** (G.8.6 — strict/deferred/pre-authorized/post-justified/override/
  guideline): the spec models *how strictly* each rule is enforced (e.g. some allow manager
  override with justification). Every rule here is enforced as a hard `Rule.constraint`
  (equivalent to "strict"), regardless of the spec's stated enforcement level for that rule.

## Simplifications within what IS implemented

- **Driver qualification** (G.7.3): spec says "over 21 years old, has a current driver license,
  and is not under any pending legal action that could adversely affect his license or
  insurability." Implemented: age ≥ `min_driver_age` and license not expired. The "pending legal
  action" clause has no data source in this schema and is not checked.
- **Grace period** (G.6.8.5.3): spec defines grace period end as "one hour after scheduled return,
  **or branch closing time, whichever is earlier**." Implemented: fixed `grace_period_hours`
  after scheduled return only — branch hours-of-operation are not modeled, so the "whichever is
  earlier" comparison is dropped.
- **Late return charge** (G.6.8.5.3): spec has a tiered tariff — hourly rate for up to 5 hours
  late, then daily rate for 5–24 hours late, with a 48-hour stolen-vehicle report threshold.
  Implemented: flat `car_group.rental_hour_rate × late_hours` for any lateness — no tier switch,
  no 48-hour stolen-report logic.
- **Rental pricing / RTU calculation** (G.6.9.3): spec has a cascading rental-time-unit calculation
  (rental_month → rental_week → rental_3_days → rental_day, each with its own rate, per car group
  per operating country). Implemented: `base_rental_cost = rental_duration_days ×
  car_group.rental_day_rate` — a single day rate, no week/month discount tiers, and rates are
  global (not per-country as the spec's `RTU has rental rate` / `operating_country has rental rate`
  design implies).
- **Location penalty amount**: the spec establishes that a location penalty charge *exists* but
  never states its amount. Assumed flat `sys_config.location_penalty_amount = 50.00`.
- **Credit card**: modeled as a single free-text `credit_card_name` column (name on the card) —
  no card number, expiry, or actual payment-gateway integration; "provisionally charged" is
  represented only as "a non-blank name is present," not an actual charge/authorization.

## Known limitation surfaced during verification

The renter of a rental is **not** automatically inserted as an authorized driver
(`rental_driver` row with `is_renter=1`) when a `Rental` is created via a raw API POST — this
project models it as a separate related-resource insert (as the seed data does), matching how a
real booking UI would submit both resources together. A `POST /api/Rental/` with `status: "open"`
and no accompanying `RentalDriverList` insert will **not** trigger the driver-qualification or
barred-driver constraints, because those constraints are declared on `RentalDriver`/counted from
it, and none exists yet. Verified live: creating such a rental for the barred driver (David,
person id 4) via `curl POST` succeeded (201) where the seed script's equivalent case — which does
insert the `RentalDriver` row in the same transaction — correctly fails. The row was deleted after
the test to keep seed data clean. A production version would add an `early_row_event` on
`Rental` insert that auto-creates the renter's `RentalDriver` row, matching the spec's actual
intent ("The renter ... must be authorized as a driver for that rental").
