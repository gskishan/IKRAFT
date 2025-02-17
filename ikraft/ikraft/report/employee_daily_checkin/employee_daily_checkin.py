# Copyright (c) 2024, gskishan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def data_condition(filters):
    if filters:
        condition = ""

        if filters.get("from_date") and filters.get("to_date"):
            condition = "AND DATE(ec_in.time) BETWEEN '{0}' AND '{1}' ".format(
                filters.get("from_date"), filters.get("to_date")
            )
        elif filters.get("from_date"):
            condition = "AND DATE(ec_in.time) = '{0}' ".format(filters.get("from_date"))

        if filters.get("employee_name"):
            condition += "AND LOWER(emp.employee_name) LIKE LOWER('%{0}%') ".format(
                filters.get("employee_name")
            )
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        condition = "AND DATE(ec_in.time) = '{0}' ".format(today)

    return condition


		
	


def get_data(filters):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    cond = data_condtion(filters)
    sql = """
			  SELECT 
			    ec_in.employee,
			    emp.employee_name,
			    DATE_FORMAT(ec_in.time, '%d-%m-%Y %H:%i:%s') AS "check_in_time",
			    DATE_FORMAT(ec_out.time, '%d-%m-%Y %H:%i:%s') AS "check_out_time",
			    ec_out.name AS check_out_id,
			    ec_in.name AS check_in_id,
			    ec_out.is_auto_created AS "is_auto_created"
			FROM 
			    `tabEmployee Checkin` ec_in
			LEFT JOIN 
			    `tabEmployee Checkin` ec_out 
			    ON ec_in.employee = ec_out.employee 
			    AND DATE(ec_out.time) = DATE(ec_in.time) 
			    AND ec_out.log_type = 'OUT'
			LEFT JOIN 
			    `tabEmployee` emp ON ec_in.employee = emp.name
			WHERE 
			    ec_in.log_type = 'IN'
			    {0}
			ORDER BY 
			    ec_in.employee, ec_in.time;

          """.format(cond)
    frappe.errprint(sql)
    frappe.log_error("SQL Query Execution", sql)
    return frappe.db.sql(sql, as_dict=1)


def get_columns():
	columns=[]

	columns+= [
		{
	 		'fieldname': 'employee',
            'label':('Employee'),
            'fieldtype': 'Link',
            'options': 'Employee',
			'width': 200
        },
		{
			'label': _('Employee Name'),
			'fieldname': "employee_name",
			'fieldtype': 'Data',
			'width': 240
		},
		{
			'label': _('Check In Time'),
			'fieldname': "check_in_time",
			'fieldtype': 'Data',
			'width': 200
		},
		{
			'label': _('Check-In'),
			'fieldname': "check_in_id",
			'fieldtype': 'Link',
			 'options': 'Employee Checkin',
			'width': 200
		},
        {
            'fieldname': "check_out_time",
            'label': ('Check Out Time'),
            'fieldtype': 'Data',
			'width': 200
        },
		{
			'label': _('Check-Out'),
			'fieldname': "check_out_id",
			'fieldtype': 'Link',
			 'options': 'Employee Checkin',
			'width': 200
		},
		{
			'label': _('Shift'),
			'fieldname': "shift_name",
			'fieldtype': 'Data',
			'width': 160
		},
        {
            'fieldname': "is_auto_created",
            'label': ('Is Auto Created'),
            'fieldtype': 'Check',
			'width': 60
        }
		
	]
	return columns
