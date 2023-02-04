# Copyright (c) 2023, malek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveApplication(Document):
	def before_validate(self):
		self.total_leave_days_()
		self.leave_balance_()
		self.check_total_leave_days()
		self.check_from_date()
		self.max_continuous_days_allowed()
		self.check_applicable()

	def on_submit(self):
		self.update_leave_balance()

	def on_cancel(self):
		self.Cancel_Leave_Application()

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

	def negative_balance_(self):
		if self.leave_type :
			negative_balance = frappe.db.sql(""" SELECT negative_balance FROM `tabLeave Type`
			where leave_type_name = %s """,(self.leave_type), as_dict=1)
		if negative_balance:
			negative_balance = negative_balance[0].negative_balance
			return negative_balance


	def check_total_leave_days(self):
		if self.from_date and self.to_date:
			total_leave_days=frappe.utils.date_diff(self.to_date,self.from_date)+1

		if self.employee and self.leave_type and self.from_date and self.to_date:
			leave_balance = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
			where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
										  (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)


		if leave_balance:
			leave_balance=leave_balance[0].total_leaves_allocated
			negative_balance=self.negative_balance_()

			if negative_balance ==0:
				if total_leave_days > leave_balance:
					frappe.throw('The number of total leave days is greater than your leave balance')
		else:
			frappe.throw('The employee does not have this leave type or the leave days you chose are out of range.')


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

	def  Cancel_Leave_Application(self):
		if self.employee and self.leave_type and self.from_date and self.to_date:
			leave_balance = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
			where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
										  (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		if leave_balance:
			leave_balance=leave_balance[0].total_leaves_allocated

		new_leave_balance= self.total_leave_days +leave_balance

		update_leave_balance = frappe.db.sql(""" update `tabLeave Allocation` set  total_leaves_allocated=%s
							where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
											 (new_leave_balance, self.employee, self.leave_type, self.from_date, self.to_date),

											 as_dict=1)
	def check_from_date(self):
		if self.from_date > self.to_date :
			frappe.throw('The leave start date must be before the end date.')


	def max_continuous_days_allowed(self):
		if self.leave_type :
			days_allowed = frappe.db.sql(""" SELECT max_continuous_days_allowed FROM `tabLeave Type`
			where leave_type_name = %s """,(self.leave_type), as_dict=1)
		if days_allowed:
			days_allowed = days_allowed[0].max_continuous_days_allowed
			if self.total_leave_days >days_allowed:
				frappe.throw(f"""The number of continuous leave days must be {days_allowed} or less """)


	def check_applicable(self):
		if self.employee and self.leave_type and self.from_date and self.to_date:
			applicable = frappe.db.sql(""" SELECT applicable FROM `tabLeave Allocation`
			where employee = %s  and leave_type = %s  """,
										  (self.employee, self.leave_type), as_dict=1)
		if applicable:
			applicable=applicable[0].applicable
			if self.from_date :
				applicable_days = frappe.utils.date_diff(self.from_date, frappe.utils.getdate(frappe.utils.today)) + 1
			if applicable_days <applicable :
				frappe.throw(f"""The leave request must be submitted at least {applicable} days in advance.""")


@frappe.whitelist()
def get_total_leave_days(from_date=None ,to_date=None):
	total_leave_days = 0
	if from_date and to_date:
		total_leave_days = frappe.utils.date_diff(to_date, from_date) + 1
	if total_leave_days >= 0:
		return total_leave_days
	else:
		return 0
@frappe.whitelist()
def get_leave_balance(employee=None ,leave_type=None ,from_date=None ,to_date=None):
	if employee and leave_type and from_date and to_date:
		leave_balance = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
		where employee = %s  and leave_type = %s  and from_date <= %s  and to_date >= %s  """,
									  (employee,leave_type, from_date, to_date), as_dict=1)
	if leave_balance:
		return leave_balance[0].total_leaves_allocated
	else:
		return 0



