# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime
  
class DriverLoginPage(Document):
	@frappe.whitelist()
	def report_in(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": self.driver,
			"asset_name": self.asset_name,
			"date"	: nowdate(),
			"status" : "Reported In"
		})
		if tripsstatus:
			tripsstatus.insert()
		# frappe.local.response["type"] = "redirect"
		# frappe.local.response["location"] = f"/desk#Logistics/Trip Details/"

	@frappe.whitelist()
	def report_out(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": self.driver,
			"asset_name": self.asset_name,
			"date"	: nowdate(),
			"status" : "Reported Out"
		})
		if tripsstatus:
			tripsstatus.insert()
