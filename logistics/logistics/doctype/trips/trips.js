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