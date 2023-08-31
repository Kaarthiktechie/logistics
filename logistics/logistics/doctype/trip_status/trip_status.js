// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt

frappe.ui.form.on('Trip Status', {
	before_save: function(frm) {
            frappe.call({
                method:"logistics.logistics.doctype.trip_status.trip_status.status_check",
				args:{
					source_in : frm.doc.source_in ,
					source_out : frm.doc.source_out,
					destination_in : frm.doc.destination_in,
					destination_out: frm.doc.destination_out
				},callback: function(response){
					var status = response.message;
					// console.log(status)
					if(status!= 0){
						if(status == "sin"){
							console.log(status)
							frm.set_df_property('source_in', 'read_only', 1);
							frm.set_df_property('source_out', 'read_only', 0);
						}
						if(status == "sout"){
							console.log(status)
							frm.set_df_property('source_out', 'read_only', 1);
							frm.set_df_property('destination_in', 'read_only', 0);					
						}
						if(status == "din"){
							console.log(status)
							frm.set_df_property('destination_in', 'read_only', 1);
							frm.set_df_property('destination_out', 'read_only', 0);
						}
						if(status == "dout"){
							console.log(status)
							frm.set_df_property('destination_out', 'read_only', 1);
						}
					}
					else{
						frm.set_df_property('source_in', 'read_only', 0);
						frm.set_df_property('source_out', 'read_only', 1);
						frm.set_df_property('destination_in', 'read_only', 1);
						frm.set_df_property('destination_out', 'read_only', 1);
					}
					// frappe.msgprint(status)
				}
				
            })
            
        }
	}
);
