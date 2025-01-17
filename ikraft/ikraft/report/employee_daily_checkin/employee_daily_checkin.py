# Copyright (c) 2024, gskishan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def data_condtion(filters):
	today =datetime.now().strftime('%Y-%m-%d')
	condition="and DATE(ec_in.time) ='{0}' ".format(today)
	if filters:
		condition="and DATE(ec_in.time) ='{0}' ".format(filters.get("from_date"))

	return condition
		
	


def get_data(filters):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    cond = data_condtion(filters)
    sql = """SELECT 
                ec_in.employee,
                emp.employee_name,
                DATE_FORMAT(ec_in.time, '%d-%m-%Y %H:%i:%s') AS "check_in_time",
                DATE_FORMAT(ec_out.time, '%d-%m-%Y %H:%i:%s') AS "check_out_time",
                es.name AS "shift_name",
                ec_out.name AS check_out_id,
                ec_in.name AS check_in_id,
                ec_out.is_auto_created AS "is_auto_created"
            FROM 
                `tabEmployee Checkin` ec_in
            LEFT JOIN 
                `tabEmployee Checkin` ec_out ON ec_in.employee = ec_out.employee 
                AND date(ec_out.time) = date(ec_in.time) 
                AND ec_out.log_type = 'OUT'
                AND DATE(ec_out.time) = DATE(ec_in.time)
            LEFT JOIN 
                `tabEmployee` emp ON ec_in.employee = emp.name
            LEFT JOIN 
                `tabShift Assignment` sa ON ec_in.employee = sa.employee
            LEFT JOIN 
                `tabShift Type` es ON sa.shift_type = es.name
            WHERE 
                ec_in.log_type = 'IN'
                AND sa.start_date <= DATE(ec_in.time)
                AND (sa.end_date IS NULL OR sa.end_date >= DATE(ec_in.time))
                {0}
            ORDER BY 
                ec_in.employee, ec_in.time;
          """.format(cond)
    frappe.errprint(sql)
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
