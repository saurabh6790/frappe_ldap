from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe import _


@frappe.whitelist(allow_guest=True)
def ldap_login(user, pwd, provider=None):
	#### LDAP LOGIN LOGIC #####
	user=ldap_authentication(user, pwd)

	frappe.local.login_manager.user = user
	frappe.local.login_manager.post_login()

	# redirect!
	frappe.local.response["type"] = "redirect"

	# the #desktop is added to prevent a facebook redirect bug
	frappe.local.response["location"] = "/desk#desktop" if frappe.local.response.get('message') == 'Logged In' else "/"

	# because of a GET request!
	frappe.db.commit()

def ldap_authentication(user, pwd):
	server_details = get_details()
	user, user_id, status, role = ldap_auth(user,pwd,server_details)
	check_profile(user, user_id, pwd, role)
	return user

def ldap_auth(user, pwd, server_details):
	from frappe_ldap.ldap.doctype.ldap_settings.ldap_settings import set_ldap_connection
	import ldap

	status = True
	mail = None
	user_id = None
	dn = None

	conn, user_dn, base_dn = set_ldap_connection(server_details)
	filters = "uid=*"+user+"*"
	role = 'Default'
	try:
		# l = ldap.initialize('ldap://ldap.forumsys.com/')
		conn.simple_bind_s(user_dn, pwd)
		result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filters)

		for dn, r in result:
			dn = str(dn)
			mail = str(r['mail'][0])
			user_id = str(r['uid'][0])
			role = r.get('description') if r.get('description') else 'Default'
		if dn:
			conn.simple_bind_s(dn,pwd)
			status = True
		else:
			frappe.msgprint("Not a valid LDAP user", raise_exception=1)
	except ldap.LDAPError, e:
		conn.unbind_s()
		status = False
		frappe.msgprint("Incorrect UserId or Password", raise_exception=1)
	return mail, user_id, status, role

def check_profile(user, user_id, pwd, role,enabled_profiles=[]):
	"check for profile, if not exist creates new profile"
	profile = frappe.db.sql("select name from tabUser where name = %s",user)

	#Make session user as Admin to create share doc entry
	frappe.session.user = 'Administrator'

	if not profile:
		from frappe.utils import nowdate, nowtime
		d = frappe.new_doc("User")
		d.owner = "Administrator"
		d.email = user
		d.first_name = user_id
		d.enabled = 1
		d.new_password = pwd
		d.creation = nowdate() + ' ' + nowtime()
		d.user_type = "System User"
		d.save(ignore_permissions=True)
		enabled_profiles.append(user_id)
		assign_role(user, user_id, role)

def assign_role(user, user_id, role):
	roles_list = get_role_list(role)
	for role in roles_list:
		ur = frappe.new_doc('UserRole')
		ur.parent=user
		ur.parentfield='user_roles'
		ur.parenttype='User'
		ur.role= role[0]
		ur.save()

def get_role_list(roles):
	role_list = []
	for role in roles.split(','):
		role_list=frappe.db.sql("select role from `tabRole Mapper Details` where parent='%s'"%(role),as_list=1)
	return role_list

def check_if_enabled(user):
	"""raise exception if user not enabled"""
	from frappe.utils import cint
	if user=='Administrator': return
	if not cint(frappe.db.get_value('User', user, 'enabled')):
		frappe.msgprint('User disabled or missing',raise_exception=1)

def get_details():
	return frappe.db.get_value("LDAP Settings",None,['ldap_server','user_dn','base_dn','pwd'],as_dict=1)
