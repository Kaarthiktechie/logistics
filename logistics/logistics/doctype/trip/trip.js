// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt

//Confirm
frappe.ui.form.on('Trip', {
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
frappe.ui.form.on('Trip', {
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
    frappe.ui.form.on('Trip', {
        refresh: function(frm) {
            frm.fields_dict.starting_km.$input.css({'font-size': '16px',
                                                "text-align":"center",
                                                "height": "40px",
                                                "margin": "0 auto",
                                                "display": "block"});
        }})

    // Sin
    frappe.ui.form.on('Trip', {
            refresh: function(frm) {
                frm.fields_dict.sin_km.$input.css({'font-size': '16px',
                                                    "text-align":"center",
                                                    "height": "40px",
                                                    "margin": "0 auto",
                                                    "display": "block"});
    }})
    frappe.ui.form.on('Trip', {
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
    frappe.ui.form.on('Trip', {
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
        frappe.ui.form.on('Trip', {
            refresh: function(frm) {
                frm.fields_dict.din_km.$input.css({'font-size': '16px',
                                                    "text-align":"center",
                                                    "height": "40px",
                                                    "margin": "0 auto",
                                                    "display": "block"});
    }})
    frappe.ui.form.on('Trip', {
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

    frappe.ui.form.on('Trip', {
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

frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict.closing_km.$input.css({'font-size': '16px',
                                            "text-align":"center",
                                            "height": "40px",
                                            "margin": "0 auto",
                                            "display": "block"});
}})
    frappe.ui.form.on('Trip', {
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
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['confirm'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.driver",
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
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.status",
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
                    frm.toggle_display(['closing_km'], status.message.status == "Dout"),
                    frm.toggle_display(['close'], status.message.status == "Dout");

                }})
    }});

//assigned  code
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        if (frm.doc.asset_name){
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.assigned",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
            })
        }}})
    
//confirmation code
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['confirm'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.confirm",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
            });frm.refresh()})
        }})


//onclick function for start
        frappe.ui.form.on('Trip', {
            refresh: function(frm) {
                frm.fields_dict['start'].$input.on('click', function() {
                    if (frm.doc.starting_km != 0){
                    frm.save()
                    frappe.call({
                        method:"logistics.logistics.doctype.trip.trip.start",
                        args:{
                            trip_id:frm.doc.name,
                            asset_name:frm.doc.asset_name
                        }
                        })
                        }
                        else{
                            frappe.throw("Please specify the Km before Start")
                        }
                    });
            }
        });

// Sin
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['s_in'].$input.on('click', function() {
            //fkhkfg
            frm.save()
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.sin",
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
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['s_out'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.sout",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
            frm.refresh_field("s_out");
        });
    }
});

//Din
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['d_in'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.din",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
               
        });
    }
});

//Dout
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['d_out'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.dout",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
                frm.refresh_field("d_out");
        });
    }
});

//Close
frappe.ui.form.on('Trip', {
    refresh: function(frm) {
        frm.fields_dict['close'].$input.on('click', function() {
            frm.save();
            frappe.call({
                method:"logistics.logistics.doctype.trip.trip.close",
                args:{
                    trip_id:frm.doc.name,
                    asset_name:frm.doc.asset_name
                }
                });
                frm.refresh_field("close","closed_km");
        })
    }
});
//trip action button at top
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.add_custom_button("Truck", function() {
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.url",
            
            callback:function(domain){
            window.location.href = domain.message+"/app/truck/?asset_name="+asset_name
        }})   
        });
    }
})
//truck action button at the top
        frappe.ui.form.on('Trip', {
            refresh: function(frm) {
                frm.add_custom_button("Truck", function() {
                    
                    frappe.call({
                        method:"logistics.logistics.doctype.trip.trip.start",
                        args:{
                            trip_id:frm.doc.name
                        },
                        callback:function(trip_status_id){
                            console.log(trip_status_id.message)
                            window.location.href = "http://localhost:8000/app/trip-status/"+trip_status_id.message
                        }});
                        
                });
            }
        })

//attendance action button at the top
        frappe.ui.form.on('Trip', {
            refresh: function(frm) {
                frm.add_custom_button("Attendance", function() {
                    
                    frappe.call({
                        method:"logistics.logistics.doctype.trip.trip.attendence",
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
