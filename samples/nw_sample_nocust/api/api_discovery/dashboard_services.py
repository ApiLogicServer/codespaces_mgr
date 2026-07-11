from database import models
import logging
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship, remote, foreign
from functools import wraps # This convenience func preserves name and docstring
import decimal as decimal
from sqlalchemy import extract, func
from flask import request, jsonify
from safrs import jsonapi_rpc, SAFRSAPI
from database import models
import safrs
from pathlib import Path

"""
Called by iFrame in home.js when admin app is loaded

Returns iFrame for ui/admin/home.js, with entries like this to populate the dashboard:
<iframe src="http://localhost:5656/chart_graphics/sales_by_category" style="flex: 1; border: none; width: 90%; height: 200px;">

curl -X GET "http://localhost:5656/dashboard"
"""

app_logger = logging.getLogger(__name__)
dashboard_result = {}


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    pass

    @app.route('/dashboard', methods=['GET','OPTIONS'])
    def dashboard():

        if request.method == 'OPTIONS':
            return jsonify({"result": "ok"})

        server = request.host_url

        iframe_template = '<div class="dashboard-iframe"><iframe src="{url}" style="flex: 1; border: none; width: 90%; height: 200px;"></iframe></div>'

        iframe_1 = iframe_template.format(url=f"{server}chart_graphics/sales_by_region")

        iframe_2 = iframe_template.format(url=f"{server}chart_graphics/sales_by_category")

        return f'<div style="display: flex; flex-direction: row; gap: 10px;  border: none; ">{iframe_1} {iframe_2}</div>'


    @app.route('/chart_graphics/<path:path>', methods=['GET','OPTIONS'])
    def chart_graphics(path):
        if request.method == 'OPTIONS':
            return jsonify({"result": "ok"})

        dashboards = get_dashboards()
        if len(dashboards) == 0:
            return jsonify({"result": "No dashboards Found"}), 404
        if path in dashboards:
            return dashboards[path]
        return jsonify({"result": "not found"}), 404


    ##############################
    # generated queries follow
    ##############################

    def get_dashboards():
        if len(dashboard_result) > 0:
            return dashboard_result

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader = FileSystemLoader('ui/templates'))
        template = env.get_template('bar_chart.jinja')


        previously_failed = Path('docs/graphics/sales_by_region.err').exists()
        if previously_failed:
            pass  # query has previously failed, so skip it
        else:
            try:
                results = models.Order.sales_by_region(None)
                color = 'rgba(75, 192, 192, 0.2)'
                dashboard1 = template.render(result=results, color=color)
                dashboard_result['sales_by_region']= dashboard1
            except Exception as e:
                msg = f"GenAI query creation error on models.Order.sales_by_region: "  + str(e)
                dashboard_result['sales_by_region'] = msg
                app_logger.error(msg)
                Path('docs/graphics').mkdir(parents=True, exist_ok=True)
                with open('docs/graphics/sales_by_region.err', 'w') as err_file:
                    err_file.write(msg)  # this logs the error to prevent future calls


        previously_failed = Path('docs/graphics/sales_by_category.err').exists()
        if previously_failed:
            pass  # query has previously failed, so skip it
        else:
            try:
                results = models.Category.sales_by_category(None)
                color = 'rgba(75, 192, 192, 0.2)'
                dashboard2 = template.render(result=results, color=color)
                dashboard_result['sales_by_category']= dashboard2
            except Exception as e:
                msg = f"GenAI query creation error on models.Category.sales_by_category: "  + str(e)
                dashboard_result['sales_by_category'] = msg
                app_logger.error(msg)
                Path('docs/graphics').mkdir(parents=True, exist_ok=True)
                with open('docs/graphics/sales_by_category.err', 'w') as err_file:
                    err_file.write(msg)  # this logs the error to prevent future calls


        return dashboard_result
