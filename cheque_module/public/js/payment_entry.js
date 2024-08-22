frappe.ui.form.on('Payment Entry', {
    custom_number_of_cheques: function(frm) {
        if (frm.doc.custom_number_of_cheques) {
            add_cheque_rows(frm);
            update_cheque_amount(frm);
        }
    },
    reference_date: function(frm) {
        if (frm.doc.custom_number_of_cheques) {
            update_cheque_details(frm);
        }
    },
    custom_plane_term: function(frm) {
        if (frm.doc.custom_number_of_cheques) {
            update_cheque_details(frm);
        }
    },
    custom_customer_bank: function(frm) {
        if (frm.doc.custom_number_of_cheques) {
            update_cheque_details(frm);
        }
    },
    reference_no: function(frm) {
        if (frm.doc.custom_number_of_cheques) {
            update_cheque_details(frm);
        }
    },
    paid_amount: function(frm) {
        update_cheque_amount(frm);
        validate_total_cheques_amount(frm);
    },
    custom_is_equal: function(frm) {
        update_cheque_amount(frm);
        validate_total_cheques_amount(frm);
    },
    'custom_cheques_table.cheque_amount': function(frm, cdt, cdn) {
        update_total_cheques_amount(frm);
        validate_total_cheques_amount(frm);
    },
    before_save: function(frm) {
        validate_total_cheques_amount(frm);
    },
    before_submit: function(frm) {
        create_receivable_cheques(frm);
        create_payaple_cheques(frm);
    }
});

function add_cheque_rows(frm) {
    const numberOfCheques = frm.doc.custom_number_of_cheques;
    const customerBank = frm.doc.custom_customer_bank;
    const referenceDate = frm.doc.reference_date;
    const referenceNo = parseInt(frm.doc.reference_no, 10) || 0;

    if (!referenceDate) {
        frappe.msgprint(__('Please ensure the Reference Date field is filled.'));
        return;
    }

    frm.clear_table('custom_cheques_table');

    for (let i = 0; i < numberOfCheques; i++) {
        let child = frm.add_child('custom_cheques_table');
        child.against_bank = customerBank;
        child.cheque_number = referenceNo + i;  // Set the cheque_number based on reference_no and increment
    }

    update_cheque_details(frm);
    frm.refresh_field('custom_cheques_table');
}

function update_cheque_details(frm) {
    const referenceDate = frm.doc.reference_date;
    const customerBank = frm.doc.custom_customer_bank;
    const referenceNo = parseInt(frm.doc.reference_no, 10) || 0;
    const planeTerm = frm.doc.custom_plane_term;

    if (!referenceDate) {
        frappe.msgprint(__('Please ensure the Reference Date field is filled.'));
        return;
    }

    frm.doc.custom_cheques_table.forEach((row, index) => {
        let dueDate = new Date(referenceDate);

        if (planeTerm !== 'Blank') {
            switch (planeTerm) {
                case 'Monthly':
                    dueDate.setMonth(dueDate.getMonth() + index);
                    break;
                case 'Quarterly':
                    dueDate.setMonth(dueDate.getMonth() + 3 * index);
                    break;
                case 'Semiannually':
                    dueDate.setMonth(dueDate.getMonth() + 6 * index);
                    break;
                case 'Annually':
                    dueDate.setFullYear(dueDate.getFullYear() + index);
                    break;
            }
        }

        row.cheque_due_date = frappe.datetime.obj_to_str(dueDate);  // Ensure this matches your Frappe version
        row.against_bank = customerBank;
        row.cheque_number = referenceNo + index;  // Update cheque_number based on reference_no and increment
    });

    frm.refresh_field('custom_cheques_table');
}

