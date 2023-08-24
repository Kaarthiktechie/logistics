# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class Trips(Document):
	def init(self):
		# self.today = date.today()
		self.trips =[]
		self.trips.clear()	
  
	def validate(self):
		self.init()
		self.function()
			
	def function(self):
		# truck_no = self.gettruck_no()
		self.table_insert()

	def gettruck_no(self):
		asset_id = frappe.db.get_list("Asset", filters={"name": self.asset_name}, fields =["item_code"])[0]
		truck_no = asset_id.item_code
		return truck_no

	def table_insert(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Trip details",
			"asset_name": self.asset_name,
			"status" : self.status,
			"driver": self.driver,
			"status" : self.status,
			"date"	: self.date,
			"trip" : self.trip,
			# "item_code" : truck_no
   
		})
		if tripsstatus:
			tripsstatus.insert()