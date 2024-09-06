frappe.ui.form.on('Payaple Cheque', {
    refresh: function(frm) {
        // Create a dropdown button labeled 'Actions'
        frm.add_custom_button('Actions', null, 'Actions');

        // Add the 'Move to Bank' action with a popup
        // frm.page.add_action_item('Move to Bank', () => {
        //     frappe.prompt([
        //         {
        //             fieldname: 'bank',
        //             label: 'Bank',
        //             fieldtype: 'Link',
        //             options: 'Bank',
        //             reqd: 1,
        //             onchange: function(value) {
        //                 // Set up a dynamic filter for the Bank Account field based on the selected Bank
        //                 let bank = value;
        //                 frappe.ui.form.make_control({
        //                     parent: this.fields_dict.bank_account.$wrapper,
        //                     df: {
        //                         fieldname: 'bank_account',
        //                         label: 'Bank Account',
        //                         fieldtype: 'Link',
        //                         options: 'Bank Account',
        //                         reqd: 1,
        //                         get_query: function() {
        //                             return { filters: { bank: bank } };
        //                         }
        //                     }
        //                 }).refresh();
        //             }
        //         },
        //         {
        //             fieldname: 'bank_account',
        //             label: 'Bank Account',
        //             fieldtype: 'Link',
        //             options: 'Bank Account',
        //             reqd: 1
        //         }
        //     ], function(values) {
        //         // Update the fields with the selected values
        //         frm.set_value('store_in_bank', values.bank);
        //         frm.set_value('store_in_bank_account', values.bank_account);
        //         frm.set_value('location', 'Bank');
        //         frm.set_value('move_to_bank_date', frappe.datetime.nowdate());

        //         // Check if the document is submitted (docstatus == 1)
        //         if (frm.doc.docstatus === 1) {
        //             // Submit the document
        //             frappe.call({
        //                 method: 'frappe.client.submit',
        //                 args: { doc: frm.doc },
        //                 callback: function(response) {
        //                     frappe.msgprint(__('Store in Bank and Bank Account updated successfully.'));
        //                     frm.reload_doc();
        //                 }
        //             });
        //         } else {
        //             // Save the document if it's in draft mode
        //             frm.save().then(() => {
        //                 frappe.msgprint(__('Store in Bank and Bank Account updated successfully.'));
        //             });
        //         }
        //     }, 'Move to Bank', 'Submit');
        // });

        // Navigate to a new Payment Entry record for 'Collect Cash' with field mappings
        frm.page.add_action_item('Pay Cash', () => {
            let payment_entry = frappe.model.get_new_doc('Payment Entry');
            payment_entry.naming_series = 'ACC-PAY-.YYYY.-';
            payment_entry.posting_date = frappe.datetime.nowdate();
            // payment_entry.mode_of_payment = frm.doc.source_mode_of_payment;
            payment_entry.payment_type = 'Internal Transfer'; // Corrected the payment type
            payment_entry.paid_to = frm.doc.against_account;
            // payment_entry.paid_to = frm.doc.bank_company_account;
            payment_entry.paid_amount = frm.doc.amount;
            payment_entry.received_amount = frm.doc.amount; // Adjust this mapping as needed
            payment_entry.reference_no = frm.doc.cheque_number;
            payment_entry.reference_date = frm.doc.cheque_due_date; // Adjust this mapping as needed
            payment_entry.company = frm.doc.company; // Adjust this mapping as needed
            frappe.set_route('form', 'Payment Entry', payment_entry.name);
            payment_entry.custom_cheque_type = 'Payaple Cheque';
            payment_entry.custom_cheque_link = frm.doc.name;
            payment_entry.custom_action_taken = 'Pay Cash';
            payment_entry.custom_status_before_action = frm.doc.status;
            
        });

        // Navigate to a new Payment Entry record for 'Collect Bank' with field mappings
        frm.page.add_action_item('Pay Bank', () => {
            let payment_entry = frappe.model.get_new_doc('Payment Entry');
            payment_entry.naming_series = 'ACC-PAY-.YYYY.-';
            payment_entry.posting_date = frappe.datetime.nowdate();
            // payment_entry.mode_of_payment = frm.doc.source_mode_of_payment;
            payment_entry.payment_type = 'Internal Transfer'; // Corrected the payment type
            payment_entry.paid_to = frm.doc.against_account;
            payment_entry.paid_from = frm.doc.default_bank_collected_account;
            payment_entry.paid_amount = frm.doc.amount;
            payment_entry.received_amount = frm.doc.amount; // Adjust this mapping as needed
            payment_entry.reference_no = frm.doc.cheque_number;
            payment_entry.reference_date = frm.doc.cheque_due_date; // Adjust this mapping as needed
            payment_entry.company = frm.doc.company; // Adjust this mapping as needed
            frappe.set_route('form', 'Payment Entry', payment_entry.name);
            payment_entry.custom_cheque_type = 'Payaple Cheque';
            payment_entry.custom_cheque_link = frm.doc.name;
            payment_entry.custom_action_taken = 'Pay Bank';
            payment_entry.custom_status_before_action = frm.doc.status;

        });

        // Other action items
        // frm.page.add_action_item('Bounce', () => {
        //     let payment_entry = frappe.model.get_new_doc('Payment Entry');
        //     payment_entry.naming_series = 'ACC-PAY-.YYYY.-';
        //     payment_entry.posting_date = frappe.datetime.nowdate();
        //     payment_entry.mode_of_payment = frm.doc.source_mode_of_payment;
        //     payment_entry.payment_type = 'Internal Transfer'; // Corrected the payment type
        //     payment_entry.paid_from = frm.doc.against_account;
        //     // payment_entry.paid_to = frm.doc.bank_company_account;
        //     payment_entry.paid_amount = frm.doc.cheque_amount;
        //     payment_entry.received_amount = frm.doc.cheque_amount; // Adjust this mapping as needed
        //     payment_entry.reference_no = frm.doc.cheque_number;
        //     payment_entry.reference_date = frm.doc.due_date; // Adjust this mapping as needed
        //     payment_entry.company = frm.doc.company; // Adjust this mapping as needed
        //     frappe.set_route('form', 'Payment Entry', payment_entry.name);
        //     frappe.msgprint(__('Bounce action executed')); // Add your custom logic here
        // });

        // frm.page.add_action_item('Cancel', () => {
        //     frappe.msgprint(__('Cancel action executed')); // Add your custom logic here
        // });

        // frm.page.add_action_item('Delivered to Customer', () => {
        //     frappe.msgprint(__('Delivered to Customer action executed')); // Add your custom logic here
        // });
    }
});

