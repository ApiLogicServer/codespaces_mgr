# 🩺 nw_sample — Project Governance Report
**Date:** 2026-06-11
**Scoring:** Coverage Score (weighted rules / domain tables) + Integrity Score (100 - demerits) + Effective LOC
**Reference:** `docs/training/health_check.md`

---

## Summary

| Project | Tables | Wtd Rules | Coverage | Integrity | Red Flag | Effective LOC | Profile |
|---|---|---|---|---|---|---|---|
| nw_sample | 9 | 34 | **3.8** | **83** | — | **782** | 🟠 Rules in declare_logic.py — needs migration; FK indexes missing schema-wide |

> **Coverage** = weighted rules / domain tables (sum/count=3, formula/copy=2, constraint=1). Target ≥ 3.0 for mature projects.
> **Integrity** = 100 minus demerits for anti-patterns: broken dependency tracking, procedural aggregates replacing rules, events that should be rules. Target ≥ 95.
> **Red Flag** = 🚨 if ≥ 10 FK tables and zero sum/count rules — team has evidently not adopted aggregation rules.
> **Effective LOC** = code added beyond the generated scaffold, vs hardcoded baseline LOC per file (see `docs/training/health_check.md` v1.7).
> See `docs/training/governance.md` for full scoring guide.

---

## Scores

| Metric | Value | Grade |
|---|---|---|
| **Coverage Score** | **3.8** (34 pts / 9 domain tables) | 🟡 Moderate |
| **Integrity Score** | **83** (17 points deducted) | 🟠 Poor |
| **Effective LOC** | **782** | — |

---

## Coverage Detail

**Domain tables (9):** CategoryTableNameTest, Customer, Department, Employee, EmployeeAudit, Order, OrderDetail, Product, Supplier

**Excluded — system (2):** SampleDBVersion (version table), sqlite_sequence (internal)
**Excluded — lookup/junction (7):** CustomerDemographic (1 col), Location (1 col), Region (1 col), Union (1 col), EmployeeTerritory (2 cols), Shipper (2 cols), Territory (2 cols)
*(lookup threshold: ≤ 2 non-PK columns)*

**Rule inventory:**

| Rule | File | Line | Type | Weight |
|---|---|---|---|---|
| Customer.Balance ≤ CreditLimit | declare_logic.py | 106 | constraint | 1 |
| Customer.Balance = sum(Order.AmountTotal where unshipped+ready) | declare_logic.py | 110 | sum | 3 |
| Order.AmountTotal = sum(OrderDetail.Amount) | declare_logic.py | 114 | sum | 3 |
| OrderDetail.Amount = Quantity × UnitPrice | declare_logic.py | 117 | formula | 2 |
| OrderDetail.UnitPrice copy from Product.UnitPrice | declare_logic.py | 120 | copy | 2 |
| Order: cannot ship unready orders | declare_logic.py | 202 | constraint | 1 |
| Product.UnitsInStock (formula via units_in_stock) | declare_logic.py | 245 | formula | 2 |
| Product.UnitsShipped = sum(OrderDetail.Quantity where unshipped) | declare_logic.py | 247 | sum | 3 |
| OrderDetail.ShippedDate = Order.ShippedDate (cascading formula) | declare_logic.py | 251 | formula | 2 |
| Customer.UnpaidOrderCount = count(Orders where unshipped) | declare_logic.py | 255 | count | 3 |
| Customer.OrderCount = count(Orders) | declare_logic.py | 259 | count | 3 |
| Order.OrderDetailCount = count(OrderDetails) | declare_logic.py | 261 | count | 3 |
| Employee: salary raise ≤ 20% | declare_logic.py | 272 | constraint | 1 |
| Order.OrderDate = now() | declare_logic.py | 355 | formula | 2 |
| Customer.CompanyName ≠ 'x' | simple_constraints.py | 22 | constraint | 1 |
| Employee.LastName ≠ 'x' | simple_constraints.py | 26 | constraint | 1 |
| Category.Description ≠ 'x' | simple_constraints.py | 35 | constraint | 1 |
| Events (8 — after_flush, commit, early, row) | declare_logic.py | various | event | 0 |
| Integration events (2 — Kafka, n8n) | integration.py | 97–98 | event | 0 |

**Weighted total:** 3×sum(3) + 3×count(3) + 4×formula(2) + 1×copy(2) + 6×constraint(1) = 9+9+8+2+6 = **34**
**Coverage:** 34 / 9 = **3.8**

---

## Integrity Findings

| | File | Line | Finding | Points |
|---|---|---|---|---|
| 🔴 | logic/declare_logic.py | 106–355 | Rules in declare_logic.py instead of logic_discovery/ files | **-2** |
| 🟡 | declare_logic.py, integration.py | 7, 5 | Wildcard import `from database.models import *` (×2 files) | **-1** |
| 🟡 | logic/logic_discovery/ | — | Missing `__init__.py` | **-1** |
| 🟡 | database/db.sqlite | — | EmployeeTerritory.TerritoryId → Territory — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | EmployeeTerritory.EmployeeId → Employee — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Order.Country → Location — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Order.City → Location — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Order.CloneFromOrder → Order — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Department.DepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | OrderDetail.ProductId → Product — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | OrderDetail.OrderId → Order — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Employee.UnionId → Union — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Employee.OnLoanDepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Employee.WorksForDepartmentId → Department — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | Product.CategoryId → CategoryTableNameTest — no covering index | **-1** |
| 🟡 | database/db.sqlite | — | EmployeeAudit.EmployeeId → Employee — no covering index | **-1** |

