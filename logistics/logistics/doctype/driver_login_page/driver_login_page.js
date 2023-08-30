// Copyright (c) 2023, techfinite and contributors
// For license information, please see license.txt
frappe.ui.form.on('Driver Login Page', {
    refresh: function(frm) {
        frm.fields_dict['reports_in'].$input.on('click', function() {
            // Redirect to a new URL
            frappe.call({
                method:"logistics.logistics.doctype.driver_login_page.driver_login_page.function"
            })
            window.location.href = "http://localhost:8000/app/todo/25b0133c6a";
        });
    }
});






