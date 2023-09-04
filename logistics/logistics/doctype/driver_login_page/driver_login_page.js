// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_in'].$input.on('click', function() {
            // print(frm.is.new)
            
            if(cur_frm.doc.__islocal != 1){
                console.log(cur_frm.doc.__islocal)
                frappe.call({
                    method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_in",
                    args:{
                        driver: frm.doc.driver,
                        asset_name:frm.doc.asset_name,
                        
                    }
                })}
            else{
                frappe.throw("Please save the document")
            }
            
        }
        );
    }})

frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_out'].$input.on('click', function() {
            if(cur_frm.doc.__islocal != 1){
            console.log(cur_frm.doc.__islocal)
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_out",
                args:{
                    driver: frm.doc.driver,
                    asset_name:frm.doc.asset_name
                }
            })}
            else{
                frappe.throw("Please save the document")
            }
            
        });
    }})
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

    frappe.ui.form.on('Driver Login Page', {
        refresh: function(frm) {
            frm.add_custom_button("Trip", function() {
                window.location.href = "http://localhost:8000/app/trips/?asset_name="+frm.doc.asset_name+"&driver="+frm.doc.driver+"&date="+frm.doc.date
                    
            });
        }
    });
    frappe.ui.form.on('Driver Login Page', {
        refresh: function(frm) {
            frm.add_custom_button("Truck", function() {
                window.location.href = "http://localhost:8000/app/trips/?asset_name="+frm.doc.asset_name+"&driver="+frm.doc.driver+"&date="+frm.doc.date
                    
            });
        }
    });


