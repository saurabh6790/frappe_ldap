# Copyright (c) 2013, New Indictrnas and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import ldap

class LDAPSettings(Document):
	pass

def set_ldap_connection(server_details):
	if server_details:
		# the following is the user_dn format provided by the ldap server
		user_dn = server_details.get('user_dn')

		# adjust this to your base dn for searching
		base_dn = server_details.get('base_dn')
		try:
			if server_details.get('ldap_server'):
				connect = ldap.initialize(server_details.get('ldap_server'))
			else:
				frappe.msgprint("Please setup server details", raise_exception=1)
		except ldap.LDAPError, e:
			frappe.msgprint("Connection Filed!!! Contact System Manager", raise_exception=1)

		return connect, user_dn, base_dn
