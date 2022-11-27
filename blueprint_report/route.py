from flask import Blueprint, render_template, request, redirect, url_for, current_app
from db_work import call_proc, select
from sql_provider import SQLProvider
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
blueprint_report = Blueprint('bp_report', __name__, template_folder="templates")



@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=current_app.config['report_list'])
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id=', rep_id)
        if request.form.get('create_rep'):
            url_rep = current_app.config['report_url'][rep_id]['create_rep']
        else:
            url_rep = current_app.config['report_url'][rep_id]['view_rep']
        print('url_rep=', url_rep)
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
def create_rep1():
    if request.method == 'GET':
        return render_template('report1_create_form.html')
    else:
        in_year = request.form.get('input_year')
        in_month = request.form.get('input_month')
        if in_year:
            _sql_check = provider.get('order_report.sql', input_year=in_year, input_month=in_month)
            product_result, schema = select(current_app.config['db_config'], _sql_check)
            if len(product_result) == 0:
                res = call_proc(current_app.config['db_config'], 'orders_report', in_year, in_month)
                return render_template('report_created.html')
            else:
                return 'report_already_exists'
        else:
            return "Repeat input"


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
def view_rep1():
    if request.method == 'GET':
        return render_template('report1_find_form.html')
    else:
        in_year = request.form.get('input_year_')
        in_month = request.form.get('input_month_')
        if in_year and in_month:
            _sql = provider.get('order_report.sql', input_year=in_year, input_month=in_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) != 0:
                return render_template('product_report.html', schema=schema, result=product_result)
            else:
                return 'report doesn\'t exists'
        else:
            return "Repeat input"


@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
def create_rep2():
    if request.method == 'GET':
        return render_template('report2_create_form.html')
    else:
        in_year = request.form.get('input_year')
        in_month = request.form.get('input_month')
        if in_year:
            _sql_check = provider.get('sale_report.sql', input_year=in_year, input_month=in_month)
            product_result, schema = select(current_app.config['db_config'], _sql_check)
            if len(product_result) == 0:
                res = call_proc(current_app.config['db_config'], 'sales_report', in_year, in_month)
                return render_template('report_created.html')
            else:
                return 'report_already_exists'
        else:
            return "Repeat input"


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
def view_rep2():
    if request.method == 'GET':
        return render_template('report2_find_form.html')
    else:
        in_year = request.form.get('input_year_')
        in_month = request.form.get('input_month_')
        if in_year and in_month:
            _sql = provider.get('sale_report.sql', input_year=in_year, input_month=in_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) != 0:
                return render_template('product_report.html', schema=schema, result=product_result)
            else:
                return 'report doesn\'t exists'
        else:
            return "Repeat input"