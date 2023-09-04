# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import nowdate, now_datetime

class Trips(Document):	
  
	def validate(self):
		# self.validation()
		self.table_insert()

	def validation(self):
		all_trips = frappe.db.get_list("Events", filters = {"id" : self.name}, fields=["status"])
		for every_trip in all_trips:
			if every_trip.status == self.status:
				frappe.throw("You already have updated the status"+" "+ self.status)
  
	def table_insert(self):
		tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": self.driver,
			"asset_name": self.asset_name,
			"trip" : self.item_id,
			"date"	: self.date,
			"time" : self.time,
			"id" : self.name
		})
		if tripsstatus:
			tripsstatus.insert()
   
@frappe.whitelist()
def trip_creation(location,date,sales_order,dispatch_address,shipping_address):
	sales_order_item_info = frappe.db.get_list("Sales Order Item",filters={"parent": sales_order}, fields=['name'])
	for each_item in sales_order_item_info:
		trip = frappe.get_doc({
					"doctype": "Trips",
					"item_id" :location,
					"date" : date,
					"sales_order_id" : sales_order,
					"sales_order_item_id" : each_item.name,
					"from_address":dispatch_address,
					"to_address":shipping_address
		})
		trip.insert()

		tripsstatus = frappe.get_doc({
				"doctype": "Events",
				"trip" : location,
				"date"	: date,
				"status" : "Open",
				"id" : trip.name
			})
		if tripsstatus:
				tripsstatus.insert()
    
@frappe.whitelist()
def start(trip_id,driver,asset_name):
		tripstatus = frappe.db.get_list("Events",filters={
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Started",
			"id" : trip_id
			})
		if not tripstatus:
			tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Started",
			"id" : trip_id
			})
			if tripsstatus:
				tripsstatus.insert()
# @frappe.whitelist()
# def start(trip_id):
# 	trip_status_id = frappe.db.get_list ("Events",
#     filters={
# 		"trip":["=", trip_id]
# 	})
 
# 	if trip_status_id:
# 		per_trip_status_id = trip_status_id[0]
# 		return per_trip_status_id.name
# 	else:
# 		trip_status = frappe.get_doc({
# 						"doctype": "Trip Status",
# 						"trip" : trip_id
# 			})
# 		if trip_status:
# 			trip_status.insert()
# 			trip_status.save()
# 		return trip_status.name

@frappe.whitelist()
def trip_details(trip_id):
	trip_status_id = frappe.db.get_list ("Trip Status",
    filters={
		"trip":["=", trip_id]
	})
 
	if trip_status_id:
		per_trip_status_id = trip_status_id[0]
		return per_trip_status_id.name
	else:
		frappe.throw("There are no trips currently active")
  
  
@frappe.whitelist()
def attendence(trip_id,asset_name,driver):
	date = datetime.date.today()
	trip_status_id = frappe.db.get_list ("Driver Login Page",
    filters={
		"asset_name":asset_name,
		"driver":driver,
		"date": date
	})
 
	if trip_status_id:
		per_trip_status_id = trip_status_id[0]
		return per_trip_status_id.name
	else:
		trip_status = frappe.get_doc({
						"doctype": "Trip Status",
						"trip" : trip_id
			})
		if trip_status:
			trip_status.insert()
			trip_status.save()
		return trip_status.name

@frappe.whitelist()
def status(trip_id):
    status = frappe.db.get_list("Events",filters={
		"id": trip_id
	},fields=["name","status","time","date"],order_by="time desc")
    if status:
        return status[0]