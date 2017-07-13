//
// javascript handling drag, drop, and file uploading goes here.
//
// TODO:  copy big binary files piece by piece w/o formData
//
'use strict';

// Create a number formatter
const locale = 'en-US';  // mv to template
const loc = new Intl.NumberFormat(locale);

// deferred string templates for error messages, utilizing arrow functions.
const render_err_maxsize = (loc, total_size) =>
    `The upload submission size (${loc.format(total_size)} bytes) is greater
    than the maximum limit of ${loc.format(MAX_CONTENT_LENGTH)} bytes—skipping
    submission.
    <p>Kindly try again with a smaller file set.`
    .replace(/\s+/g, ' ');  // normalizes string for console log
const render_err_unsavory = (filelist) =>
    `Unsupported file types were selected. Kindly drop another set of files or
    select with the Browse… (Choose files) button. ${filelist}`
    .replace(/\s+/g, ' ');
const render_err_zerofiles = () =>
    `No files were selected.  Kindly choose a file with the Browse…
     (Choose files) button and try again.`.replace(/\s+/g, ' ');
const render_server_resp = (req, type) =>
    `The server responded with the ${type} message:<br>
     ${req.status} ${req.statusText}`.replace(/\s+/g, ' ');
const err_network =
    'A low-level network error occurred, or the connection was reset.';
const err_nofiles = 'No files found in drop action.  Please try again.';

const rmtags = (text) => text.replace(/(<([^>]+)>)/ig, '');  // html cleaner


// prevent known-skeezy file types from entering our upload list
function check_unsavory_files(evt, files) {
    if (typeof(files) === 'undefined') {    // handle event or a direct call.
        files = evt.target.files;           // FileList object
    }
    const unsavory = [];                    // props still mutable

    for (let file of files) {
        const ext = file.name.split('.').pop();
        if (DEBUG) {
            console.debug(`check_files: ${file.name}, ${file.type}, size:
               ${loc.format(file.size)}  ext: ${ext}`.replace(/\s+/g, ' '));
        }
        if (unsavory_exts.has(ext)) {
            console.warn('    Unsupported file found: ' + file.name);
            unsavory.push(file.name);
        }
    }

    // TODO: dialog building should be broken out to own function.
    if (unsavory.length) {
        let filelist = '<p>\n';                 // build text list
        for (let name of unsavory) {
            filelist += '<i class="fa fa-file-code-o"></i> ' + name + '<br>\n'
        }
        filelist += '</p>\n'

        console.warn('upload:', render_err_unsavory(''));  // render w/o list
        show_err_dialog(render_err_unsavory(filelist));
    }
    return unsavory.length;
}


// ---------------------------------------------------------------------------
// traditional upload form

$('#files').change(check_unsavory_files)    // on file selection change
$('#upload_form').submit(function (evt) {   // on submit button
    const files = $('input#files')[0].files;

    if (files.length === 0) {
        const msg = render_err_zerofiles();
        console.error('upload on_submit:', msg);
        show_msg_dialog('exclamation-circle', 'Error:', msg);
        evt.preventDefault();

    } else if (check_unsavory_files(null, files)) {
        console.error('upload on_submit: unsupported files, skipped.');
        evt.preventDefault();
    }
});


// ---------------------------------------------------------------------------
// ajax upload

const completion_delay = 1200;  // ms

function prog_handler(evt) {
    console.debug(`upload progress: ${evt.loaded}/${evt.total}`);
    $('#progress').attr('value', evt.loaded);
    $('#progress').attr('max', evt.total);
};

function err_handler(evt) {
    // err handler only fires on low-level network errors, not most http
    $('#droptarget').html('<i class="fa fa-times-circle"></i>');
    console.error('upload: ', err_network);
    show_err_dialog(err_network);
};

function loadend_handler(evt) {     // upon completion or http error
    let req = evt.target;
    let pb = $('#progress');

    if (req.status == 200) {
        pb.attr('max', 100);
        pb.attr('value', 100);
        $('#droptarget').html('<i class="fa fa-cloud-upload"></i>');
        const msg = render_server_resp(req, 'status');
        console.log('upload end:', msg.replace('<br>', ''));

        // reset progress bar, delay for perception of work with tiny files.
        setTimeout(function () {
            $('#progress').attr('value', 0);
        }, completion_delay);

    } else if (req.status == 0) {   // net error occurred, see err_handler.
        'no-op';
    } else {                        // http error occurred
        pb.attr('max', 100);
        pb.attr('value', 0);
        $('#droptarget').html('<i class="fa fa-times-circle"></i>');
        const msg = render_server_resp(req, 'error');
        console.error('upload end:', msg);
        show_err_dialog(msg);
    }
};

function upload_files(location, formdata) {
    // prepare request, jq slim build no tiene .ajax
    console.log(`upload: to ${location} starting…`);
    let req = new XMLHttpRequest();

    // note: add the event listeners before calling open
    req.onprogress = prog_handler;
    req.onerror = err_handler;
    req.onabort = err_handler;
    req.onloadend = loadend_handler;

    req.open('POST', location);
    // signal back-end to return json instead of full page:
    req.setRequestHeader('Accept', 'application/json');
    req.send(formdata);
}


// ---------------------------------------------------------------------------
// drag, drop handlers - could be moved

function drag_end_handler(evt) {
    evt.preventDefault();
    console.debug('drag: end/exit/leave');
    $('#droptarget').removeClass('hover');
};

$('#droptarget').on({
    dragend: drag_end_handler,
    dragexit: drag_end_handler,
    dragleave: drag_end_handler,

    dragenter:
        function (evt) {
            evt.preventDefault();
            console.debug('drag: enter');
            $('#droptarget').addClass('hover');
        },

    dragover:
        function (evt) {
            evt.preventDefault();  // yes, this is needed.
        },

    drop:
        function (evt) {
            evt.preventDefault();
            console.log('drop: occurred');
            $('#droptarget').removeClass('hover');

            // what did we get?
            const files = evt.originalEvent.dataTransfer.files;
            if (files.length) {

                if (check_unsavory_files(null, files)) {
                    // this is the second error msg delivered, needs refr.
                    console.error('upload submit: unsupported files, skipped.');
                    return
                }

                // check sizes first
                let total_size = 0;
                for (let file of files) {
                    total_size += file.size
                }
                console.debug('upload: total file size:',
                               loc.format(total_size), 'bytes');
                if (total_size > MAX_CONTENT_LENGTH) {
                    const msg = render_err_maxsize(loc, total_size);
                    console.error('upload:', msg);
                    show_err_dialog(msg);
                    return
                }

                // add to form, b64 may cause slowdown
                const fdata = new FormData();
                for (let file of files) {
                    fdata.append('files[]', file, file.name);
                }
                upload_files(window.location.pathname, fdata);
            } else {
                console.error('upload:', err_nofiles);
                show_err_dialog(err_nofiles);
            }
        },
});

