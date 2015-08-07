import ldap, sys, frappe
from frappe.utils import nowdate,  nowtime, cstr
from frappe import sendmail
from templates.pages.ldap_login import check_profile
from frappe.utils import random_string

def check_profiles_daily():
	check_profiles_if("Daily")

def check_profiles_weekly():
	check_profiles_if("Weekly")

def check_profiles_monthly():
	check_profiles_if("Monthly")

def check_profiles_if(freq):
	if frappe.db.get_value("LDAP Settings", None, "sync_frequency")==freq:
		ldap_connect()

def ldap_connect():
	import ldap
	from frappe_ldap.templates.pages.ldap_login import get_details
	from frappe_ldap.ldap.doctype.ldap_settings.ldap_settings import set_ldap_connection

	server_details = get_details()

	connect, user_dn, base_dn = set_ldap_connection(server_details)
	filters =  "uid=*"

	new_created = []
	enabled_profiles = []

	try:
		#if authentication successful, get the full user data
		connect.simple_bind_s(user_dn, server_details.get('pwd'))
	except :
		connect.unbind_s()

	#search for profiels
	result = connect.search_s(base_dn, 2,filters)

	for dn, r in result:
		if r.get('mail'):
			password = random_string(10)
			role = r.get('description') if r.get('description') else 'Default'
			check_profile(r.get('mail')[0], r.get('uid')[0], password, role, new_created)
			enabled_profiles.append(r.get('mail')[0])

	disable_profiles(enabled_profiles)
	admin_notification(new_created)

def disable_profiles(enabled_profiles):
	profiles = []
	enabled_profiles.extend([x[0] for x in get_system_manger()])

	for pro in enabled_profiles:
		profiles.append("'%s'"%pro)

	if len(profiles)>=1:
		profile = frappe.db.sql("select name from tabUser where email not in (%s)"%str(','.join(profiles)),as_list=1)
	else:
		profile = []

	for pro in profile:
		frappe.db.sql("update tabUser set enabled = 0 where name = '%s' and name not in ('Administrator','Guest')"%pro[0])

def get_system_manger():
	return frappe.db.sql("""select parent from tabUserRole
		where role = 'System Manager'
			and parent not in ('Administrator')""",as_list=1)

def admin_notification(new_profiels):
	msg = get_message(new_profiels)
	receiver = frappe.db.sql("select parent from tabUserRole where role = 'System Manager' and parent not like '%administrator%'", as_list=1)[0]
	
	if len(new_profiels) >= 1:
		frappe.sendmail(recipients=receiver, sender=None, subject="[LDAP-ERP] Newly Created Profiles", message=cstr(msg))

def get_message(new_profiels):
	return """ Hello Admin. \n
			Profiles has been synced. \n
			Please check the assigned roles to them. \n
			List is as follws:\n %s """%'\n'.join(new_profiels)
