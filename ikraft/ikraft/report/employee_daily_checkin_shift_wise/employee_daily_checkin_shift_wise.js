// Copyright (c) 2025, gskishan and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Checkin Shift Wise"] = {
	"filters": [{
		"fieldname": "from_date",
		"label": __("Date"),
		"fieldtype": "Date",
		"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),

	},
	{
		"fieldname": "to_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"width": 80,
		"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
		// "default": dateutil.year_end()
	}, {
		"fieldname": "shift",
		"label": __("Shift"),
		"fieldtype": "Link",
		"options": "Shift Type",
		"width": 80,
		"reqd": 0,
	},
		{
		"fieldname": "employee_name",
		"label": __("Employee Name"),
		"fieldtype": "Data",
		"width": 80,
		"reqd": 0,
	}
	],
};
