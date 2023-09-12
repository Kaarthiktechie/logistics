# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime
class DriverLoginPage(Document):
    pass



@frappe.whitelist()
def report_in(driver,asset_name,name):
    report_in_list = frappe.db.get_list("Events",filters={
		"asset_name":asset_name,
	},fields=["status"],order_by="name desc")
    a = 0
    if report_in_list:
        for every_report_in  in report_in_list:
            if every_report_in.status == "Reported In":
                frappe.throw(f"Truck no {asset_name} is already assigned to a driver")
                a = 1
            if every_report_in.status == "Reported Out":
                report_in_sub(driver,asset_name,name)
                a = 1
                break
        if a == 0:
            report_in_sub(driver,asset_name,name)
    else:
        report_in_sub(driver,asset_name,name)
        
    
def report_in_sub(driver,asset_name,name):
        tripsstatus = frappe.get_doc({
			"doctype": "Events",
							"driver": driver,
							"asset_name": asset_name,
							"date"	: nowdate(),
							"status" : "Reported In"
								})
        if tripsstatus:
            tripsstatus.insert()
            driver_report_data = frappe.get_doc("Driver Login Page", name)
            driver_report_data.report_status = 1
            driver_report_data.save()
        
        
   
@frappe.whitelist()
def url():
    domain = frappe.utils.get_url()
    return domain

@frappe.whitelist()
def truck_error():
    frappe.throw("truck number is not mentioned")
    
    
@frappe.whitelist()
def report_out(driver,asset_name,name):
    
        tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Reported Out"
			})
        if tripsstatus:
            tripsstatus.insert()
            driver_report_data = frappe.get_doc("Driver Login Page", name)
            driver_report_data.report_status = 0
            driver_report_data.save()
   
   
