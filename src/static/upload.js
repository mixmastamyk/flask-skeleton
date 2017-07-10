'use strict';

function check_unsavory_files(evt, files) {
    if (typeof(files) === 'undefined') {  // handle event and direct call.
        files = evt.target.files;         // FileList object
    }
    const unsavory = [];                  // props mutable

    for (let file of files) {
        const ext = file.name.split('.').pop();
        console.debug(`check_files: ${file.name}, ${file.type}, ext: ${ext}`)
        if (unsavory_exts.has(ext)) {
            console.warn('    Unsupported file found: ' + file.name);
            unsavory.push(file.name)
        }
    }

    if (unsavory.length) {
        let text = '<p>\n';               // build text list
        for (let name of unsavory) {
            text += '<i class="fa fa-file-code-o"></i> ' + name + '<br>\n'
        }
        text += '</p>\n'
        show_msg_dialog('exclamation-triangle', 'Warning:',
            `<p>Unsupported file types were selected.
             Kindly choose another set of files with the Browse button.</p>
            ${text}`
        )
    }
    return unsavory.length;
}

// traditional upload form
$('#files').change(check_unsavory_files)    // on file selection change
$('#upload_form').submit(function (e) {     // on submit button
    const files = $('#files')[0].files;

    if (files.length === 0) {
        console.error('upload on_submit: No files were selected.');
        show_msg_dialog('exclamation-circle', 'Error:',
            `No files were selected.  Kindly choose a file with the Browse…
             button and try again.`)
        e.preventDefault();

    } else if (check_unsavory_files(null, files)) {
        console.error('upload on_submit: unsupported files, skipped.');
        e.preventDefault();
    }
});

// ajax upload
const completion_delay = 1200;

function comp_handler(evt) {   // on completion
    console.log('upload: complete');
    setTimeout(function () {
        $('#progress').attr('value', 0);
        $('#droptarget').removeClass('hover');
    }, completion_delay);
};

function prog_handler(evt) {
    console.log(`upload progress: ${evt.loaded}/${evt.total}`);
    $('#progress').attr('value', evt.loaded);
    $('#progress').attr('max', evt.total);
};
// if looping
//~ // https://stackoverflow.com/a/12713090/450917
//~ let progid = 'progress';
//~ (function (id) {
    //~ const progid = '#' + id;
    //~ req.upload.onprogress = function (e) {
        //~ console.log(`upload progress: ${e.loaded}/${e.total}`);
        //~ $(progid).attr('value', e.loaded);
        //~ $(progid).attr('max', e.total);
    //~ };
//~ }(progid));

function load_handler(evt) {
    evt.preventDefault();
    //~ console.error('upload: loadend ' + evt.detail);
    //~ console.dir(evt);  // didn't find any good information
    //~ $('#progress').attr('value', 0);
    //~ $('#droptarget').html('<i class="fa fa-times-circle"></i>');
    //~ $('#droptarget').removeClass('hover');
};

function err_handler(evt) {
    console.error('upload: ' + evt.detail);
    evt.preventDefault();
    console.dir(evt);  // didn't find any good information
    $('#droptarget').html('<i class="fa fa-times-circle"></i>');
    $('#droptarget').removeClass('hover');
};

function upload_files(location, formdata, comp_handler, prog_handler,
                                          load_handler, err_handler) {
    // prepare request, jq slim build no tiene .ajax
    console.log('upload: starting...');
    let req = new XMLHttpRequest();

    // note: add the event listeners before calling open
    req.upload.onload = comp_handler;
    req.upload.onloadend = load_handler;
    req.upload.onprogress = prog_handler;
    req.upload.onerror = err_handler;

    req.open('POST', location);
    req.send(formdata);
}

// drag, drop handlers
function drag_end_handler(evt) {
    evt.preventDefault();
    console.debug('drag: end/exit');
    $('#droptarget').removeClass('hover');
};

$('#droptarget').on({
    dragend: drag_end_handler,
    dragexit: drag_end_handler,
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

            // what did we get?
            const files = evt.originalEvent.dataTransfer.files;
            if (files.length) {

                // add to form
                const fdata = new FormData();
                for (let f of files) {
                    fdata.append('files[]', f, f.name);
                }
                upload_files(window.location.pathname, fdata, comp_handler,
                             prog_handler, load_handler, err_handler);

            } else {
                $('#droptarget').removeClass('hover');
                const msg =
                    'No files found in drop action.  Please try again.';
                console.error(msg);
                show_msg_dialog('exclamation-circle', 'Error:', msg);
                return;
            }

        },
});

