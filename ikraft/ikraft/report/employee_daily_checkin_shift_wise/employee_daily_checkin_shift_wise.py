# Copyright (c) 2024, gskishan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def data_condition(filters):
    condition = ""

    if filters:
        if filters.get("from_date") and filters.get("to_date"):
            condition += "AND DATE(ec_in.time) BETWEEN '{0}' AND '{1}' ".format(
                filters.get("from_date"), filters.get("to_date")
            )
        elif filters.get("from_date"):
            condition += "AND DATE(ec_in.time) = '{0}' ".format(filters.get("from_date"))

        if filters.get("employee_name"):
            condition += "AND LOWER(emp.employee_name) LIKE LOWER('%{0}%') ".format(
                filters.get("employee_name")
            )

        if filters.get("shift"):
            condition += "AND ec_in.shift = '{0}' ".format(filters.get("shift"))
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        condition += "AND DATE(ec_in.time) = '{0}' ".format(today)

    return condition


def get_data(filters):
    cond = data_condition(filters)

    sql = """
        SELECT
            ec_in.employee,
            emp.employee_name,
            ec_in.shift AS shift_name,
            DATE_FORMAT(ec_in.time, '%d-%m-%Y %H:%i:%s') AS check_in_time,
            ec_in.name AS check_in_id,
            DATE_FORMAT(ec_out.time, '%d-%m-%Y %H:%i:%s') AS check_out_time,
            ec_out.name AS check_out_id,
            ec_out.is_auto_created AS is_auto_created,

            SEC_TO_TIME(TIMESTAMPDIFF(SECOND, ec_in.time, ec_out.time)) AS total_time,
            
            CASE 
                WHEN ec_out.is_auto_created = 1 THEN '00:00:00'
                WHEN TIMESTAMPDIFF(SECOND, ec_in.time, ec_out.time) > 32400
                THEN SEC_TO_TIME(TIMESTAMPDIFF(SECOND, ec_in.time, ec_out.time) - 32400)
                ELSE '00:00:00' 
            END AS ot
             

        FROM
            `tabEmployee Checkin` ec_in
        LEFT JOIN
            `tabEmployee` emp ON ec_in.employee = emp.name
        LEFT JOIN
            `tabEmployee Checkin` ec_out
            ON ec_out.employee = ec_in.employee
            AND ec_out.log_type = 'OUT'
            AND ec_out.time = (
                SELECT MIN(time)
                FROM `tabEmployee Checkin`
                WHERE log_type = 'OUT'
                AND employee = ec_in.employee
                AND time > ec_in.time
                AND DATE(time) = DATE(ec_in.time)
            )
        WHERE
            ec_in.log_type = 'IN'
            {0}
        ORDER BY ec_in.employee, ec_in.time
    """.format(cond)

    frappe.errprint(sql)
    frappe.log_error("SQL Query Execution", sql)
    return frappe.db.sql(sql, as_dict=1)


def get_columns():
    return [
        {
            'fieldname': 'employee',
            'label': _('Employee'),
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
            'label': _('Shift'),
            'fieldname': "shift_name",
            'fieldtype': 'Data',
            'width': 160
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
            'label': _('Check Out Time'),
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
            'fieldname': "is_auto_created",
            'label': _('Is Auto Created'),
            'fieldtype': 'Check',
            'width': 60
        },
        
        {
            'label': _('Total Time'),
            'fieldname': 'total_time',
            'fieldtype': 'Data',
            'width': 150
        },    
        {
            'label': _('OT'),
            'fieldname': 'ot',
            'fieldtype': 'Data',
            'width': 100
        }
    ]
