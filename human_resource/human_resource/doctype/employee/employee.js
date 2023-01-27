// Copyright (c) 2023, malek and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
	 refresh: function(frm) {
        frm.set_df_property('age', 'read_only','1');
        frm.set_df_property('full_name', 'read_only','1');
	 }
});
