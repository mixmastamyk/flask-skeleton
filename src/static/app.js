// Common app-wide js goes here.
//
/* eslint no-unused-vars: ['error', {vars: 'local'}] */
'use strict';
const MILLI = 1000;


// support for bootstrap modal message dialogs
function show_msg_dialog(icon, title, body) {
    $('#msg_dialog .modal-title').html(
        `<i class="fa fa-${icon}"></i> ${title}`);
    $('#msg_dialog .modal-body').html(`<p>${body}`);
    $('#msg_dialog').modal('show');
}


function show_err_dialog(body) {
    console.debug('show_err_dialog called.');
    show_msg_dialog('exclamation-circle', 'Error:', body);
}


function show_warn_dialog(body) {
    console.debug('show_warn_dialog called.');
    show_msg_dialog('exclamation-triangle', 'Warning:', body);
}


// can js do that?  Apparently so: https://stackoverflow.com/a/39914235/450917
function sleep(msecs) {
    console.debug('sleeping for', msecs / MILLI, 'secs…');
    return new Promise(resolve => setTimeout(resolve, msecs));
}

