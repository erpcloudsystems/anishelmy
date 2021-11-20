from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, get_fullname, add_days, nowdate, get_datetime
from erpnext.hr.utils import set_employee_name, get_leave_period, share_doc_with_approver
from erpnext.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from erpnext.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
from frappe.model.document import Document
from datetime import timedelta, datetime
import re, math, time
from urllib.parse import quote, urljoin
from frappe.desk.utils import slug
from frappe.utils import add_to_date, now, nowdate
from frappe.model.document import Document

def make_je(doc, method=None):
    if doc.is_party == 1:
        accounts = [
            {
                "doctype": "Journal Entry Account",
                "account": doc.account,
                "party_type": "Supplier",
                "party": doc.party,
                "credit": 0,
                "debit": doc.value_difference,
                "debit_in_account_currency": doc.value_difference,
                "user_remark": doc.name
            },
            {
                "doctype": "Journal Entry Account",
                "account": "5111 - مصاريف العمليات - A",
                "debit": 0,
                "credit": doc.value_difference,
                "credit_in_account_currency": doc.value_difference,
                "user_remark": self.name
            }
        ]
        new_doc = frappe.get_doc({
            "doctype": "Journal Entry",
            "cheque_no": doc.name,
            "cheque_date": doc.posting_date,
            "posting_date": doc.posting_date,
            "accounts": accounts,
            "user_remark": doc.party

        })
        new_doc.insert()
        new_doc.submit()

        doc.reload()