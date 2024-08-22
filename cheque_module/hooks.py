app_name = "cheque_module"
app_title = "Cheque Module"
app_publisher = "Zewail"
app_description = "A custom App to Handle Cheque Transaction Through ERPNext"
app_email = "unclee919@gmail.com"
app_license = "MIT"

# Document Events
# doc_events = {
#     "Receivable Cheque": {
#         "onload": "cheque_module.buutons.setup_buttons",  # Correct path based on file location
#     },
#     "Payment Entry": {
#         # "before_save": "cheque_module.cheque.before_save",
#         "before_submit": "cheque_module.cheque.before_submit",
#         "on_submit": "cheque_module.cheque.on_submit",
#          "validate": "cheque_module.cheque.validate_cheque_fields",
#     }
# }

# # Include Python Files
# import cheque_module.buutons
# import cheque_module.cheque

###############################################################


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/excuse_custom/css/excuse_custom.css"
# app_include_js = "/assets/excuse_custom/js/excuse_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/excuse_custom/css/excuse_custom.css"
# web_include_js = "/assets/excuse_custom/js/excuse_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "excuse_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Payment Entry" : "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "excuse_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "excuse_custom.utils.jinja_methods",
# 	"filters": "excuse_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "excuse_custom.install.before_install"
# after_install = "excuse_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "excuse_custom.uninstall.before_uninstall"
# after_uninstall = "excuse_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "excuse_custom.utils.before_app_install"
# after_app_install = "excuse_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "excuse_custom.utils.before_app_uninstall"
# after_app_uninstall = "excuse_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "excuse_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events


# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"excuse_custom.tasks.all"
# 	],
# 	"daily": [
# 		"excuse_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"excuse_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"excuse_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"excuse_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "excuse_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "excuse_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "excuse_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#


# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["excuse_custom.utils.before_request"]
# after_request = ["excuse_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["excuse_custom.utils.before_job"]
# after_job = ["excuse_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"excuse_custom.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.


# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