function update_cheque_amount(frm) {
    const paidAmount = frm.doc.paid_amount || 0;
    const numberOfCheques = frm.doc.custom_number_of_cheques || 1; // Default to 1 to avoid division by zero
    const isEqual = frm.doc.custom_is_equal || false;
    
    if (isEqual) {
        const chequeAmount = paidAmount / numberOfCheques;
        frm.doc.custom_cheques_table.forEach(row => {
            row.cheque_amount = chequeAmount;
        });
    } else {
        frm.doc.custom_cheques_table.forEach(row => {
            row.cheque_amount = paidAmount;
        });
    }

    frm.refresh_field('custom_cheques_table'); // Ensure field refresh
    update_total_cheques_amount(frm);  // Update the total amount after setting cheque amounts
}

function update_total_cheques_amount(frm) {
    const totalChequeAmount = frm.doc.custom_cheques_table.reduce((total, row) => total + (row.cheque_amount || 0), 0);
    cur_frm.set_value('custom_total_cheques_amount', totalChequeAmount); // Use cur_frm for consistency
    cur_frm.refresh_field('custom_total_cheques_amount');
}

function validate_total_cheques_amount(frm) {
    const paidAmount = frm.doc.paid_amount || 0;
    const totalChequeAmount = frm.doc.custom_total_cheques_amount || 0;

    if (frm.doc.custom_is_create_cheque === 1 && totalChequeAmount !== paidAmount) {
        frappe.msgprint(__('The total cheque amount does not match the paid amount. Please review your entries.'));
        frappe.validated = false;
    }
}

async function create_receivable_cheques(frm) {
    if (frm.doc.payment_type === 'Receive' && frm.doc.custom_is_create_cheque === 1) {
        try {
            const promises = frm.doc.custom_cheques_table.map(row =>
                frappe.call({
                    method: 'frappe.client.insert',
                    args: {
                        doc: {
                            doctype: 'Receivable Cheque',
                            reference_date: frm.doc.reference_date,
                            customer: frm.doc.party,
                            posting_date: frm.doc.posting_date,
                            company: frm.doc.company,
                            against_account: frm.doc.paid_to,
                            cheque_image: row.cheque_image,
                            cheque_number: row.cheque_number,
                            due_date: row.cheque_due_date,
                            cheque_amount: row.cheque_amount,
                            customer_bank: row.against_bank,
                            attach_cheque_image: row.attach_image,
                            from_payment_entry: frm.doc.name // Reference to the Payment Entry
                        }
                    }
                })
            );

            await Promise.all(promises);
            frappe.msgprint(__('Receivable Cheques have been created successfully.'));
        } catch (error) {
            console.error(error);
            frappe.msgprint(__('An error occurred while creating Receivable Cheques.'));
            frappe.validated = false;
        }
    }
}

async function create_payaple_cheques(frm) {
    if (frm.doc.payment_type === 'Pay' && frm.doc.custom_is_create_cheque === 1) {
        try {
            const promises = frm.doc.custom_cheques_table.map(row =>
                frappe.call({
                    method: 'frappe.client.insert',
                    args: {
                        doc: {
                            doctype: 'Payaple Cheque',
                            cheque_due_date: frm.doc.reference_date,
                            party: frm.doc.party,
                            party_name: frm.doc.party_name,
                            cheque_posting_date: frm.doc.posting_date,
                            company: frm.doc.company,
                            against_account: frm.doc.paid_from,
                            attach_image_bhtz: row.cheque_image,
                            cheque_number: row.cheque_number,
                            cheque_due_date: row.cheque_due_date,
                            amount: row.cheque_amount,
                            bank: row.against_bank,
                            attach_image_bhtz: row.attach_image,
                            from_payment_entry: frm.doc.name,
                            bank_account: frm.doc.bank_account // Reference to the Payment Entry
                        }
                    }
                })
            );

            await Promise.all(promises);
            frappe.msgprint(__('Receivable Cheques have been created successfully.'));
        } catch (error) {
            console.error(error);
            frappe.msgprint(__('An error occurred while creating Receivable Cheques.'));
            frappe.validated = false;
        }
    }
}