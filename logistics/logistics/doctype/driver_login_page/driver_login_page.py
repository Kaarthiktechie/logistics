# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime
class DriverLoginPage(Document):
    pass

def validate_status(asset_name, current_status):

        last_events = frappe.db.sql(
        """SELECT * from tabEvents e1, 
        (select max(name) as name from tabEvents 
        where asset_name = %s and type = 'Attendance') e2
        where e1.name = e2.name
        """,
        asset_name,
        as_dict=True)
        # try:
        #     if last_events:
        #         last_event = last_events[0]
        #         if last_event.status == current_status:
        #             raise Exception(f"Truck no {asset_name} is already assigned to a driver")
        # except Exception as e:
        #     frappe.throw(str(e))
        #     return None

        if last_events:
            last_event = last_events[0]
            if last_event.status == current_status:
               
                frappe.throw(f"Truck no {asset_name} is already assigned to a driver")
                return None
    
@frappe.whitelist()
def report_in(driver,asset_name,name):

    validate_status(asset_name, "Reported In")
    report_in_sub(driver,asset_name,name)
    frappe.msgprint("You have reported in successfully")
    return None
def report_in_sub(driver,asset_name,name):
        tripsstatus = frappe.get_doc({
			"doctype": "Events",
							"driver": driver,
							"asset_name": asset_name,
							"date"	: nowdate(),
							"status" : "Reported In",
                                "type": "Attendance"
								})
        if tripsstatus:
            tripsstatus.insert()


        
   
@frappe.whitelist()
def url():
    domain = frappe.utils.get_url()
    return domain

@frappe.whitelist()
def truck_error():
    frappe.throw("truck number is not mentioned")
    
    
@frappe.whitelist()
def report_out(driver,asset_name,name):
    query = """SELECT * from tabEvents where type = "Attendance" and (status = "Reported In" Or status = "Reported Out") ORDER BY name DESC LIMIT 1;"""
    # tripstatus = frappe.db.sql("Select * from tabEvents where type = Attendance and status = (Reported In OR  Reported Out")
    results = frappe.db.sql(query, as_dict = True)
    if results:
        result = results[0]
            
    if result.status == "Reported In":
        tripsstatus = frappe.get_doc({
			"doctype": "Events",
			"driver": driver,
			"asset_name": asset_name,
			"date"	: nowdate(),
			"status" : "Reported Out",
            "type": "Attendance"
			})
        if tripsstatus:
            tripsstatus.insert()
            driver_report_data = frappe.get_doc("Driver Login Page", name)
            driver_report_data.report_status = 0
            driver_report_data.save()
            frappe.msgprint("You have reported out successfully")
   
   
