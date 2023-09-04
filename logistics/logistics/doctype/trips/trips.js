// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt



// Start
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict.start.$input.css({'font-size': '16px',
                                            "text-align":"center",
                                            "background-color": "#42a5fc",
                                            "color":"white",
                                            "height": "40px",
                                            "width": "150px",
                                            "margin": "0 auto",
                                            "display": "block"});
	}})
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.starting_km.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "height": "40px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})

    // Sin
    frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.fields_dict.sin_km.$input.css({'font-size': '16px',
                                                    "text-align":"center",
                                                    "height": "40px",
                                                    "margin": "0 auto",
                                                    "display": "block"});
    }})
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.s_in.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "background-color": "#42a5fc",
                                                "color":"white",
                                                "height": "40px",
                                                "width": "150px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})
    // Sout
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.s_out.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "background-color": "#42a5fc",
                                                "color":"white",
                                                "height": "40px",
                                                "width": "150px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})
    // Din
        frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.fields_dict.din_km.$input.css({'font-size': '16px',
                                                    "text-align":"center",
                                                    "height": "40px",
                                                    "margin": "0 auto",
                                                    "display": "block"});
    }})
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.d_in.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "background-color": "#42a5fc",
                                                "color":"white",
                                                "height": "40px",
                                                "width": "150px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})
    // Dout

    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.d_out.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "background-color": "#42a5fc",
                                                "color":"white",
                                                "height": "40px",
                                                "width": "150px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})
        
// Close
    frappe.ui.form.on('Trips', {
        refresh: function(frm) {
            frm.fields_dict.close.$input.css({'font-size': '16px',
            "text-align":"center",
            "background-color": "#42a5fc",
            "color":"white",
            "height": "40px",
            "width": "150px",
            "margin": "0 auto",
            "display": "block"
});
        }})

// Scripts

//for enabling and disabling button
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.status",
                args:{
                    trip_id:frm.doc.name
                },
                callback:function(status){
                    frm.toggle_display(['sin'], status.message.status == "Started");
                    frm.toggle_display(['s_in'], status.message.status == "Started");
                    frm.toggle_display(['s_out'], status.message.status == "S");
                }})
    }});

//onclick function for start
        frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.fields_dict['start'].$input.on('click', function() {
                    // cur_frm_set_df_property("start","read_only")
                    // console.log(frm.doc.docstatus)
                    if(frm.doc.starting_km != 0){
                    frappe.call({
                        method:"logistics.logistics.doctype.trips.trips.start",
                        args:{
                            trip_id:frm.doc.name,
                            driver:frm.doc.driver,
                            asset_name:frm.doc.asset_name
                        },callback:function(){
                            doc.save()
                        }
                        })}
                    else{
                        frappe.throw("Please enter Km to proceed")
                    }
                });
            }
        });
//truck action button at the top
        frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.add_custom_button("Truck", function() {
                    
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
//attendance action button at the top
        frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.add_custom_button("Attendance", function() {
                    
                    frappe.call({
                        method:"logistics.logistics.doctype.trips.trips.attendence",
                        args:{
                            trip_id:frm.doc.name,
                            asset_name:frm.doc.asset_name,
                            driver:frm.doc.driver
                        },
                        callback:function(trip_status_id){
                            console.log(trip_status_id.message)
                            window.location.href = "http://localhost:8000/app/driver-login-page/"+trip_status_id.message
                        }});
                        
                });
            }
        });

