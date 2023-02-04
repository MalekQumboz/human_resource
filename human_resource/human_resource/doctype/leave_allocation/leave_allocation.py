# Copyright (c) 2023, malek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveAllocation(Document):
	def validate(self):
		self.check_from_date()
		self.check_employee_allocation()

	# def on_submit(self):
	# 	self.check_employee_allocation()



	def check_from_date(self):
		if self.from_date > self.to_date :
			frappe.throw('The leave start date must be before the end date.')

	def check_employee_allocation(self):

		data = frappe.db.sql(""" SELECT employee FROM `tabLeave Allocation`
					where name !=%s and employee = %s  and leave_type = %s  and 
					( (from_date <= %s  and to_date >= %s) or (from_date <= %s  and to_date >= %s) 
						or (from_date >= %s  and to_date <= %s) )""",
					  (self.name,self.employee, self.leave_type, self.from_date, self.from_date,
					   self.to_date,self.to_date,self.from_date,self.to_date), as_dict=1)
		if data:
			frappe.throw("Leave Allocation for Employee already exists")


