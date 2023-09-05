# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import nowdate, now_datetime

class Trip(Document):	
  
	def validate(self):
		# self.validation()
		self.table_insert()

	def validation(self):
		all_trip = frappe.db.get_list("Events", filters = {"id" : self.name}, fields=["status"])
		for every_trip in all_trip:
			if every_trip.status == self.status:
				frappe.throw("You already have updated the status"+" "+ self.status)
  
	def table_insert(self):
		tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": self.asset_name,
			"trip" : self.item_id,
			"date"	: self.date,
			"time" : self.time,
			"id" : self.name
		})
		if tripstatus:
			tripstatus.insert()
   
@frappe.whitelist()
def trip_creation(location,date,sales_order,dispatch_address,shipping_address):
	sales_order_item_info = frappe.db.get_list("Sales Order Item",filters={"parent": sales_order}, fields=['name'])
	
	trip = frappe.get_doc({
					"doctype": "Trip",
					"item_id" :location,
					"date" : date,
					"sales_order_id" : sales_order,
					"from_address":dispatch_address,
					"to_address":shipping_address
		})
	trip.insert()

	tripstatus = frappe.get_doc({
				"doctype": "Events",
				"trip" : location,
				"date"	: date,
				"status" : "Booked",
				"id" : trip.name
			})
	if tripstatus:
		tripstatus.insert()
    
@frappe.whitelist()
def start(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Started",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Started",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()
    
@frappe.whitelist()
def sin(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Sin",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Sin",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()


@frappe.whitelist()
def sout(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Sout",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Sout",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()

@frappe.whitelist()
def din(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Din",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Din",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()

@frappe.whitelist()
def dout(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Dout",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Dout",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()

@frappe.whitelist()
def close(trip_id,asset_name):
		triptatus = frappe.db.get_list("Events",filters={
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Closed",
			"id" : trip_id
			})
		if not triptatus:
			tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Closed",
			"id" : trip_id
			})
			if tripstatus:
				tripstatus.insert()

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
		frappe.throw("There are no trip currently active")
  
  
@frappe.whitelist()
def attendence(trip_id,asset_name):
	date = datetime.date.today()
	trip_status_id = frappe.db.get_list ("Driver Login Page",
    filters={
		"asset_name":asset_name,
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
    
@frappe.whitelist()
def assigned(trip_id, asset_name):
	status = frappe.db.get_list("Events",filters={
		"id": trip_id
	},fields=["name","status","time","date"],order_by="time desc")[0]
	if (status.status == "Booked"):
		tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Assigned",
			"id" : trip_id
			})
		if tripstatus:
			tripstatus.insert()
   
@frappe.whitelist()
def confirm(trip_id, asset_name):
	status = frappe.db.get_list("Events",filters={
		"id": trip_id
	},fields=["name","status","time","date"],order_by="time desc")[0]
	
	if (status.status == "Assigned"):
		tripstatus = frappe.get_doc({
			"doctype": "Events",
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Confirmed",
			"id" : trip_id
			})
		if tripstatus:
			tripstatus.insert()
   
   
   
@frappe.whitelist()
def driver(trip_id,asset_name,date):
	is_driver = frappe.db.get_list("Events",filters={
		"id": trip_id,"date":date},fields=["driver","time","status"],order_by="time desc")
	driver_1 = is_driver[0]
	if driver_1.driver == None:
		driver = frappe.db.get_list("Events",filters={
		"asset_name": asset_name,"status": "Reported In","date":date},fields=["driver"],order_by="time desc")
		if driver:
			driver_name = driver[0]
			driver_save = frappe.get_doc("Trip",trip_id)
			driver_save.driver = driver_name.driver
			driver_save.save()
			# return driver_save.employee