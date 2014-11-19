import ldap, sys, frappe
from frappe.utils import nowdate,  nowtime, cstr
from frappe.utils.email_lib import sendmail

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

	except ldap.LDAPError, e:
		connect.unbind_s()

	#search for profiels
	result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,filters)
	
	for dn, r in result:
		exist = profile_check(r.get('mail'))

		if r.get('mail'):	
			enabled_profiles.append(r.get('mail')[0])

		if not exist and r.get('mail'):
			create_profile(r.get('mail')[0], r.get('uid')[0])
			if r.get('mail'):
				new_created.append(r.get('uid')[0])

	disable_profiles(enabled_profiles)
	admin_notification(new_created)

def profile_check(usr):
	if usr:
		return frappe.db.sql("select true from tabProfile where name =  %s",str(usr[0]))

def create_profile(usr, name):
	d = frappe.new_doc("User")
	d.owner = "Administrator"
	d.email = user
	d.first_name = user_id
	d.enabled = 1
	d.new_password = pwd
	d.creation = nowdate() + ' ' + nowtime()
	d.user_type = "System User"
	d.save(ignore_permissions=True)

def disable_profiles(enabled_profiles):
	profiels = []
	for pro in enabled_profiles:
		profiels.append("'%s'"%pro)

	profile = frappe.db.sql("select name from tabProfile where email not in (%s)"%str(','.join(profiels)),as_list=1)
	
	for pro in profile:
		frappe.db.sql("update tabProfile set enabled = 0 where name = '%s' and name not in ('Administrator','Guest')"%pro[0])

def admin_notification(new_profiels):
	msg = get_message(new_profiels)
	receiver = frappe.db.get_value('User', 'Administrator', 'email')
	subj = "Newly Created profiels"

	sendmail(receiver, subject=subj, msg = cstr(msg))

def get_message(new_profiels):

	return """ Hello Admin. Profiles has been synced. Please check the assigned roles to them. List is as follws:\n %s """%'\n'.join(new_profiels)