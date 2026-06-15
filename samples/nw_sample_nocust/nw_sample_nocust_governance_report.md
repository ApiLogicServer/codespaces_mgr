# 🩺 nw_sample_nocust — Project Governance Report
**Date:** 2026-06-11
**Scoring:** Coverage Score (weighted rules / domain tables) + Integrity Score (100 - demerits) + Effective LOC
**Reference:** `docs/training/health_check.md`, `docs/training/governance.md`

---

## Summary

| Project | Tables | Wtd Rules | Coverage | Integrity | Red Flag | Effective LOC | Profile |
|---|---|---|---|---|---|---|---|
| nw_sample_nocust | 16 | 0 | **0.0** | **87** | 🚨 | **0** | ℹ️ Intentionally empty — "new from db" reference; FK indexes missing (schema-wide) |

---

> **ℹ️ About this project**
> `nw_sample_nocust` is the reference "new from database" project — what you get immediately
> after `genai-logic create --db_url=nw`. No customization, no rules added. It exists to show
> the baseline and to contrast with `nw_sample` (same schema, rules added).
> See `../nw_sample/nw_sample_governance_report.md` for the comparison.
>
> **Effective LOC = 0 by definition** — this project's files ARE the baseline used to compute
> Effective LOC for every other project (see `docs/training/health_check.md` v1.7).

---

## Scores

| Metric | Value | Grade |
|---|---|---|
| **Coverage Score** | **0.0** (0 weighted rules / 16 tables) | 🔴 Weak |
| **Integrity Score** | **87** (13 points deducted — schema only) | 🟡 Fair |
| **Effective LOC** | **0** (this IS the baseline) | — |
| **Red Flag** | **🚨 RAISED** | 16 FK tables, zero aggregation rules |

---

## 🚨 Red Flag

**Condition met:** 10+ tables with incoming foreign keys AND zero `Rule.sum` + zero `Rule.count`

```
🚨 RED FLAG: 16 tables with child relationships, zero aggregation rules.
   Suggestion: schedule rules training or consulting engagement.
   To acknowledge: add @health-check: red-flag-suppress to use_case.py docstring.
```

**In this case the flag is expected** — this project is intentionally the pre-rules baseline.
See the contrast in `../nw_sample/nw_sample_governance_report.md`:
- nw_sample: Coverage 3.8, Integrity 83, Effective LOC 782, no red flag
- nw_sample_nocust: Coverage 0.0, Integrity 87, Effective LOC 0, Red Flag raised ← you are here

---

## Coverage Detail

**Domain tables (16):** Category, Customer, CustomerDemographic, Department, Employee,
EmployeeAudit, EmployeeTerritory, Location, Order, OrderDetail, Product, Region, Shipper,
Supplier, Territory, Union
*(SampleDBVersion excluded — system/version table)*

**Tables with incoming FKs (10):** Order, OrderDetail, Employee, EmployeeTerritory,
EmployeeAudit, Product, CustomerDemographic, Department, Territory, Location

**Rule inventory:** None. The only declaration is `Rule.early_row_event_all_classes`
for stamping/opt-locking — infrastructure, weight 0.

**Weighted total:** 0
**Coverage:** 0 / 16 = **0.0**

---

## Integrity Findings

No logic-organization demerits — there is no logic to evaluate. All findings below are
**schema-level**, identical to `nw_sample` (same database schema, unmodified).

| | File | Finding | Points |
|---|---|---|---|
| 🟡 | database/db.sqlite | EmployeeTerritory.TerritoryId → Territory — no covering index | **-1** |
| 🟡 | database/db.sqlite | EmployeeTerritory.EmployeeId → Employee — no covering index | **-1** |
| 🟡 | database/db.sqlite | Order.Country → Location — no covering index | **-1** |
| 🟡 | database/db.sqlite | Order.City → Location — no covering index | **-1** |
| 🟡 | database/db.sqlite | Order.CloneFromOrder → Order — no covering index | **-1** |
| 🟡 | database/db.sqlite | Department.DepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | OrderDetail.ProductId → Product — no covering index | **-1** |
| 🟡 | database/db.sqlite | OrderDetail.OrderId → Order — no covering index | **-1** |
| 🟡 | database/db.sqlite | Employee.UnionId → Union — no covering index | **-1** |
| 🟡 | database/db.sqlite | Employee.OnLoanDepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | Employee.WorksForDepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | Product.CategoryId → CategoryTableNameTest — no covering index | **-1** |
| 🟡 | database/db.sqlite | EmployeeAudit.EmployeeId → Employee — no covering index | **-1** |

**Integrity:** 100 - (13 × 1) = **87**

### Schema Check — Primary Keys

All 17 mapped tables have a primary key. **No findings.**
(`ProductDetails_View` is flagged by raw schema scan as having no PK — but it is a database
**VIEW**, not a mapped SQLAlchemy table, so it is excluded from this check.)

**Infrastructure present (correct):**
- ✅ `early_row_event_all_classes` — date/user stamping + opt-locking (disabled by default, correctly stubbed)
- ✅ `logic/logic_discovery/use_case.py` — discovery stub, ready for rules
- ✅ `logic/logic_discovery/auto_discovery.py` — discovery wiring in place

---

## What This Looks Like After Adding Rules

Run the health check on `../nw_sample/` to see the same schema with rules added:

| | nw_sample_nocust | nw_sample |
|---|---|---|
| Coverage Score | 0.0 | 3.8 |
| Integrity Score | 87 (schema only) | 83 (schema + organization) |
| Effective LOC | 0 (baseline) | 782 |
| Red Flag | 🚨 Raised | — None |
| Weighted rules | 0 | 34 |
| Rule.sum/count | 0 | 6 |
| Rule.formula/copy | 0 | 5 |
| Rule.constraint | 0 | 6 |

The jump from 0.0 → 3.8 coverage and red flag → no flag represents the value of
adopting rules on an existing project. The 13 unindexed FK columns are a **schema-wide**
finding present in both projects — fixing it in one (e.g., via a shared migration) fixes
it in both, since they share the same Northwind schema.

---

## Action Items

| Priority | Item | Fix |
|---|---|---|
| 🟡 -13 | 13 unindexed FK columns | `CREATE INDEX` on each FK column listed above (Order, OrderDetail, Employee, EmployeeTerritory, EmployeeAudit, Department, Product) — same fix applies to `nw_sample` |

---

## Summary

This project is **intentionally empty** — it is the correct output of `genai-logic create`
before any developer customization. The red flag is expected and informative, not a problem
to fix in this project. **Effective LOC = 0** because this project's files define the
baseline against which all other projects are measured.

The Integrity score of 87 (down from a vacuous 100) reflects 13 FK columns with no covering
index — a finding inherent to the Northwind schema as produced by `rebuild-from-database`,
not a consequence of any code written in this project. The same finding appears identically
in `nw_sample`.

Its governance value is as a **reference baseline**: a team whose production project looks
like this report has not adopted rules. A team whose production project looks like
`nw_sample` has made a solid start — at the cost of some logic-organization debt
(Integrity 83 vs 87) but with substantial added value (Effective LOC 782).
