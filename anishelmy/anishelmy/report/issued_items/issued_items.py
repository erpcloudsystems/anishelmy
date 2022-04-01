# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Item Code"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Item",
            "width": 100
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Qty Issued"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Data",
            "width": 80
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabStock Entry`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabStock Entry`.posting_date<=%(to_date)s"
    if filters.get("warehouse"):
        conditions += " and `tabStock Entry Detail`.s_warehouse=%(warehouse)s"
    if filters.get("cost_center"):
        conditions += " and `tabStock Entry Detail`.cost_center=%(cost_center)s"
    if filters.get("project"):
        conditions += " and `tabStock Entry Detail`.project=%(project)s"
    if filters.get("work"):
        conditions += " and `tabStock Entry Detail`.works=%(work)s"
    if filters.get("floor"):
        conditions += " and `tabStock Entry Detail`.floors=%(floor)s"
    if filters.get("frame_system"):
        conditions += " and `tabStock Entry Detail`.frame_system=%(frame_system)s"


    result = []
    item_results = frappe.db.sql("""
            SELECT distinct
                `tabStock Entry Detail`.item_code as name,
                `tabStock Entry Detail`.item_name as item_name,
                `tabStock Entry Detail`.stock_uom as stock_uom

            FROM
                `tabStock Entry Detail` join `tabStock Entry` on `tabStock Entry`.name = `tabStock Entry Detail`.parent
            WHERE
                `tabStock Entry`.docstatus = 1
                and `tabStock Entry`.stock_entry_type in ("Material Issue", "Material Transfer")
                {conditions}           

            Group BY `tabStock Entry Detail`.item_code
            """.format(conditions=conditions), filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'item_name': item_dict.item_name,
                'stock_uom': item_dict.stock_uom
            }
            details = frappe.db.sql("""
                SELECT 
                    
                    sum(`tabStock Entry Detail`.qty) as qty

                FROM
                    `tabStock Entry Detail`  join `tabStock Entry` on `tabStock Entry`.name = `tabStock Entry Detail`.parent
                WHERE 
                    `tabStock Entry Detail`.item_code = '{name}'
                    and  `tabStock Entry`.docstatus = 1
                    {conditions}
                """.format(name=item_dict.name, conditions=conditions), filters, as_dict=1)

            for x in details:
                data['qty']= x.qty

            result.append(data)
    return result

