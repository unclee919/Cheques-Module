# In your custom app's Python file, e.g., `receivable_cheque.py` and `payment_entry.py`

import frappe

# Receivable Cheque Actions

@frappe.whitelist()
def move_to_bank(docname, bank, bank_account):
    doc = frappe.get_doc('Receivable Cheque', docname)
    doc.store_in_bank = bank
    doc.store_in_bank_account = bank_account
    doc.location = 'Bank'
    doc.move_to_bank_date = frappe.utils.nowdate()

    if doc.docstatus == 1:
        doc.submit()
        frappe.msgprint(_('Store in Bank and Bank Account updated successfully.'))
    else:
        doc.save()
        frappe.msgprint(_('Store in Bank and Bank Account updated successfully.'))

@frappe.whitelist()
def create_payment_entry(docname, payment_type):
    doc = frappe.get_doc('Receivable Cheque', docname)
    payment_entry = frappe.new_doc('Payment Entry')
    payment_entry.naming_series = 'ACC-PAY-.YYYY.-'
    payment_entry.posting_date = frappe.utils.nowdate()
    payment_entry.mode_of_payment = doc.source_mode_of_payment
    payment_entry.payment_type = payment_type
    payment_entry.paid_from = doc.against_account
    payment_entry.paid_to = doc.bank_company_account if payment_type == 'Collect Bank' else ''
    payment_entry.paid_amount = doc.cheque_amount
    payment_entry.received_amount = doc.cheque_amount
    payment_entry.reference_no = doc.cheque_number
    payment_entry.reference_date = doc.due_date
    payment_entry.company = doc.company
    payment_entry.insert()
    return payment_entry.name

@frappe.whitelist()
def bounce_cheque(docname):
    doc = frappe.get_doc('Receivable Cheque', docname)
    doc.status = 'Bounced'
    doc.save()
    frappe.msgprint(_('Cheque status updated to Bounced.'))

@frappe.whitelist()
def cancel_cheque(docname):
    doc = frappe.get_doc('Receivable Cheque', docname)
    doc.status = 'Cancelled'
    doc.save()
    frappe.msgprint(_('Cheque status updated to Cancelled.'))

@frappe.whitelist()
def deliver_to_customer(docname):
    doc = frappe.get_doc('Receivable Cheque', docname)
    doc.status = 'Delivered to Customer'
    doc.save()
    frappe.msgprint(_('Cheque status updated to Delivered to Customer.'))

# Payment Entry Actions

@frappe.whitelist()
def add_cheque_rows(docname):
    doc = frappe.get_doc('Payment Entry', docname)
    number_of_cheques = doc.custom_number_of_cheques
    reference_date = doc.reference_date
    reference_no = int(doc.reference_no) if doc.reference_no else 0

    if not reference_date:
        frappe.throw(_('Please ensure the Reference Date field is filled.'))

    doc.custom_cheques_table = []
    for i in range(number_of_cheques):
        row = doc.append('custom_cheques_table')
        row.against_bank = doc.custom_customer_bank
        row.cheque_number = reference_no + i

    update_cheque_details(doc)
    doc.save()

@frappe.whitelist()
def update_cheque_details(docname):
    doc = frappe.get_doc('Payment Entry', docname)
    reference_date = doc.reference_date
    plane_term = doc.custom_plane_term
    reference_no = int(doc.reference_no) if doc.reference_no else 0

    if not reference_date:
        frappe.throw(_('Please ensure the Reference Date field is filled.'))

    for idx, row in enumerate(doc.custom_cheques_table):
        due_date = frappe.utils.add_days(reference_date, idx * 30)  # Adjust based on plane_term

        if plane_term == 'Monthly':
            due_date = frappe.utils.add_months(reference_date, idx)
        elif plane_term == 'Quarterly':
            due_date = frappe.utils.add_months(reference_date, 3 * idx)
        elif plane_term == 'Semiannually':
            due_date = frappe.utils.add_months(reference_date, 6 * idx)
        elif plane_term == 'Annually':
            due_date = frappe.utils.add_years(reference_date, idx)

        row.cheque_due_date = frappe.utils.formatdate(due_date)
        row.against_bank = doc.custom_customer_bank
        row.cheque_number = reference_no + idx

    doc.save()

@frappe.whitelist()
def update_cheque_amount(docname):
    doc = frappe.get_doc('Payment Entry', docname)
    paid_amount = doc.paid_amount
    number_of_cheques = doc.custom_number_of_cheques
    is_equal = doc.custom_is_equal

    if is_equal:
        cheque_amount = paid_amount / number_of_cheques
        for row in doc.custom_cheques_table:
            row.cheque_amount = cheque_amount
    else:
        for row in doc.custom_cheques_table:
            row.cheque_amount = paid_amount

    doc.save()
    update_total_cheques_amount(doc)

@frappe.whitelist()
def update_total_cheques_amount(docname):
    doc = frappe.get_doc('Payment Entry', docname)
    total_cheque_amount = sum(row.cheque_amount for row in doc.custom_cheques_table)
    doc.custom_total_cheques_amount = total_cheque_amount
    doc.save()

@frappe.whitelist()
def create_receivable_cheques(docname):
    doc = frappe.get_doc('Payment Entry', docname)

    if doc.payment_type == 'Receive' and doc.custom_is_create_cheque:
        for row in doc.custom_cheques_table:
            cheque_doc = frappe.get_doc({
                'doctype': 'Receivable Cheque',
                'reference_date': doc.reference_date,
                'customer': doc.party,
                'posting_date': doc.posting_date,
                'company': doc.company,
                'against_account': doc.paid_to,
                'cheque_number': row.cheque_number,
                'due_date': row.cheque_due_date,
                'cheque_amount': row.cheque_amount,
                'customer_bank': row.against_bank
            })
            cheque_doc.insert()
        frappe.msgprint(_('Receivable Cheques have been created successfully.'))
def validate_cheque_fields(doc, method):
    # Check if the number of cheques or reference date or reference no has changed
    if (
        doc.meta.has_field("custom_number_of_cheques") and 
        doc.meta.has_field("reference_date") and 
        doc.meta.has_field("reference_no")
    ):
        if (
            doc.get_doc_before_save().custom_number_of_cheques != doc.custom_number_of_cheques or
            doc.get_doc_before_save().reference_date != doc.reference_date or
            doc.get_doc_before_save().reference_no != doc.reference_no
        ):
            add_cheque_rows(doc.name)

def add_cheque_rows(docname):
    doc = frappe.get_doc('Payment Entry', docname)
    number_of_cheques = doc.custom_number_of_cheques
    reference_date = doc.reference_date
    reference_no = int(doc.reference_no) if doc.reference_no else 0

    if not reference_date:
        frappe.throw(_('Please ensure the Reference Date field is filled.'))

    # Clear existing rows
    doc.custom_cheques_table = []
    
    for i in range(number_of_cheques):
        row = doc.append('custom_cheques_table')
        row.against_bank = doc.custom_customer_bank
        row.cheque_number = reference_no + i

    # Update cheque details (functionality should be defined elsewhere)
    update_cheque_details(doc)

    doc.save()