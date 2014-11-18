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

		connect = ldap.open(server_details.get('ldap_server'))
	return connect, user_dn, base_dn
