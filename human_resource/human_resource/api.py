# import frappe
#
#
# @frappe.whitelist()
# def create_attendance(attendance_date=None,check_in=None,check_out=None):
# 	user=frappe.session.user
# 	employee_id=frappe.db.get_list('Employee', filters={ 'user': ['=', user] })
# 	employee_id=employee_id[0].name
#
# 	if attendance_date and check_in and check_out:
# 		doc=frappe.new_doc('Attendance')
# 		doc.employee=f"{employee_id}"
# 		doc.attendance_date=frappe.utils.getdate(attendance_date)
# 		doc.check_in=check_in
# 		doc.check_out=check_out
# 		doc.insert()
# 		return doc
# 	return []