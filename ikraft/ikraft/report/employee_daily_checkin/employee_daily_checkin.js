// Copyright (c) 2024, gskishan and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Checkin"] = {
	"filters": [{
			"fieldname":"from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.add_days(frappe.datetime.get_today(), -1),

		},
	]
};
