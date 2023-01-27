# Copyright (c) 2023, malek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	def validate(self):
		self.diff_date()
		self.check_employee_age()
		self.full_name_()
		self.phone_length()
		self.phone_start()
		self.employee_education_()
	def diff_date(self):
		age = frappe.utils.date_diff(
			frappe.utils.getdate(frappe.utils.today), self.date_of_birth) / 365
		self.age = int(age)
	def check_employee_age(self):
		if self.age > 60 and self.status =='Active':
			frappe.throw('An Employee over the age of 60 connot have an Active status.')
	def full_name_(self):
		self.full_name=self.first_name+" "+self.middle_name+" "+self.last_name

	def phone_length(self):
		phone_len=len(self.phone)
		if not phone_len==10:
			frappe.throw('The number of phone must be 10 digits.')

	def phone_start(self):
		if not self.phone.startswith('059'):
			frappe.throw('The number of phone must start with 059')
	def employee_education_(self):
		count=len(self.employee_education)
		if count < 2:
			frappe.throw('The number of Education Qualifications must be at least tow.')

