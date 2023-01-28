# Copyright (c) 2023, malek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveApplication(Document):
	def before_validate(self):
		self.total_leave_days_()
		self.leave_balance_()
		self.check_total_leave_days()

	def on_submit(self):
		self.update_leave_balance()
	def total_leave_days_(self):
		total_leave_days=0
		if self.from_date and self.to_date:
			total_leave_days=frappe.utils.date_diff(self.to_date,self.from_date)+1
		if total_leave_days >=0:
			self.total_leave_days=total_leave_days
	def leave_balance_(self):
		if self.employee and self.leave_type and self.from_date and self.to_date :
			leave_balance=frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
			where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
							   (self.employee,self.leave_type,self.from_date,self.to_date),as_dict=1)
		if leave_balance:
			self.leave_balance_before_application=leave_balance[0].total_leaves_allocated
	def check_total_leave_days(self):
		if self.from_date and self.to_date:
			total_leave_days=frappe.utils.date_diff(self.to_date,self.from_date)+1

		if self.employee and self.leave_type and self.from_date and self.to_date:
			leave_balance = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
			where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
										  (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		if leave_balance:
			leave_balance=leave_balance[0].total_leaves_allocated


		if total_leave_days > leave_balance:
			frappe.throw('The number of total leave days is greater than your leave balance')


	def update_leave_balance(self):
		leave_balance = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
		where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
										  (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		leave_balance=leave_balance[0].total_leaves_allocated

		total_leave_days=frappe.utils.date_diff(self.to_date,self.from_date)+1

		new_balance=leave_balance - total_leave_days

		update_leave_balance = frappe.db.sql(""" update `tabLeave Allocation` set  total_leaves_allocated=%s
					where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
									  (new_balance,self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)




