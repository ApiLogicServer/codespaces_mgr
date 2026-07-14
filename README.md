<!--
title: Welcome - see end for instructions to hide this
Description: Instant mcp-enabled microservices, standard projects, declarative business logic
Source: docs/Manager-readme
version info: 17.02.06 (07/09/2026)
do_process_code_block_titles: True
Used: Manager Readme (via copy_md())
demo_customs: Customs-readme
demo_customs_surtax: Customs-readme-surtax
demo_kafka: Sample-Integration
demo_allo: Sample_Allo_Dept_GL_readme
demo_ai_rules: Sample-ai-rules
demo_mcp_send: Sample-Basic-Demo-MCP-Send-Email
demo_emp_types: Sample-Types
demo_eai: Sample-Basic-EAI
demo_vibe: Sample-Basic-Demo-Vibe
demo_copilot_mcp_discovery: Sample-ai-mcp
basic_demo: Sample-Basic-Demo
codespaces_patch: |
  create_codespaces_mgr.py injects a Codespaces-only browser note immediately after
  the "## 🚀 First Time Here?" heading (sentinel: do not rename that heading without
  updating the matching logic in create_codespaces_mgr.py). The note warns Safari users to
  switch to Chrome/Edge. This avoids forking the README for Codespaces.
-->

# Welcome to GenAI-Logic

### Governed Executable Requirements

One prompt, or your existing database, **builds a working API and Admin App**, then you declare business logic **you can read, trust, and maintain** — *5 rules instead of ~200 lines of code*.

<details markdown>
<summary>The Key Idea: Combine AI with Declarative Logic</summary>

<br>Leverage AI for what it's great at — database design, data mapping, and more. Your AI assistant does the translation: plain English, Gherkin, even actual regulation text — it reads your business logic and translates it into rules, not code.

You'll see the enforcement yourself in a few minutes: those rules run at **one commit point**, no matter which path the transaction came in on — API, MCP, agent, Kafka. **No bypass.**

And you're not alone throughout: ask your AI assistant anything — architecture, rules, debugging, deployment, or how the system works.

</details>

<br>

This is the start page for the [GenAI-Logic Manager](https://apilogicserver.github.io/Docs/Manager) — where you manage projects, create notes and resources, etc.

&nbsp;

## 🤖 AI Assistance

**Check the Chat panel's title bar or model picker actually says Copilot** before continuing — VS Code's Chat panel can be backed by different extensions (Copilot, Claude Code, Gemini, Codex, etc.), and `/agent` is a Copilot-only command; other extensions will silently ignore it and fall back to their own default model instead of erroring.

**Once you've confirmed Copilot Chat is active, type this and press Enter:**

```
/agent .github/agents/genai-logic-manager.agent.md
```

That's it — GenAI-Logic Manager will greet you and ask what you want to build, using Claude Sonnet 5 (falling back to 4.6, then 4.5, if 5 isn't on your plan yet). No "Please load" needed; the model is picked automatically.

<details markdown>
<summary>Why: pins the model to Claude Sonnet 5 and pre-loads instructions</summary>

&nbsp;

This workspace ships a custom **GenAI-Logic Manager** agent — it prefers **Claude Sonnet 5** and pre-loads the project's instructions automatically, no extra step needed. "Ask" mode will not work — GenAI-Logic Manager needs to create files and run commands.

If `/agent` isn't recognized by your Copilot version, select **Agent** mode, pick **Claude Sonnet 5.0/4.6** from the model picker, then paste:

```
Please load `.github/copilot-instructions.md`.
```

