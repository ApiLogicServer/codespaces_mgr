---
title: Declarative Application Integration
file: docs/Sample-integration
notes: gold docsite, 2100 words (goal: 1500)
version: 10.03.02 from docsite, for readme
---


&nbsp;
**Key Takeways - TL;DR - Kafka Integration: Async Messaging**
&nbsp;

    APIs are useful to application integration, but do not deal with the reality that the receiving system might be down.

    Message Brokers like Kafka address this with guaranteed ***async delivery*** of messages.  The Broker stores the message, delivering it (possibly later) when the the receiver is up.

    Message Brokers also support multi-cast: you ***publish*** a message to a "topic", and other systems ***subscribe***.  This is often casually described as "pub/sub".

    This sample presumes you are familiar with basic GenAI-Logic services, as illustrated in the Basic Demo tutorial.

    This guide will illustrate how to publish Kafka messages, and subscribe to and process them in another project.  This all runs on your machine, and includes instructions in installing Kafka as a Docker container.



# Purpose

**System Requirements**

This app illustrates using IntegrationServices for B2B push-style integrations with APIs, and internal integration with messages.  

&nbsp;

![demp_kafka](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/integration/demo_kafka.png?raw=true)

The **demo_kafka API Logic Server** provides APIs *and logic*:

1. **Order Logic:** enforcing database integrity and application Integration (alert shipping)

2. A **Custom API**, to match an agreed-upon format for B2B partners

3. **Standard APIs** for ad-hoc integration, user interfaces, etc

The **Shipping API Logic Server** listens on kafka, and processes the message.<br><br>

&nbsp;

**Self-serve APIs, Shared Logic**

This sample illustrates some key architectural considerations:

| Requirement | Poor Practice | Good Practice | Best Practice | Ideal
| :--- |:---|:---|:---|:---|
| **Ad Hoc Integration** | ETL | APIs | **Self-Serve APIs** |  **Automated** Self-Serve APIs |
| **Logic** | Logic in UI | | **Reusable Logic** | **Declarative Rules**<br>.. Extensible with Python |
| **Messages** | | | Kafka | **Kafka Logic Integration** |

We'll further expand of these topics as we build the system, but we note some Best Practices:

* **APIs should be self-serve:** not requiring continuing server development

    * APIs avoid the overhead of nightly Extract, Transfer and Load (ETL)

* **Logic should be re-used** over the UI and API transaction sources

    * Logic in UI controls is undesirable, since it cannot be shared with APIs and messages

