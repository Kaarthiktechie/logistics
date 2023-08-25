# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class Trips(Document):	
  
	def validate(self):
		self.validation()
		self.table_insert()

	def validation(self):
		all_trips = frappe.db.get_list("Trip details", filters = {"id" : self.name}, fields=["status"])
		for every_trip in all_trips:
			if every_trip.status == self.status:
				frappe.throw("You already have updated the status"+" "+ self.status)
  
	def table_insert(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Trip details",
			"driver": self.driver,
			"asset_name": self.asset_name,
			"item_id" : self.item_id,
			"trip" : self.trip,
			"item_id" : self.item_id,
			"status" : self.status,
			"date"	: self.date,
			"time" : self.time,
			"km" : self.km,
			"id" : self.name
		})
		if tripsstatus:
			tripsstatus.insert()