For more information, see [AI-Enabled Projects](https://apilogicserver.github.io/Docs/Project-AI-Enabled/) or [click here](https://apilogicserver.github.io/Docs/Manager-readme/).

</details>

&nbsp;

## 🚀 First Time Here?
<!-- CODESPACES-INSERT-POINT: create_codespaces_mgr.py injects browser note here — do not rename this heading -->
&nbsp;

You're already running in GitHub Codespaces — a cloud VS Code environment in your browser. Nothing to install. (Use Chrome or Edge — Safari has known compatibility issues with VS Code in the browser.)


<details markdown>
<summary>The Ideal — executable business prompts, held to an enterprise standard</summary>

<br>Say this to your AI assistant (allow several minutes):

```
Create basic_demo from samples/dbs/basic_demo.sqlite (customers, orders, products).

Include a notes field for orders.

On Placing Orders, Check Credit    
    1. The Customer's balance is less than the credit limit
    2. The Customer's balance is the sum of the Order amount_total where date_shipped is null
    3. The Order's amount_total is the sum of the Item amount
    4. The Item amount is the quantity * unit_price
    5. The Item unit_price is copied from the Product unit_price

Use case: App Integration
    1. Publish the Order to Kafka topic 'order_shipping' when the date_shipped is not None.
```

<details markdown>
<summary>Starting from a new database instead?</summary>

&nbsp;

The prompt above starts from an existing database — the common real-world case, and much faster (no schema design step). You *could* have AI design a new database from scratch instead — drop the `from samples/dbs/basic_demo.sqlite` clause from the first line above (allow 8-10 mins).

</details>

&nbsp;

> **Running in Codespaces?** During project creation, a browser tab may auto-open (or offer to) showing it running — safe to decline or dismiss.

The goal here isn't a demo — it's an **enterprise-class** system you can trust and maintain. That's exactly what gets tested next.

</details>

&nbsp;

<details markdown>
<summary>AI is great — but logic-as-code is hard to Read, Trust, and Maintain — here's why</summary>

<br>AI is genuinely good at UI, data mapping, boilerplate, etc — no argument there. **Business logic is the exception.**

Most developers estimate it requires about **half the development and debugging effort** on a real system — not a side concern.

Left unguided, any AI assistant — including the one that just built basic_demo for you — would default to procedural code for logic like this. Ask it directly, and you get three problems:

- **Not readable.** [procedural/credit_service.py](samples/basic_demo_logic_gov/logic/procedural/credit_service.py) — ~200 lines for those same 5 requirements. Open it and judge for yourself.
- **Not trustworthy.** The procedural version shipped 2 real bugs — found only by specifically testing what happens when a row is reparented to a new owner: [the A/B test](samples/basic_demo_logic_gov/logic/procedural/declarative-vs-procedural-comparison.md). Root cause: **path confusion** — procedural code must enumerate every change path (insert, update, delete, reparent) by hand, and it's easy to miss one.
- **Not maintainable.** Every future change means re-checking every execution path *and* getting the order right, by hand, again. Root causes: **path confusion** and **manual ordering** — the same problem as above, back for round two. Honestly? At some point you'd stop checking and just hope testing catches it.

Even when AI generates procedural code that happens to work today, there's a governance problem underneath: nobody can audit ~200 lines of event-handler logic at a glance — not the next developer, not compliance, not you in six months.

Even at ~200 lines for just 5 requirements, this wasn't just hard to read — it had bugs in it. Now picture a real system: 10-20X the requirements of this example, and proportionally more procedural code to match. At that scale, an auditor can't read it all — they can only sample, and hope. **Unreadable at scale is ungovernable at scale.**

There's a structural problem underneath the bugs, too: procedural code cannot represent transitive dependencies reliably. The AI diagnosed this itself, unprompted:

> *"Business logic is not a coding problem. It's a dependency graph problem."*

That's not a capability gap. No amount of AI capability fixes a representation problem.

**We're deeply impressed with AI — this is about closing the one gap it has: logic.** That's next.

</details>

&nbsp;

<details markdown>
<summary>AI-driven rules are easy to Read, Trust, and Maintain — here's how</summary>

&nbsp;

<details markdown>
<summary>&emsp;&emsp;1. Run it — see the API and logic operate</summary>

<br>You've probably used AI to generate code before — so what's different here?

**Difference 1: it produces models, not code.** Run the basic_demo prompt above, and instead of a pile of procedural code, you get artifacts that declare structure or policy rather than procedure — same 5 requirements, same AI:

1. **Data model** — `database/models.py`
2. **Full JSON:API** — Swagger, pagination, optimistic locking (`api/expose_api_models.py` — 52 lines, zero per-table code)
3. **Admin App** — multi-table, with navigations and lookups (`ui/admin/admin.yaml` — simple YAML, not HTML/JS)
4. **Business logic** — [logic_discovery/place_order/check_credit.py](samples/basic_demo_logic_gov/logic/logic_discovery/place_order/check_credit.py) — 5 rules (~40X less), same requirements, same AI, 0 bugs

**Difference 2: the logic itself is declarative** — more on why that matters below.

Each small, readable, yours. Plain Python — standard tooling applies. Security is opt-in, not default — bootstrap RBAC anytime with `genai-logic add-auth`.

**See it running:** Press F5 using "API Logic Server Run (run project from manager)", and open the Admin App. Explore the API via Swagger, browse the data, and follow the relationships — all auto-generated from the data model.

Now trigger it: open an **unshipped** Order for Alice, edit the Widget item:

```
Change the quantity to a very large number. Save.
```

<details markdown>
<summary>&emsp;&emsp;Detail Instructions -- Screen Shots</summary>

<br>Alter the quantity for an *unshipped* item:

1. Show the Customer List
2. Show the first Customer
3. Show first Order
4. Edit the Item
5. Set the quantity

![credit-check](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/basic_demo/credit-check.png?raw=true?raw=true)

</details>

<br>

The save fails — note the dialog. Why? Let's look.

</details>

&nbsp;

<details markdown>
<summary>&emsp;&emsp;2. Debug it — standard logging, standard debugger</summary>

<br>No new tools required. The rule chain that just fired is in the log — plain text, readable in your terminal or editor: [sample trace](samples/basic_demo_logic_gov/logs/als-sample.log). A live run writes the same thing to the standard log, `logs/als.log`.

Every rule is a plain Python function or lambda. Set a breakpoint on any `calling=` function or `as_condition=` lambda in your IDE, exactly like you would anywhere else in the codebase — no proprietary debugger, no special UI.

![logic-debug](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/logic/logic-debug.png?raw=true)

</details>

&nbsp;

<details markdown>
<summary>&emsp;&emsp;3. Iterate — 1 AI prompt adds table, relationship, 2 rules</summary>

<br>Ask your AI assistant for a new rule, in plain English:

```
Customers should not be able to create new orders if they have unresolved past due letters.
```

There was no `Letter` table in the model — the AI adds it, relates it to `Customer`, and declares a `count` + a `constraint`. One sentence creates a schema change and two new rules — automatically integrated with the 5 already there. No need to open `check_credit.py` to find where this belongs, or trace the other rules to check for conflicts: **maintainable**, demonstrated, not asserted.

Without the engine, an AI rewriting procedural code from scratch would have to re-read and re-touch every existing rule to check for dependencies — more surface area for a missed path, more tokens spent doing it. At 5 rules that's a nuisance; **at 500, the re-read is the bottleneck and the missed-path risk compounds.** Here, the engine resolves dependencies at load time, so adding this rule doesn't touch the rest — no regeneration, no regression risk, at any scale.

</details>

&nbsp;

<details markdown>
<summary>&emsp;&emsp;4. Important Observations — no calling, no ordering, since rules are declarative</summary>

<br>Iteration was remarkably similar to traditional maintenance, because **rules are declarative:**

- **No need to call the new logic.** Rules are invoked automatically - regardless of the originating path.  You can **trust** that they'll always run.
- **Order doesn't matter.** Open `check_credit.py` and shuffle the five rules into any order you like. Rerun — still correct. Try that with 200 lines of procedural code.  You can **trust** that they'll run in the right order.
- **You got more than you asked for.** The original requirement said *"On Placing Orders, Check Credit"* — insert time. But the save that failed was an *edit* to an existing order. Nobody wrote an update-time check.

Functions don't behave like that. So why is that?

> **Traditional logic is procedural** — you own *how*: when it's called, and in what order. **Declarative logic — rules** — is about *what*, not how: you state the fact, and the system takes responsibility for invocation and ordering. That's why the new rule didn't need to be called, and why order didn't matter.

The next section explores this in detail. Ask your AI assistant — *"What are rules?"* — or keep reading.

</details>

&nbsp;

<details markdown>
<summary>&emsp;&emsp;5. What Rules Are — and how they make logic easy to Read, Trust, and Maintain</summary>

<br>**Rules** enforce business policy — multi-table derivations, constraints, and actions like messaging. **LogicBank**, the rule engine, hooks SQLAlchemy's commit event to run them on every transaction — authored as plain Python functions in `logic/logic_discovery/`, readable, version-controlled, owned like any other source file.

**How it works:**
1. **At startup** — rules load, and the engine computes their dependency graph once.
2. **At commit** — for each transaction, the engine finds the rules relevant to what changed, and fires them in the right order.

Unlike procedural code, they're **declarative** — solving exactly the three problems raised above (AI great, but hard to Read, Trust, and Maintain):

| Property | What it means | Why it matters |
|---|---|---|
| **Readable** | 5 lines, one per requirement — declared once, e.g. `Customer.balance = sum of unpaid orders` | No archaeology needed to see what it does |
| **Trustworthy** | Rules fire at every commit, from every caller — you never call them | Can't be forgotten, can't be bypassed |
| **Maintainable** | Dependency order is computed once, automatically | Add a rule anywhere, it finds its place |

> Think of a **spreadsheet:** `B10 = SUM(B1:B9)` isn't called, it *reacts* — change any input cell, it recalculates. Rules react the same way to changes in what they depend on.

That's why order didn't matter — the engine computes it, not your source file — and why the edit was caught: it fires at every commit, from every caller, not just the one you wrote it for.

> With procedural code, even if you find the right passage — how do you know it's called for *every* transaction source? API, MCP, agent, Kafka, a future caller you haven't written yet? With thousands of code paths, you can't know. That's not a testing gap; it's a representation problem. Rules solve it structurally — declared once, fired at one commit point, from every caller, with no bypass possible. The 40x reduction in code isn't the point. The verifiable coverage is: ***you can read the rules, and trust they are being enforced. Always.***

<details markdown>
<summary>How this works: Context Engineering (CE) + a commit-time rules engine</summary>

<br>Two things have to be true for this to work:

**Step 1 — Context Engineering trains the AI to write rules, not code.** That same AI, left unguided, would have produced the ~200 buggy lines from earlier. Writing rules instead wasn't its own idea — it was told to, in detail, by **Context Engineering** — the same files driving this conversation right now:

- **Directs rules, not code.** When you ask for business logic, CE steers the AI toward the *right* rule type (sum vs. count vs. Allocate vs. Request Pattern) for what you actually asked for, instead of letting it default to the procedural code it's seen a million times in training.

- **Trains the AI to automate everything above, and to help you when it breaks.** EAI's 2-message Kafka pattern, the AI/Request Pattern wiring, Executable Requirements' pre-coding schema assessment — all of it is documented training material (`docs/training/*`) the AI reads *before* writing your code, not generic knowledge it's guessing from. Ask "what are rules?" or "how do rules work?" — or, without an AI handy, just read [samples/basic_demo_logic_gov/logic/readme_logic.md](samples/basic_demo_logic_gov/logic/readme_logic.md) — same material.

- **Answers your own questions, too.** Same materials, same AI — ask it directly:
    - Is this really infrastructure, like a database?
    - Is this a black box? How do I debug a rule chain?
    - What does it take to migrate off this if we ever wanted to?
    - How does this perform at scale?
    - What does this integrate with — APIs, workflows, agents, MCP?
    - Does this work with my existing database?

  More background: [Eval Guide](https://apilogicserver.github.io/Docs/Eval/).

  <details markdown>
  <summary>The AI was trained on this material — can you trust its answers?</summary>

  <br>Don't take them on faith. Ask the same question a different way, or ask something not covered here — like where this architecture breaks down. If it just recites the same lines back, you've caught it. If it reasons, that's the test passing.

  </details>

Put together: once the AI knows how the system works, it doesn't just generate rules instead of code — it helps you debug them, and helps you understand them. A design assistant, not just a coding assistant.

**Step 2 — the rules engine runs the rules.** Rules aren't called from your code — they're wired into a single SQLAlchemy `before_flush` listener, loaded once at server start as described above. Every write, from any path — API, custom endpoint, Kafka consumer, agent — passes through that one listener before it commits. No bypass — there's no second door.

</details>

<br>

Full writeup: [declarative/procedural comparison](samples/basic_demo_logic_gov/logic/procedural/declarative-vs-procedural-comparison.md).

</details>

</details>

&nbsp;

<details markdown>
<summary>Scaling to the Enterprise — here's how</summary>

<br>With logic off its plate, AI can create remarkable results — solid enterprise systems, from requirements, not just demos that become tech debt.

**We add key *enterprise architecture* integration:**

- **Enterprise Integration (EAI)** — the demo above showed ***Publish** the Order to Kafka topic*. For the **subscribe** side, see [samples/basic_demo_eai/readme.md](samples/basic_demo_eai/readme.md): B2B orders from partner systems, via a Custom API or Kafka subscriber, including *lookups* so partners send `"Account": "Alice"` (not internal IDs).

- **MCP** — your API is **MCP-discoverable** out of the box (`/.well-known/mcp.json`).
Copilot, Claude, or ChatGPT can find the schema and answer natural-language queries against it.  There's no discovery layer for you to write — see [samples/basic_demo_ai_rules-supplier/readme_ai_mcp.md](samples/basic_demo_ai_rules-supplier/readme_ai_mcp.md)

- **AI Rules** — rules that call AI for genuinely judgment-call decisions (e.g. picking a supplier under disrupted shipping lanes).  Such AI "proposals" are governed by the deterministic rules to ensure results conform to business policy — see [samples/basic_demo_ai_rules-supplier/readme.md](samples/basic_demo_ai_rules-supplier/readme.md)

- **Custom UIs, safely** — Vibe tools (Cursor, v0, etc.) generate the UI; it's built against the same governed API, so the logic runs the same regardless of what's calling it — `genai-logic genai-add-app --vibe`.

- **Governance you can prove, not just assert** — three reports, generated from the running system, not hand-written:
    - **[Logic flow diagram](samples/basic_demo_logic_gov/docs/requirements/logic_flow_basic_demo_logic_gov.md)** — NL requirement, dependency diagram, and rule summary, for every rule chain
    - **[Ad-libs report](samples/basic_demo_logic_gov/docs/requirements/ad-libs.md)** — every assumption the AI made beyond the spec, so you know exactly what to verify
    - **[Health check](samples/basic_demo_logic_gov/docs/requirements/health_check.md)** — rule adoption, dependency-tracking integrity, missing docstrings, across the whole project

    A compliance reviewer can check the implementation in minutes, not by reading code.

    <img src="samples/basic_demo_logic_gov/docs/requirements/logic_diagrams/logic_diagram.svg" alt="Logic diagram: Item/Order/Customer rule chain, generated from the running rules" width="480">


That combination — AI, logic automation, and that enterprise architecture — is what enables ***Executable Requirements***: AI building real enterprise-class systems, from formats you already are familiar with, not a new syntax to learn:

- **Gherkin-style scenarios** — [business description](samples/demo_customs_clvs/readme.md), and the [actual requirements](samples/demo_customs_clvs/docs/requirements/customs_demo/requirements.md) used by AI to create the system.

- The **short prompt that built a system straight from an actual government tariff regulation** (Canada, CBSA) — [the prompt](samples/demo_customs_surtax/readme.md), and [the rules it produced](samples/demo_customs_surtax/logic/logic_discovery/cbsa_steel_surtax.py)

    > So, simply by referencing the regs, you get a complete enterprise system — including governed logic you can audit, trust, and maintain. AI implements the spec end-to-end and reports an **ad-libs list** — every decision it made beyond what the spec said — so you know exactly where it guessed.

&nbsp;

<img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/architecture/logic-architecture-exec.png?raw=true" alt="Design and Runtime funnels into one governed Rules Engine" height="380" width="380" align="right">

The architecture that makes this work: two funnels, converging on one engine. All requirement formats, and all transaction sources, passing through **the same commit point. No bypass.**

**What AI delivers, once logic is off its plate: entire, *governed* systems from requirements** — not just code that becomes instant tech debt. It is this approach that **caught an 8-figure compliance exposure** a major logistics company's hand-coded system missed for months. [Full writeup →](https://apilogicserver.github.io/Docs/Tech-Ent-AI)

</details>

&nbsp;

<details markdown>
<summary>Go deeper — 30-45 min guided tour</summary>

&nbsp;

**Create basic_demo** (auto-opens with guided tour option):
```bash
genai-logic create --project_name=basic_demo --db_url=sqlite:///samples/dbs/basic_demo.sqlite
```

**Inside the project:** Say to your AI assistant: *"Guide me through basic_demo"* (30-45 min hands-on tour).

> Teaches API creation, declarative rules, security, and Python customization. Fail-safe — scripts ensure no coding errors.

</details>

&nbsp;

&nbsp;

## 📚 Build It Yourself — Demo Catalog

The section above showed you pre-built samples to browse. These are the same use cases, but as commands you run yourself — paste one into your AI assistant and it builds that project for you, live.

> Tip: every project is AI-enabled — once it's built, ask your AI assistant how it works

&nbsp;

## 1. Strategic Use Cases (From [genai-logic.com](https://www.genai-logic.com))

Explore the key use cases from our home page:


| Use Case | Say to your AI / Run | What You'll Learn |
|----------|---------|-------------------|
| **[Allocation with AI Rules](samples/allocate_dept_account_demo/docs/requirements/logic_flow_allocate_dept_account_demo.md)** <br> demo_allo_dept_gl | create demo_allo_dept_gl from samples/prompts/allocation.prompt.md <br> or genai-logic create --project_name=demo_allo_dept_gl --db_url=sqlite:///samples/dbs/starter.sqlite | - [Cascade Allocation (Costs to Depts/GL)](https://apilogicserver.github.io/Docs/Sample_Allo_Dept_GL_full) <br> - AI Rules for fuzzy match to project |
| **[Use Case 1: AI Rules](samples/basic_demo_ai_rules-supplier/readme.md)**<br> demo_ai_rules_supplier | genai-logic create --project_name=demo_ai_rules_supplier --db_url=sqlite:///samples/dbs/basic_demo.sqlite | - Use AI Rules (req pattern) to choose Optimal Supplier, per world conditions |
| **[Use Case 2: Governed MCP Server](https://apilogicserver.github.io/Docs/Sample-Basic-Demo-MCP-Send-Email)** <br>demo_mcp_send_email | genai-logic create --project_name=demo_mcp_send_email --db_url=sqlite:///samples/dbs/basic_demo.sqlite | - Bus Users compose new service to send email to overdue customers, subject to email opt-out rules<br>- Create custom API with NL<br>- Create an email service (req pattern) |
| **[EAI: Enterprise App Integration](samples/basic_demo_eai/readme.md)** <br>demo_eai | genai-logic create --project_name=demo_eai --db_url=sqlite:///samples/dbs/basic_demo.sqlite | - Executable Requirements<br>- Create custom API with NL<br>- Create Kafka Listener with NL |
| **[Use Case 4: Vibe Dev Backend](https://apilogicserver.github.io/Docs/Sample-Basic-Demo-Vibe)** <br> demo_vibe | genai-logic create --project_name=demo_vibe --db_url=sqlite:///samples/dbs/basic_demo.sqlite | - UI elements, eg, Cards, Maps, Trees... |
| **[Use Case 5: Business Users](https://www.genai-logic.com/#h.69d2voz8q5r1)** <br> webgenai | See `webgenai/` in this Manager | - Create systems from browser, with logic, sample data and derived attributes |
| **[Customs CLVS](samples/requirements/customs_demo_clvs/docs/requirements/customs_demo/requirements.md)** <br> demo_customs_clvs | genai-logic create  --project_name=demo_customs_clvs --db_url=sqlite:///samples/requirements/customs_demo_clvs/database/customs.sqlite | - Governed Business Systems<br> - EAI (using XML), textual requirements |
| **[Customs Surtax](samples/prompts/customs_cbsa.prompt.md)** <br> demo_customs_surtax | implement project demo_customs_surtax from samples/prompts/customs_cbsa.prompt.md | - New Business System from Regulations |

&nbsp;

> **Running a cloned project?** F5 won't work until the venv is set up — see [Project-Env](https://apilogicserver.github.io/Docs/Project-Env/) for options (`genai-logic run`, symlink, or local venv).

&nbsp;

## 2. Additional Demos

Advanced examples and specialized patterns:

| Demo | Say to your AI / Run | What You'll Learn |
|------|---------|-------------------|
| **Executable Requirements** | See [samples/requirements/readme_reqmts.md](samples/requirements/readme_reqmts.md) | Create from Gherkin requirements <br>implement reqs <path> |
| **New system from prompt** | genai-logic genai --using=samples/prompts/genai_demo.prompt | Create systems from prompt<br>Like WebGenAI, but from IDE |
| **Coding Samples** | code samples/nw_sample | Useful code examples<br>Search: `#als` |
| **MCP Discovery** <br> demo_copilot_mcp_discovery | genai-logic create --project_name=demo_copilot_mcp_discovery --db_url=sqlite:///samples/dbs/basic_demo.sqlite | test rules via Copilot access to MCP Server | 


**Copy Snippets for venv:**
```bash title="Copy Snippets for venv"
source venv/bin/activate       # windows: venv\Scripts\activate
source ../venv/bin/activate    # windows: ../venv\Scripts\activate
python -m venv venv            # may require python3 -m venv venv
```

&nbsp;


## Procedures

<br>

<details markdown>

<summary> Detail Procedures</summary>

<br>Specific procedures for running the demo are here, so they do not interrupt the conceptual discussion above.

You can use either VSCode or Pycharm.


**1. Establish your Virtual Environment**

Python employs a virtual environment for project-specific dependencies.

**If the project was created in this Manager** (or opened from it), the venv is already configured — just press F5.

**If the project was cloned from git**, choose one of:

* **Quickest (no VS Code setup):** from the Manager terminal (or, use Code Assistant):
    ```bash
    genai-logic run --project-name=<project-name>
    ```

* **Mac/Linux with F5:** create a symlink to the Manager venv:
    ```bash
    cd <project>
    sh venv_setup/venv.sh symlink
    # reload VS Code window, then F5
    ```

* **Any platform:** create a local venv:
    ```bash
    sh venv_setup/venv.sh go        # mac/linux
    .\venv_setup\venv.ps1 go        # windows
    ```

For PyCharm, you will get a dialog requesting to create the `venv`; say yes.

See [Project-Env](https://apilogicserver.github.io/Docs/Project-Env/) for more information.

&nbsp;

**2. Start and Stop the Server**

Both IDEs provide Run Configurations to start programs.  These are pre-built by `ApiLogicServer create`.

For VSCode, start the Server with F5, Stop with Shift-F5 or the red stop button.

For PyCharm, start the server with CTL-D, Stop with red stop button.

&nbsp;

**3. Entering a new Order**

To enter a new Order:

1. Click `Customer 1`

2. Click `+ ADD NEW ORDER`

3. Set `Notes` to "hurry", and press `SAVE AND SHOW`

4. Click `+ ADD NEW ITEM`

5. Enter Quantity 1, lookup "Product 1", and click `SAVE AND ADD ANOTHER`

6. Enter Quantity 2000, lookup "Product 2", and click `SAVE`

7. Observe the constraint error, triggered by rollups from the `Item` to the `Order` and `Customer`

8. Correct the quantity to 2, and click `Save`


**4. Update the Order**

To explore our new logic for green products:

1. Access the previous order, and `ADD NEW ITEM`

2. Enter quantity 11, lookup product `Green`, and click `Save`.

</details>

&nbsp;

### Pre-created Samples

<details markdown>

<summary> Explore Pre-created Samples</summary>

<br>The `samples` folder has pre-created important projects you will want to review at some point (Important: look for **readme files**):

* [nw_sample_nocust](https://apilogicserver.github.io/Docs/Tutorial/) - northwind (customers, orders...) database

    * This reflects the results you can expect with your own databases

* [nw_sample](https://apilogicserver.github.io/Docs/Sample-Database/) - same database, but with ***with [customizations](https://apilogicserver.github.io/Docs/IDE-Customize/) added***.  It's a great resource for exploring how to customize your projects.

    * Hint: use your IDE to search for `#als`

* [tutorial](https://apilogicserver.github.io/Docs/Tutorial/) - short (~30 min) walk-through of using API Logic Server using the northwind (customers, orders...) database

</br>

<details markdown>

<summary>You can always re-create the samples</summary>

<br>Re-create them as follows:

1. Open a terminal window (**Terminal > New Terminal**), and paste the following CLI command:

```bash
genai-logic create --project-name=samples/tutorial --db-url=
genai-logic create --project-name=samples/nw_sample --db-url=nw+
genai-logic create --project-name=samples/nw_sample_nocust --db-url=nw
```
</details>


</details>

&nbsp;

### Hiding Front Matter

<details markdown>

<summary>Hiding Front Matter </summary>

To hide the YAML or JSON front matter (the metadata block at the top of your markdown files) in the built-in VS Code markdown preview, you can adjust your editor settings:

1. Open the Settings panel using Ctrl + , (Windows/Linux) or Cmd + , (macOS).
2. Search for the following term: `markdown.previewFrontMatter`.
3. Change the dropdown value from show to `hide`.

The preview will now automatically strip the front matter from the rendered view.

![hide-front-matter](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/manager/hide-front-matter.png?raw=true)

</details>