# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime
class DriverLoginPage(Document):
    pass



@frappe.whitelist()
def report_in(driver,asset_name):

		tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Reported In"
		})
		if tripsstatus:
			tripsstatus.insert()

		
   
@frappe.whitelist()
def driver_error():
    frappe.throw("driver name is not mentioned")

@frappe.whitelist()
def truck_error():
    frappe.throw("truck number is not mentioned")
    
    
@frappe.whitelist()
def report_out(driver,asset_name):
		tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Reported Out"
		})
		if tripsstatus:
			tripsstatus.insert()
   
   
   
