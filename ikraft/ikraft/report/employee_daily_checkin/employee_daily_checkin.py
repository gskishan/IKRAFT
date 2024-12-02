# Copyright (c) 2024, gskishan and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_data():
	sql="""SELECT 
			ec_in.employee ,
			emp.employee_name,
			ec_in.time AS "check_in_time",
			ec_out.time AS "check_out_time",
			es.name AS "shift_name",
			ec_out.is_auto_created AS "is_auto_created"
		FROM 
			`tabEmployee Checkin` ec_in
		LEFT JOIN 
			`tabEmployee Checkin` ec_out ON ec_in.employee = ec_out.employee 
			AND ec_out.time > ec_in.time 
			AND ec_out.log_type = 'OUT'
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
			AND DATE(ec_in.time) = CURDATE() - INTERVAL 1 DAY
		ORDER BY 
			ec_in.employee, ec_in.time;
		"""
	return  frappe.db.sql(sql,as_dict=1)

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
            'fieldname': "check_out_time",
            'label': ('Check Out Time'),
            'fieldtype': 'Data',
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
