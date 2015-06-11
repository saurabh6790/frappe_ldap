app_name = "frappe_ldap"
app_title = "LDAP"
app_publisher = "New Indictrnas"
app_description = "Ldap Auth"
app_icon = "icon-asterisk"
app_color = "#001122"
app_email = "saurabh.p@indinctranstech.com"
app_url = "www.indictrnastech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_ldap/css/frappe_ldap.css"
# app_include_js = "/assets/frappe_ldap/js/frappe_ldap.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_ldap/css/frappe_ldap.css"
# web_include_js = "/assets/frappe_ldap/js/frappe_ldap.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

fixtures=["LDAP ERP Role Mapper"]

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_ldap.install.before_install"
# after_install = "frappe_ldap.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_ldap.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"frappe_ldap.sync_profile.check_profiles_daily"
	],
	"daily": [
		"frappe_ldap.sync_profile.check_profiles_daily"
	],
	"weekly": [
		"frappe_ldap.sync_profile.check_profiles_weekly"
	],
	"monthly": [
		"frappe_ldap.sync_profile.check_profiles_monthly"
	]
}

# Testing
# -------

# before_tests = "frappe_ldap.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.core.doctype.event.event.get_events": "frappe_ldap.event.get_events"
# }

