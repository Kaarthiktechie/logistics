// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt

frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['start'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.start",
                args:{
                    trip_id:frm.doc.name
                },
                callback:function(trip_status_id){
                    console.log(trip_status_id.message)
                    window.location.href = "http://localhost:8000/app/trip-status/"+trip_status_id.message
                }});
        });
    }
});
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['trip_details'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.start",
                args:{
                    trip_id:frm.doc.name
                },
                callback:function(trip_status_id){
                    console.log(trip_status_id.message)
                    window.location.href = "http://localhost:8000/app/trip-status/"+trip_status_id.message
                }});
        });
    }
});
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict.start.$input.css({'font-size': '16px',
                                            "text-align":"center",
                                            "background-color": "#42a5fc",
                                            "color":"white",
                                            "height": "40px",
                                            "width": "150px"});
	}})
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict.trip_details.$input.css({'font-size': '16px',
        "text-align":"center",
        "background-color": "#42a5fc",
        "color":"white",
        "height": "40px",
        "width": "150px"});
    }})
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict.voucher.$input.css({'font-size': '16px',
        "text-align":"center",
        "background-color": "#42a5fc",
        "color":"white",
        "height": "40px",
        "width": "150px"});
    }})
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.close.$input.css({'font-size': '16px',
            "text-align":"center",
            "background-color": "#42a5fc",
            "color":"white",
            "height": "40px",
            "width": "150px"});
        }})