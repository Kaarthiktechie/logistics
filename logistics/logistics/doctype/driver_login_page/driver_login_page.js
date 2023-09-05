// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt

//css style
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
            frm.fields_dict.reports_in.$input.css({'font-size': '16px',
            "text-align":"center",
            "background-color": "#42a5fc",
            "color":"white",
            "height": "40px",
            "width": "150px",
            "margin": "0 auto",
            "display": "block"});
    }})

frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
                frm.fields_dict.reports_out.$input.css({'font-size': '16px',
                "text-align":"center",
                "background-color": "#42a5fc",
                "color":"white",
                "height": "40px",
                "width": "150px",
                "margin": "0 auto",
                "display": "block"});
    }})


//enabling and disbling button
// frappe.ui.form.on('Driver Login Page', {
//     refresh: function(frm) {
//             if (frappe.reported_in == 1){
                
//             }
//             // 
            
//     }});

//report_in function

frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_in'].$input.on('click', function() {
                console.log(cur_frm.doc.__islocal)
                frappe.reported_in = 1
                frm.save()
                frappe.call({
                    method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_in",
                    args:{
                        driver: frm.doc.driver,
                        asset_name:frm.doc.asset_name,
                        
                    }
                }) 
        })
    }
})

//report out function

frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_out'].$input.on('click', function() {
            frm.save()
            console.log(cur_frm.doc.__islocal)
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_out",
                args:{
                    driver: frm.doc.driver,
                    asset_name:frm.doc.asset_name
                }
            })
        });
    }})

    //action buttons (trip&truck)

    frappe.ui.form.on('Driver Login Page', {
        refresh: function(frm) {
            frm.add_custom_button("Trip", function() {
                frappe.call({
                    method:"logistics.logistics.doctype.driver_login_page.driver_login_page.url",
                
                callback:function(domain){
                window.location.href = domain.message+"/app/trip/?asset_name="+frm.doc.asset_name+"&date="+frm.doc.date
            }})   
            });
        }
    });
    frappe.ui.form.on('Driver Login Page', {
        refresh: function(frm) {
            frm.add_custom_button("Truck", function() {
                frappe.call({
                    method:"logistics.logistics.doctype.driver_login_page.driver_login_page.url",
                
                callback:function(domain){
                window.location.href = domain.message+"/app/truck/?asset_name="+frm.doc.asset_name
            }})   
            });
        }
    });


