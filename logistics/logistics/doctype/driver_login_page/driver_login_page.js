// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_in'].$input.on('click', function() {
            frm.toggle_enable('reports_in', false);
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_in",
                args:{
                    driver: frm.doc.driver,
                    asset_name:frm.doc.asset_name
                }
            })
            
        });
    }})
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['trip'].$input.on('click', function() {
            window.location.href = "http://localhost:8000/app/trips/?asset_name="+frm.doc.asset_name+"&driver="+frm.doc.driver+"&date="+frm.doc.date
            });
        }})
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_out'].$input.on('click', function() {
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.report_out",
                args:{
                    driver: frm.doc.driver,
                    asset_name:frm.doc.asset_name
                }
            })
            
        });
    }})






