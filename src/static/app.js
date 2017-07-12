// Common app-wide js goes here.
'use strict';


// code for generic empty tab-modal message dialog.
function show_msg_dialog(icon, title, body) {
    $('#msg_dialog .modal-title').html(
                                    `<i class="fa fa-${icon}"></i> ${title}`);
    $('#msg_dialog .modal-body').html(`<p>${body}`);
    $('#msg_dialog').modal('show');
}








