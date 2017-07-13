// Common app-wide js goes here.
'use strict';


// support for bootstrap modal message dialogs
function show_msg_dialog(icon, title, body) {
    $('#msg_dialog .modal-title').html(
                                    `<i class="fa fa-${icon}"></i> ${title}`);
    $('#msg_dialog .modal-body').html(`<p>${body}`);
    $('#msg_dialog').modal('show');
}

function show_warn_dialog(body) {
    show_msg_dialog('exclamation-triangle', 'Warning:', body);
}

function show_err_dialog(body) {
    show_msg_dialog('exclamation-circle', 'Error:', body);
}


