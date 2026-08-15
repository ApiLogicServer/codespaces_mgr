# car_rental — provenance

- **Source prompt:** `docs/requirements/prompt.pdf` (verbatim copy, byte-identical to
  `samples/prompts/Rent Example.pdf` — OMG SBVR v1.5, Annex G "EU-Rent Example", Oct 2019, 90 pages)
- **Created:** 2026-08-01
- **Model:** Claude Sonnet 5 (Claude Code)
- **Method:** Manager CE Method 4 (System Creation Services)

## Creation steps (in order actually run)

```bash
# 1. Create from starter.sqlite (Manager root = codespaces_mgr)
genai-logic create --project-name=car_rental --db_url=sqlite:///samples/dbs/starter.sqlite

# 2. Constant extraction + FK inventory -> database/car_rental_ddl.sql, then apply
sqlite3 car_rental/database/db.sqlite < car_rental/database/car_rental_ddl.sql

# 3. Rebuild models from the altered database
cd car_rental && genai-logic rebuild-from-database --db_url=sqlite:///database/db.sqlite

# 4. Logic files (one per use case, see docs/requirements/eu_rent_rulebook/requirements.md)
#    logic/logic_discovery/eu_rent_rulebook/driver_rules.py
#    logic/logic_discovery/eu_rent_rulebook/rental_period_rules.py
#    logic/logic_discovery/eu_rent_rulebook/pickup_rules.py
#    logic/logic_discovery/eu_rent_rulebook/pricing_and_return_rules.py

# 5. Seed data (Flask context, LogicBank active)
PROJECT_DIR=$(pwd) python database/test_data/alp_init.py

# 6. Verified: server starts, JSON:API (localhost:5656/api) and Admin App
#    (localhost:5656/admin-app) both serve correctly; constraint enforcement
#    confirmed via a live POST to /api/Rental/ (see ad-libs.md).
```

## Schema decisions (Step 4a/4b — constants and FK inventory)

**SysConfig constants extracted** (every rate/threshold in the spec that would otherwise be a
hardcoded literal):

| Domain value (source) | `sys_config` column | Default |
|---|---|---|
| "It is prohibited that ... rental period is more than 90 rental days" (G.7.7) | `max_rental_days` | 90 |
| "Each rental authorizes at most 3 additional drivers" (G.6.6) | `max_additional_drivers` | 3 |
| "driver is qualified ... over 21 years old" (G.5) | `min_driver_age` | 21 |
| "grace period ... ends one hour after ... scheduled return date-time" (G.6.8.5.3) | `grace_period_hours` | 1 |
| "barred ... has at least 3 bad experiences" (G.5.1) | `bad_experience_bar_threshold` | 3 |
| location penalty charge amount (G.7.6 — amount unspecified in spec, assumed) | `location_penalty_amount` | 50.00 |

**FK inventory** (every lookup entity got an integer FK column, not a text code):
`country_id`, `operating_company_id`, `local_area_id`, `branch_id` (pickup/return/drop-off/stored-at),
`car_manufacturer_id`, `car_group_id`, `car_model_id`, `car_id`, `renter_id`/`person_id`,
`sys_config_id` on every table that reads a global constant.

**Request Pattern scan (Step 4c):** none of EU-Rent's rules involve AI, email, Kafka, or an
external API — every rule is a plain data derivation/constraint, so no `Sys*` request table was
needed.

## Scope

The full spec is 90 pages of SBVR meta-vocabulary (communities, dictionaries, formal DTV date-time
theory, enforcement-level taxonomy) intended to illustrate the SBVR *notation*, not to be a literal
schema. This project implements the concrete rental-car domain model and the rulebook's most
load-bearing behavioral rules. See `ad-libs.md` for the complete list of what was scoped out and
every simplification made within what *was* implemented.
