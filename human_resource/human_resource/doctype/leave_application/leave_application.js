// Copyright (c) 2023, malek and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Application', {
	// refresh: function(frm) {

	// }

	from_date:function(frm){
	frm.trigger("get_total_leave_days");
	},
	to_date:function(frm){
	frm.trigger("get_total_leave_days");
	},
	get_total_leave_days:function(frm){
	frappe.call({
	method:"human_resource.human_resource.doctype.leave_application.leave_application.get_total_leave_days",
	args:{
	from_date:frm.doc.from_date,
	to_date:frm.doc.to_date
	},
	callback:(r)=>{
	frm.doc.total_leave_days=r.message;
	frm.refresh()
	}
	})},

//
//    leave_type:function(frm){
//	frm.trigger("get_leave_balance");
//	},
//	employee:function(frm){
//	frm.trigger("get_leave_balance");
//	},
//	get_leave_balance:function(frm){
//	frappe.call({
//	method:"human_resource.human_resource.doctype.leave_application.leave_application.get_leave_balance",
//	args:{
//	employee:frm.doc.employee,
//	leave_type=frm.doc.leave_type,
//	from_date:frm.doc.from_date,
//	to_date:frm.doc.to_date
//	},
//	callback:(r)=>{
//	frm.doc.leave_balance_before_application=r.message;
//	frm.refresh()
//	}
//	})}
});
