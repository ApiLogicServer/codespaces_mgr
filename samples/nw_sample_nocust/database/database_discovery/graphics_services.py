from database import models
import logging
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship, remote, foreign
from functools import wraps # This convenience func preserves name and docstring
import decimal as decimal
from sqlalchemy import extract, func
from flask import request, jsonify
from safrs import jsonapi_rpc, SAFRSAPI
import safrs

"""
Graphics methods for database classes.

Called by api/api_discovery/dashboard_services.py when admin app loaded
"""

app_logger = logging.getLogger(__name__)


def add_method(cls):
  """
  Decorator to add method to class, e.g., db class group by query method

  Thanks to: https://mgarod.medium.com/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
  """
  def decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
      return func(*args, **kwargs)

    setattr(cls, func.__name__, wrapper)
    # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
    return func # returning func means func can still be used normally
  return decorator

##############################
# generated services follow
##############################


@classmethod
@add_method(models.Order)
@jsonapi_rpc(http_methods=['GET', 'OPTIONS'])
def sales_by_region(*args, **kwargs):
    """
    Complex query with multiple joins, for graphics, from 'Graph Sales by Region'.
    Test with Swagger.
    """
    if request.method == 'OPTIONS':
        return jsonify({ "result": "ok" })

    from database.models import Order, OrderDetail
    db = safrs.DB
    session = db.session    # sqlalchemy.orm.scoping.scoped_session
    # Security.set_user_sa()  # an endpoint that requires no auth header (see also @bypass_security)

    # SQLAlchemy query
    query = sales_by_region = ((session.query(Order.ShipRegion, func.sum(OrderDetail.Quantity * OrderDetail.UnitPrice * (1 - OrderDetail.Discount))
            .label("TotalSales"))
            .join(OrderDetail, OrderDetail.OrderId == Order.Id)
            .filter(Order.ShippedDate.is_not(None))
            .filter(Order.ShipRegion.is_not(None))
            .group_by(Order.ShipRegion)
            .order_by(func.sum(OrderDetail.Quantity * OrderDetail.UnitPrice * (1 - OrderDetail.Discount))
            .desc())))
    # Execute query and fetch results
    results = query.all()
    from decimal import Decimal
    columns = ['Ship Region' , 'Total Sales']
    results = [{columns[0]: row[0], columns[1]: round(float(row[1]), 2)} for row in results]
    title = 'Sales by Region'
    graph_type = 'Bar'.lower()
    json_results = {
        "results": results,
        "columns": columns,
        "title": title,
        "chart_type": graph_type,
        "xAxis": columns[0],
        "yAxis": columns[1],
    }

    return json_results


@classmethod
@add_method(models.Category)
@jsonapi_rpc(http_methods=['GET', 'OPTIONS'])
def sales_by_category(*args, **kwargs):
    """
    Complex query with multiple joins, for graphics, from 'Graph Sales by Category'.
    Test with Swagger.
    """
    if request.method == 'OPTIONS':
        return jsonify({ "result": "ok" })

    from database.models import Category, Product, OrderDetail, Order
    db = safrs.DB
    session = db.session    # sqlalchemy.orm.scoping.scoped_session
    # Security.set_user_sa()  # an endpoint that requires no auth header (see also @bypass_security)

    # SQLAlchemy query
    query = sales_by_category = ((session.query(Category.CategoryName_ColumnName, func.sum(OrderDetail.Quantity * OrderDetail.UnitPrice * (1 - OrderDetail.Discount))
            .label("TotalSales"))
            .join(Product, Category.Id == Product.CategoryId)
            .join(OrderDetail, Product.Id == OrderDetail.ProductId)
            .join(Order, OrderDetail.OrderId == Order.Id)
            .filter(Order.ShippedDate.is_not(None))
            .group_by(Category.CategoryName_ColumnName)
            .order_by(func.sum(OrderDetail.Quantity * OrderDetail.UnitPrice * (1 - OrderDetail.Discount))
            .desc())))
    # Execute query and fetch results
    results = query.all()
    from decimal import Decimal
    columns = ['Category Name' , 'Total Sales']
    results = [{columns[0]: row[0], columns[1]: round(float(row[1]), 2)} for row in results]
    title = 'Sales by Category'
    graph_type = 'Bar'.lower()
    json_results = {
        "results": results,
        "columns": columns,
        "title": title,
        "chart_type": graph_type,
        "xAxis": columns[0],
        "yAxis": columns[1],
    }

    return json_results
