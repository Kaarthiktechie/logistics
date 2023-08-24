# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class Trips(Document):	
  
	def validate(self):
		self.table_insert()
  
	def table_insert(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Trip details",
			"driver": self.driver,
			"asset_name": self.asset_name,
			"trip" : self.trip,
			"status" : self.status,
			"date"	: self.date,
			"time" : self.time,
			"km" : self.km
		})
		if tripsstatus:
			tripsstatus.insert()