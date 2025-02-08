// Copyright (c) 2024, gskishan and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Checkin"] = {
	"filters": [{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.add_days(frappe.datetime.get_today(), -1),

		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 80,
			"default":frappe.datetime.add_days(frappe.datetime.get_today(), -1),
			// "default": dateutil.year_end()
		},
		{
			"fieldname":"employee_name",
			"label": __("Employee Name"),
			"fieldtype": "Data",
			"width": 80,
			"reqd":0,
		}
	],
};
