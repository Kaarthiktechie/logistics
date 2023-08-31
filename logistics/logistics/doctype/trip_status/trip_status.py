# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime
class TripStatus(Document):
	pass
	
@frappe.whitelist()
def status_check(source_in,source_out,destination_in,destination_out):	
		all_status = {"sin" : source_in,
            			"sout":source_out,
               		"din" : destination_in,
                	"dout" : destination_out}
		sin = all_status["sin"]
		sout =  all_status["sout"]
		din = all_status["din"]
		dout = all_status["dout"]
		if sin  == "1":
			status = "sin"
			if sout == "1":
				status = "sout"
				if din == "1":
					status = "din"
					if dout == "1":
						status = "dout"
		else:
			status = 0

		return status