This sample was developed with API Logic Server - [open source, available here](https://apilogicserver.github.io/Docs/).

<br>

```bash title='🤖 Bootstrap your AI assistant — paste into chat (Agent mode, Claude Sonnet 4.6 recommended)'
Please load `.github/.copilot-instructions.md`
```

&nbsp;

# Development Overview

&nbsp;

## 1. Create Project

The command below creates an `demo_kafka` by reading your schema.  The database is Northwind (Customer, Orders, Items and Product), as shown in the Appendix.  

Notes: 

1. If you are in the project `demo_kafka`, this is already done -- ignore this step
2. the `db_url` value is [an abbreviation](https://apilogicserver.github.io/Docs/Data-Model-Examples); you would normally supply a SQLAlchemy URL.  

```bash
$ genai-logic create --project_name=Kafka_demo --db_url=nw-    # create project from nw (uncustomized)
```

You can then open the project in your IDE, and run it.

&nbsp;

## 2. Customize: in your IDE

While API/UI automation is a great start, we now require Custom APIs, Logic and Security.

&nbsp;

### a. Using Copilot (experimental)

```text title="Add Logic with Copilot"
on Placing Orders, Check Credit    
    1. The Customer's balance is less than the credit limit
    2. The Customer's balance is the sum of the Order amount_total where date_shipped is null
    3. The Order's amount_total is the sum of the Item amount
    4. The Item amount is the quantity * unit_price
    5. The Item unit_price is copied from the Product unit_price

Use case: App Integration
    1. Publish the Order to Kafka topic 'order_shipping' if the date_shipped is not None.
```

&nbsp;

### b. Using `add-cust`

You normally apply such customizations using your IDE, leveraging code completion, etc.  To accelerate this sample, you can apply the customizations with `ApiLogicServer add-cust`.   We'll review the customizations below.

&nbsp;

The following `add-cust` process simulates:

* Adding security to your project using a CLI command, and
* Using your IDE to:

    * declare logic in `logic/declare_logic.sh`
    * declare security in `security/declare_security.py`
    * implement custom APIs in `api/customize_api.py`, using <br>`OrderShipping` declared in `integration/row_dict_maps`

> These customizations are shown in the screenshots below.

To apply customizations, in a terminal window for your project:

**1. Stop the Server** (Red Stop button, or Shift-F5 -- see Appendix)

**2. Apply Customizations:**

```bash
genai-logic add-cust # requires correct active (venv)
```
> Do not 'add-auth` - it is not required for this demo

&nbsp;

**3. Enable and Start Kafka**

To enable Kafka:

1. In `conf/config.py`, find and comment out: `KAFKA_PRODUCER = None  # comment out to enable Kafka`

2. Update your `etc/conf` to include the lines shown below (e.g., `sudo nano /etc/hosts`).

```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##

# for kafka
127.0.0.1       broker1
::1             localhost
255.255.255.255 broadcasthost
::1             localhost

127.0.0.1       localhost
# Added by Docker Desktop
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section
```
3. If you already created the container, you can

    1. Start it in the Docker Desktop, and
    2. **Skip the next 2 steps;** otherwise...

4. Start Kafka: in a terminal window: `docker compose -f integration/kafka/dockercompose_start_kafka.yml up`

5. Create topic: in Docker: 

```bash
docker exec -it broker1 bash # then, in the docker shell
/opt/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3  --topic order_shipping
```

Here some useful Kafka commands:

```bash
# use Docker Desktop > exec, or docker exec -it broker1 bash 
# in docker terminal: set prompt, delete, create, monnitor topic, list all topics
# to clear topic, delete and create

PS1="kafka > "  # set prompt

/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic order_shipping --delete

/opt/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3  --topic order_shipping

# list the msgs - note: you need to increment the group# at the end each time you issue the command
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic order_shipping --from-beginning --group fresh-group-1

/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

6. Enable Kafka - update `config/default.env` to include:

```text
KAFKA_SERVER=localhost:9092
```

&nbsp;

**4. Restart the server, login as `admin`**


&nbsp;

## 3. Integrate: B2B and Shipping

We now have a running system - an API, logic, security, and a UI.  Now we must integrate with:

* B2B partners -- we'll create a **B2B Custom Resource**
* OrderShipping -- we add logic to **Send an OrderShipping Message**

&nbsp;

### B2B Custom Resource

As illustrated in the Basic Demo tutorial, the `add-cust` procedure has added a B2B custom endpoint to add an order and items.

&nbsp;

### EAI Message

Alternatively, we might receive a message from sales using Kafka.  We can subscribe as follows:

```text title="Subscribe to sales message - Kafka Enterprise Application Integration"
Subscribe to Kafka topic `order_b2b` (JSON format).

The payload is a single order with items:
{
  "AccountId": "ALFKI",
  "Given": "Steven",
  "Surname": "Buchanan",
  "Items": [
    { "ProductName": "Chai",  "QuantityOrdered": 1 },
    { "ProductName": "Chang", "QuantityOrdered": 2 }
  ]
}

Target tables: Order, OrderDetail (from models.py).

Field mappings:
- `AccountId` → look up Customer by Customer.Id, set Order.CustomerId
- `Given` + `Surname` → compound lookup on Employee.FirstName + Employee.LastName, set Order.EmployeeId
- `Items` array → OrderDetail rows: `ProductName` → look up Product by Product.ProductName, set OrderDetail.ProductId; `QuantityOrdered` → OrderDetail.Quantity
```

&nbsp;

### Produce `OrderShipping` Message

Successful orders need to be sent to Shipping, again in a predesignated format.

To place an order, and send the message:

1. Use the Admin App, ServicesEndPoint / OrderB2B
2. Click Try It
3. Click Execute to use the sample data

We could certainly POST an API, but Messaging (here, Kafka) provides significant advantages:

* **Async:** Our system will not be impacted if the Shipping system is down.  Kafka will save the message, and deliver it when Shipping is back up.
* **Multi-cast:** We can send a message that multiple systems (e.g., Accounting) can consume.
 
The content of the message is a JSON string, just like an API.

Just as you can customize apis, you can complement rule-based logic using Python events:

1. Declare the mapping -- see the `OrderShipping` class in the right pane.  This formats our Kafka message content in the format agreed upon with Shipping.

2. Define a Python `after_flush` event, which invokes `send_order_to_shipping`.  This is called by the logic engine, which passes the SQLAlchemy `models.Order`` row.

3. `send_order_to_shipping` uses the `OrderShipping` class, which maps our SQLAlchemy order row to a dict (`row_to_dict`).

![overview](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/integration/integration.png?raw=true)


&nbsp;
**Key Takeways - Extensible Rules, Kafka Message Produced**
&nbsp;

    Rule-based logic is extensible with Python, here producing a Kafka message with 20 lines of code.

&nbsp;

## 4. Consuming Messages

The Shipping system illustrates how to consume messages.  This system was [created from AI](https://apilogicserver.github.io/Docs/Tutorial-AI), here customized to add message consumption.

&nbsp;

### Create/Start Shipping

To explore Shipping:

**1. Create the Shipping Project:**

```bash
genai-logic create --project_name=shipping --db_url=shipping
```

**2. Start your IDE (e.g., `code shipping`) and establish your `venv`**

**3. Start the Shipping Server: F5** (it's configured to use a different port)

&nbsp;

### Consuming Logic

To consume messages:

**1. Enable Consumption**

Shipping is pre-configured to enable message consumption with a setting in `conf/config.py`:

```python
KAFKA_CONSUMER = '{"bootstrap.servers": "localhost:9092", "group.id": "als-default-group1", "auto.offset.reset":"smallest"}'
```

When the server is started in `api_logic_server_run.py`, it invokes `integration/kafka/kafka_consumer.py#flask_consumer`.  This calls the pre-supplied `FlaskKafka`, which takes care of the Kafka listening, thread management, and the `handle` annotation used below.

> `FlaskKafka` was inspired by the work of Nimrod (Kevin) Maina, in [this project](https://pypi.org/project/flask-kafka/).  Many thanks!

&nbsp;

**2. Configure a mapping**

As we did for our OrderB2B Custom Resource, we configure an `OrderToShip` mapping class to map the message onto our SQLAlchemy Order object.

&nbsp;

**3. Provide a Message Handler**

We provide the `order_shipping` handler in `integration/kafka/kafka_consumer.py`:

1. Annotate the topic handler method, providing the topic name.

    * This is used by `FlaskKafka` establish a Kafka listener

2. Provide the topic handler code, leveraging the mapper noted above.  It is called by `Flaskkafka` per the method annotations.

![process in shipping](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/integration/kafka-consumer.jpg?raw=true)

&nbsp;

### Test it

Use your IDE terminal window to simulate a business partner posting a B2BOrder.  You can set breakpoints in the code described above to explore system operation.

```bash
ApiLogicServer curl "'POST' 'http://localhost:5656/api/ServicesEndPoint/OrderB2B'" --data '
{"meta": {"args": {"order": {
    "AccountId": "ALFKI",
    "Surname": "Buchanan",
    "Given": "Steven",
    "Items": [
        {
        "ProductName": "Chai",
        "QuantityOrdered": 1
        },
        {
        "ProductName": "Chang",
        "QuantityOrdered": 2
        }
        ]
    }
}}}'
```

&nbsp;

# Summary

These applications have demonstrated several **types of application integration:**

* **Ad Hoc Integration** via self-serve APIs

* **Custom Integration** via custom APIs, to support business agreements with B2B partners

* **Message-Based Integration** to decouple internal systems by reducing dependencies that all systems must always be running


We have also illustrated several technologies noted in the **Ideal** column:

| Requirement | Poor Practice | Good Practice | Best Practice | **Ideal**
| :--- |:---|:---|:---|:---|
| **Ad Hoc Integration** | ETL | APIs | **Self-Serve APIs** |  **Automated** Self-Serve APIs |
| **Logic** | Logic in UI | | **Reusable Logic** | **Declarative Rules**<br>.. Extensible with Python |
| **Messages** | | | Kafka | **Kafka Logic Integration** |


API Logic Server supports the **Ideal Practices** noted above: 

1. **Automation:** instant ad hoc API (and Admin UI) with the `ApiLogicServer create` command

2. **Declarative Rules** - security and multi-table logic, providing a 40X code reduction for backend half of these systems

3. **Kafka Logic Integration**

    * **Send** from logic events

    * **Consume** by extending `kafka_consumer`

    * Services, including:

        * `Mapper` services to transform rows and dict

        * `FlaskKafka` for Kafka listening, threading, and annotation invocation

4. **Standards-based Customization:**

    * Standard packages: Python, Flask, SQLAlchemy, Kafka...

    * Using standard IDEs

As a result, we built 2 non-trivial systems with a remarkably small amount of Python code:

| Type | Code |
| :--- |:--|
| Custom B2B API | 10 lines |
| Check Credit Logic | 5 rules |
| Row Level Security | 1 security declaration |
| Send Order to Shipping | 20 lines |
| Process Order in Shipping | 30 lines |
| Mapping configurations <br>to transform rows and dicts |  45 lines |

For more information on API Logic Server, [click here](https://apilogicserver.github.io/Docs/).

&nbsp;

# Appendix

## Status

Tested on Mac

## Apendix: Customizations

View them [here](https://github.com/ApiLogicServer/ApiLogicServer-src/tree/main/api_logic_server_cli/prototypes/nw).

&nbsp;

## Appendix: Procedures

Specific procedures for running the demo are here, so they do not interrupt the conceptual discussion above.

You can use either VSCode or Pycharm.

&nbsp;

**1. Establish your Virtual Environment**

Python employs a virtual environment for project-specific dependencies.  Create one as shown below, depending on your IDE.

For VSCode:

Establish your `venv`, and run it via the first pre-built Run Configuration.  To establish your venv:

```bash
python -m venv venv; venv\Scripts\activate     # win
python3 -m venv venv; . venv/bin/activate      # mac/linux

pip install -r requirements.txt
```

For PyCharm, you will get a dialog requesting to create the `venv`; say yes.

See [here](https://apilogicserver.github.io/Docs/Install-Express/) for more information.

&nbsp;

**2. Start and Stop the Server**

Both IDEs provide Run Configurations to start programs.  These are pre-built by `ApiLogicServer create`.

For VSCode, start the Server with F5, Stop with Shift-F5 or the red stop button.

For PyCharm, start the server with CTL-D, Stop with red stop button.

&nbsp;

**3. Entering a new Order**

To enter a new Order:

1. Click `ALFKI``

2. Click `+ ADD NEW ORDER`

3. Set `Notes` to "hurry", and press `SAVE AND SHOW`

4. Click `+ ADD NEW ITEM`

5. Enter Quantity 1, lookup "Chai", and click `SAVE AND ADD ANOTHER`

6. Enter Quantity 2000, lookup "Chang", and click `SAVE`

7. Observe the constraint error, triggered by rollups from the `OrderDetail` to the `Order` and `Customer`

8. Correct the quantity to 2, and click `Save`


**4. Update the Order**

To explore our new logic for green products:

1. Access the previous order, and `ADD NEW ITEM`

2. Enter quantity 11, lookup product `Chang`, and click `Save`.