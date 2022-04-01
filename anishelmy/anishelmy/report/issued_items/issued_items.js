// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Issued Items"] = {
	"filters": [
        {
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today()),
			"reqd": 0
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"reqd": 0
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"reqd": 0
		},
		{
			"fieldname": "work",
			"label": __("Work"),
			"fieldtype": "Link",
			"options": "works",
			"reqd": 0
		},
		{
			"fieldname": "floor",
			"label": __("Floor"),
			"fieldtype": "Link",
			"options": "Floors",
			"reqd": 0
		},
		{
			"fieldname": "frame_system",
			"label": __("Frame System"),
			"fieldtype": "Link",
			"options": "frame system",
			"reqd": 0
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 0
		},

	]
};