# cheque_module/buutons.py

import frappe
from frappe import _

def setup_buttons(doc):
    if doc.doctype == 'Receivable Cheque':   
        setup_receivable_cheque_buttons(doc)
    elif doc.doctype == 'Payment Entry':
        setup_payment_entry_buttons(doc)

def setup_receivable_cheque_buttons(doc):
    if doc.docstatus == 1:
        doc.add_custom_button(_('Actions'), '', 'Actions')

    if doc.location != 'Bank':  # Example condition
        doc.page.add_action_item(_('Move to Bank'), lambda: move_to_bank_action(doc))
    
    doc.page.add_action_item(_('Collect Cash'), lambda: collect_cash_action(doc))
    doc.page.add_action_item(_('Collect Bank'), lambda: collect_bank_action(doc))
    doc.page.add_action_item(_('Bounce'), lambda: bounce_action(doc))
    doc.page.add_action_item(_('Cancel'), lambda: cancel_action(doc))
    doc.page.add_action_item(_('Return Back'), lambda: delivered_to_customer_action(doc))

# Other functions like move_to_bank_action, collect_cash_action, etc.
