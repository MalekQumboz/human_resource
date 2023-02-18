# Copyright (c) 2023, malek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Attendance(Document):

	# def on_submit(self):
	# 	self.work_hours_()
	# 	self.late_hours_()
	# 	self.status_()
	def validate(self):
		self.work_hours_()
		self.late_hours_()
		self.status_()
		self.check_time()

	#Find the number of hours of delay when check_in
	def late_entry_(self):
		# Get data from the doctype Attendance Settings
		attendance_settings_doc=frappe.get_doc('Attendance Settings')
		start_time=attendance_settings_doc.start_time
		late_entry_grace_period=attendance_settings_doc.late_entry_grace_period
		late_entry_final=0

		#Find the number of hours late when checking out
		if self.check_in and self.check_in >=start_time:
			late_entry=frappe.utils.time_diff_in_seconds(self.check_in,start_time)/60
			if late_entry <= late_entry_grace_period:
				late_entry_final=0
			else:
				late_entry_final=late_entry-late_entry_grace_period

		return late_entry_final

	#Find the number of hours of delay when check_out
	def early_exit_(self):
		# Get data from the doctype Attendance Settings
		attendance_settings_doc = frappe.get_doc('Attendance Settings')
		end_time = attendance_settings_doc.end_time
		early_exit_grace_period=attendance_settings_doc.early_exit_grace_period
		early_exit_final=0

		#Find the number of hours late when checking out
		if self.check_out and self.check_out <= end_time:
			early_exit=frappe.utils.time_diff_in_seconds(end_time,self.check_out)/60
			if early_exit <=early_exit_grace_period:
				early_exit_final=0
			else:
				early_exit_final=early_exit-early_exit_grace_period

		return early_exit_final

	# Find the number of work hours
	def work_hours_(self):
		#Get data from the doctype
		attendance_settings_doc = frappe.get_doc('Attendance Settings')
		start_time=attendance_settings_doc.start_time
		end_time=attendance_settings_doc.end_time
		full_hours=frappe.utils.time_diff_in_hours(end_time ,start_time)

		#Fetch the allowed time for delay and convert it from minutes to hours
		late_entry_grace_period = attendance_settings_doc.late_entry_grace_period/60
		early_exit_grace_period = attendance_settings_doc.early_exit_grace_period/60

		#get a delay time
		late_entry = self.late_entry_()
		early_exit = self.early_exit_()

		work_hours=0
		if self.check_out and self.check_in and not(self.check_in < start_time and self.check_out <start_time) and not(self.check_in > end_time and self.check_out >end_time):
			#Verify that there are no delays and bring the number of working hours
			if late_entry == 0 and early_exit==0:
				work_hours = frappe.utils.time_diff_in_hours(end_time,start_time)
			elif late_entry==0:
				work_hours = frappe.utils.time_diff_in_hours(self.check_out,start_time)+early_exit_grace_period
			elif early_exit==0:
				work_hours = frappe.utils.time_diff_in_hours(end_time,self.check_in)+late_entry_grace_period
			else:
				work_hours = frappe.utils.time_diff_in_hours(self.check_out, self.check_in)

			if work_hours > full_hours:
				work_hours=full_hours

		self.work_hours=work_hours

	# Find the number of delay hours
	def late_hours_(self):
		late_entry=self.late_entry_()
		early_exit=self.early_exit_()
		self.late_hours=(late_entry + early_exit)/60

	# Change status according to the number of working hours
	def status_(self):
		# Get data from the doctype
		attendance_settings_doc = frappe.get_doc('Attendance Settings')
		working_hours_threshold_for_absent=attendance_settings_doc.working_hours_threshold_for_absent

		#Change status according to the number of working hours
		if self.work_hours:
			if float(working_hours_threshold_for_absent) != 0:
				if working_hours_threshold_for_absent >= self.work_hours:
					self.status='Absent'
				else:
					self.status = 'Present'

	def check_time(self):
		if frappe.utils.get_time(self.check_in) > frappe.utils.get_time(self.check_out) :
			frappe.throw('Check In must be before the Check Out.')


@frappe.whitelist()
def create_attendance(attendance_date=None,check_in=None,check_out=None):
	user=frappe.session.user
	employee_id=frappe.db.get_list('Employee', filters={ 'user': ['=', user] })
	employee_id=employee_id[0].name

	if attendance_date and check_in and check_out:
		doc=frappe.new_doc('Attendance')
		doc.employee=f"{employee_id}"
		doc.attendance_date=frappe.utils.getdate(attendance_date)
		doc.check_in=check_in
		doc.check_out=check_out
		doc.insert()
		return doc
	return []


