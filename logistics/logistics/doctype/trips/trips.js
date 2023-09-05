// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt

//Confirm
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict.confirm.$input.css({'font-size': '16px',
                                            "text-align":"center",
                                            "background-color": "#42a5fc",
                                            "color":"white",
                                            "height": "40px",
                                            "width": "150px",
                                            "margin": "0 auto",
                                            "display": "block"});
	}})
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
// for making the driver details as login
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['confirm'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.driver",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name,
                    date:frm.doc.date
                },callback:function(driver){
                    console.log("cur_frm.doc.asset_name ->" + cur_frm.doc.asset_name)
                    frm.doc.employee=driver.message;
                    frm.refresh_field("employee");
                }})})}
                })

//for enabling and disabling button
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.status",
                args:{
                    trip_id:frm.doc.name
                },
                callback:function(status){
                    frm.toggle_display(["confirm"], status.message.status == "Assigned");
                    frm.toggle_display(["starting_km"], status.message.status == "Confirmed"),
                    frm.toggle_display(["start"], status.message.status == "Confirmed"),
                    frm.toggle_display(['sin_km'], status.message.status == "Started"),
                    frm.toggle_display(['s_in'], status.message.status == "Started"),
                    frm.toggle_display(['s_out'], status.message.status == "Sin"),
                    frm.toggle_display(['din_km'], status.message.status == "Sout"),
                    frm.toggle_display(['d_in'], status.message.status == "Sout"),
                    frm.toggle_display(['d_out'], status.message.status == "Din"),
                    frm.toggle_display(['close'], status.message.status == "Dout");

                }})
    }});

//assigned  code
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        if (frm.doc.asset_name){
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.assigned",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
            })
        }}})
    
//confirmation code
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['confirm'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.confirm",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
            });frm.refresh()})
        }})


//onclick function for start
        frappe.ui.form.on('Trips', {
            refresh: function(frm) {
                frm.fields_dict['start'].$input.on('click', function() {
                    // cur_frm_set_df_property("start","read_only")
                    // console.log(frm.doc.docstatus)
                    frm.save()
                    frappe.call({
                        method:"logistics.logistics.doctype.trips.trips.start",
                        args:{
                            trip_id:frm.doc.name,
                            asset_name:frm.doc.asset_name
                        }
                        })
                });
            }
        });

// Sin
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['s_in'].$input.on('click', function() {
            //fkhkfg
            frm.save()
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.sin",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
                frm.refresh();
        });
    }
});

//Sout
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['s_out'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.sout",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
            frm.refresh();
        });
    }
});

//Din
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['d_in'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.din",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
               
        });
    }
});

//Dout
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['d_out'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.dout",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
                frm.refresh();
        });
    }
});

//Close
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        frm.fields_dict['close'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trips.trips.close",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
                frm.refresh();
        })
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
                           
                        },
                        callback:function(trip_status_id){
                            console.log(trip_status_id.message)
                            window.location.href = "http://localhost:8000/app/driver-login-page/"+trip_status_id.message
                        }});
                        
                });
            }
        });

