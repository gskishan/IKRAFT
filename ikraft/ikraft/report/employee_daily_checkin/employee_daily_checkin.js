// Copyright (c) 2024, gskishan and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Checkin"] = {
	"filters": [{
			"fieldname":"from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":frappe.utils.add_days(frappe.utils.get_today(), -1),

		},
	]
};