**Integrity:** 100 - 2 - 1 - 1 - (13 × 1) = **83**

### Schema Check — Primary Keys

All 17 mapped tables have a primary key. **No findings.**

### Hall Passes Applied

| | File | Line | Pattern |
|---|---|---|---|
| ✅ | integration.py | 97 | `kafka-publish` — send_kafka_message call |
| ✅ | integration.py | 98 | `kafka-publish` — n8n webhook (external I/O) |
| ✅ | declare_logic.py | 176 | `row-lookup` — single `.filter().one()` in commit_row_event |

### What's Clean

- ✅ No `session.query()` inside formula functions — all queries are in events (correct)
- ✅ No `as_expression=lambda row: my_func(row)` wrapping — both lambdas are direct computations
- ✅ `units_in_stock()` calling function references `row.UnitsInStock`, `row.UnitsShipped` directly — LB tracks dependencies correctly
- ✅ No side-effect assignments inside formula functions
- ✅ No hardcoded values in rule lambdas

---

## Action Items

| Priority | Item | Fix |
|---|---|---|
| 🔴 -2 | Rules in declare_logic.py | Migrate into logic_discovery/ files by use case — see suggested structure below |
| 🟡 -1 | Wildcard imports (×2) | Replace with explicit: `from database.models import Customer, Order, OrderDetail, Product, Employee` |
| 🟡 -1 | Missing `__init__.py` | `touch logic/logic_discovery/__init__.py` |
| 🟡 -13 | 13 unindexed FK columns | `CREATE INDEX` on each FK column listed above (Order, OrderDetail, Employee, EmployeeTerritory, EmployeeAudit, Department, Product) |

### Suggested Migration Structure

```
logic/logic_discovery/
  __init__.py
  check_credit.py         ← Customer.Balance, constraint
  order_amounts.py        ← Order.AmountTotal, OrderDetail.Amount, OrderDetail.UnitPrice
  inventory.py            ← Product.UnitsInStock, Product.UnitsShipped, OrderDetail.ShippedDate
  customer_metrics.py     ← Customer.UnpaidOrderCount, Customer.OrderCount
  order_metrics.py        ← Order.OrderDetailCount, Order constraint (unready), Order.OrderDate
  employee_audit.py       ← Employee constraint (salary), audit event
  app_integration.py      ← after_flush Kafka/n8n events (already in integration.py ✅)
  simple_constraints.py   ← already correct ✅
```

This migration would raise the Integrity Score from 83 → 85 and make the rules self-documenting by use case.
The remaining -13 (FK indexes) is a schema-wide pattern across all sample projects — see governance.md for portfolio context.

---

## Effective LOC Detail

Total Effective LOC: **782** (vs hardcoded scaffold baselines; `database/models.py` excluded)

| Bucket | LOC | Detail |
|---|---|---|
| declare_logic.py growth | 270 | 361 lines vs baseline 91 |
| logic_discovery (new files) | 138 | integration.py=100, simple_constraints.py=38 (auto_discovery.py and use_case.py match baseline exactly → 0) |
| api_discovery (new files) | 243 | authentication_expose_api_models.py=52, sales_by_category.py=49, dashboard_services.py=142 |
| integration (new files) | 131 | row_dict_maps: Customer_Orders.py=31, OrderById.py=30, OrderB2B.py=36, OrderShipping.py=34 |

> Note: `security/declare_security.py` is 99 lines in both `nw_sample` and the unmodified
> `nw_sample_nocust` baseline — no growth, 0 effective lines. `api/api_discovery/openapi.py`
> (130 lines, present in nocust but not in nw_sample) is a removed scaffold file — does not
> count against Effective LOC (only additions are counted per v1.7).

**Per-table (logic_discovery LOC referencing each table — overlapping by design):**

> Note: nw_sample's rules are concentrated in `declare_logic.py` (270 effective lines, not yet
> migrated to `logic_discovery/`), so per-table attribution is not meaningful until the
> migration in Action Items is complete. The 138 new logic_discovery lines (integration.py,
> simple_constraints.py) are EAI/integration scaffolding and simple field-level constraints
> rather than per-table aggregation rules.

---

## Summary

nw_sample has **solid business logic** — 14 weighted rules across the core order/customer/inventory domain, well-structured and correctly implemented. The main organizational issue is that the rules predate the discovery pattern and live in `declare_logic.py` (270 effective lines beyond baseline). The logic itself is clean (no dependency-tracking bugs, no procedural aggregates replacing rules). Schema-check found 13 FK columns with no covering index — typical of `rebuild-from-database` scaffolding on a 17-table schema, which does not auto-create FK indexes.

**Coverage 3.8** — moderate-to-strong; the 16-table Northwind schema has several tables with no rules (Region, Territory, Shipper, Supplier, etc.) which is appropriate for a reference/demo project.
**Integrity 83** — poor, driven primarily by the 13 unindexed FK columns (a schema-wide pattern, not specific to this project's logic) plus the pre-existing organizational findings.
**Effective LOC 782** — substantial "beyond-scaffold" effort: 270 lines of business rules (declare_logic.py), 138 lines of logic_discovery integration/constraints, 243 lines of new custom API endpoints, and 131 lines of B2B/row-dict mappers.
