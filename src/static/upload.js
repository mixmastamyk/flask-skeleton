'use strict';

function check_unsavory_files(evt, files) {
    if (typeof(files) === 'undefined') {    // handle event and direct call.
        files = evt.target.files;           // FileList object
    }
    const unsavory = [];                    // props mutable

    for (let file of files) {
        const ext = file.name.split('.').pop();
        console.debug(`check_files: ${file.name}, ${file.type}, ext: ${ext}`)
        if (unsavory_exts.has(ext)) {
            console.warn('    Unsupported file found: ' + file.name);
            unsavory.push(file.name)
        }
    }

    // dialog building should be broken out to own function.
    if (unsavory.length) {
        let text = '<p>\n';                 // build text list
        for (let name of unsavory) {
            text += '<i class="fa fa-file-code-o"></i> ' + name + '<br>\n'
        }
        text += '</p>\n'
        show_msg_dialog('exclamation-triangle', 'Warning:',
            `<p>Unsupported file types were selected.
             Kindly drop another set of files or select with the Browse
             button.</p>
            ${text}`
        )
    }
    return unsavory.length;
}


// ---------------------------------------------------------------------------
// traditional upload form

$('#files').change(check_unsavory_files)    // on file selection change
$('#upload_form').submit(function (evt) {     // on submit button
    const files = $('#files')[0].files;
    evt.preventDefault();

    if (files.length === 0) {
        console.error('upload on_submit: No files were selected.');
        show_msg_dialog('exclamation-circle', 'Error:',
            `No files were selected.  Kindly choose a file with the Browse…
             button and try again.`)

    } else if (check_unsavory_files(null, files)) {
        console.error('upload on_submit: unsupported files, skipped.');
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
    console.error(`upload: network error.`);
    show_msg_dialog('exclamation-circle', 'Error:',
        `A low-level network error occurred, or the connection was reset.`);
};

function loadend_handler(evt) {     // upon completion or http error
    let req = evt.target;
    let pb = $('#progress');
    pb.attr('max', 100);

    if (req.status == 200) {
        pb.attr('value', 100);
        $('#droptarget').html('<i class="fa fa-cloud-upload"></i>');
        console.log(`upload end: server response: ${req.status} ${req.statusText}`);

        // reset progress bar, delay for perception of work with tiny files.
        setTimeout(function () {
            $('#progress').attr('value', 0);
        }, completion_delay);

    } else if (req.status == 0) {   // net error occurred, see err_handler.
        'no-op';
    } else {                        // http error occurred
        pb.attr('value', 0);
        $('#droptarget').html('<i class="fa fa-times-circle"></i>');
        console.error(`upload end: server response: ${req.status} ${req.statusText}`);
        show_msg_dialog('exclamation-circle', 'Error:',
            `The server responded with the error message:<br>
            ${req.status} ${req.statusText}`);
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
                    console.error('upload on_submit: unsupported files, skipped.');
                    return
                }

                // add to form, b64 may cause slowdown
                const fdata = new FormData();
                for (let f of files) {
                    fdata.append('files[]', f, f.name);
                }
                upload_files(window.location.pathname, fdata);
            } else {
                const msg =
                    'No files found in drop action.  Please try again.';
                console.error(msg);
                show_msg_dialog('exclamation-circle', 'Error:', msg);
            }
        },
});

