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
    select with the Browse… (Choose files) button.  ${filelist}`
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

    for (const file of files) {
        const ext = file.name.split('.').pop();
        file._ext = ext;  // save for later
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
        let filelist = ['<p>'];
        for (const name of unsavory) {
            filelist.push(`<i class="fa fa-file-code-o ml-4"></i> ${name}<br>`);
        }
        filelist.push('</p>');

        console.warn('upload:', render_err_unsavory(''));  // render w/o list
        show_err_dialog(render_err_unsavory(filelist.join('\n')));
    }
    return unsavory.length;
}


// ---------------------------------------------------------------------------
// traditional upload form

$('#files').change(check_unsavory_files)    // on file selection change
$('#upload_form').submit( (evt) => {   // on submit button
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

const FILE_SIZE_THRESHOLD = 1000000;  // 1 MB
const COMPLETION_DELAY = 1000;  // ms, for perception of work with tiny files.
const droptarget = $('#droptarget');
const progbar = $('progress#main');
const uplist = $('#uplist');


// rm a bit of implementation detail
droptarget.set_icon = function (name) {
    this.html('<i class="fa fa-' + name + '"></i>');
};
droptarget.show_busy  = function () { droptarget.set_icon('send'); };
droptarget.show_error = function () { this.set_icon('times-circle'); };
droptarget.show_ready = function () { this.set_icon('inbox'); };


function prog_handler(evt) {
    if (evt.lengthComputable) {
        console.debug(`upload progress: ${evt.loaded}/${evt.total}`);
        progbar.attr('value', evt.loaded);
        progbar.attr('max', evt.total);
    } else {
        console.debug('upload progress: not computable.');
    }
};


function err_handler(evt) {
    // err handler only fires on low-level network errors, not most http
    console.error('upload: ', err_network);
    droptarget.show_error();
    show_err_dialog(err_network);
};


function loadend_handler(evt) {     // upon completion or http error
    const req = evt.target;  // this?

    if (req.status == 200) {
        progbar.attr('max', 100);
        progbar.attr('value', 100);
        const msg = render_server_resp(req, 'status');
        console.log('upload end:', msg.replace('<br>', ''));

        // reset progress bar,
        setTimeout( () => {
            progbar.attr('value', 0);
            droptarget.set_icon('inbox');
        }, COMPLETION_DELAY);

    } else if (req.status == 0) {   // net error occurred, see err_handler.
        'no-op';
    } else {                        // http error occurred
        progbar.attr('max', 100);
        progbar.attr('value', 0);
        droptarget.show_error();
        const msg = render_server_resp(req, 'error');
        console.error('upload end:', msg);
        show_err_dialog(msg);
    }
};


// send small files at once as a form
function upload_files_form(location, formdata, numfiles) {
    return new Promise( (resolve, reject) => {

        console.debug(`upload form: sending ${numfiles}
                       small files as form to ${location}…`.replace(/\s+/g, ' '));
        // prepare request, jq slim build no tiene .ajax
        const req = new XMLHttpRequest();

        // note: add the event listeners before calling open
        req.upload.onprogress = prog_handler;   // .upload.
        req.upload.onerror = err_handler;
        req.upload.onabort = err_handler;
        req.onloadend = loadend_handler;        // not .upload.
        req.onload = resolve;                   // notify Promise
        req.onerror = reject;

        req.open('POST', location);
        // signal back-end to return json instead of full page:
        req.setRequestHeader('Accept', 'application/json');
        req.send(formdata);

    });
};


// send big files separately with a binary put
function upload_file(location, file) {
    return new Promise( (resolve, reject) => {

        console.debug(`upload put: sending large file '${file.name}'
                       to ${location}…`.replace(/\s+/g, ' '));
        // prepare request, jq slim build no tiene .ajax
        const req = new XMLHttpRequest();

        // add the event listeners before calling open
        req.upload.onprogress = prog_handler;   // note .upload.
        req.upload.onerror = err_handler;
        req.upload.onabort = err_handler;
        req.onloadend = loadend_handler;        // download
        req.onload = resolve;                   // notify Promise
        req.onerror = reject;

        req.open('PUT', location);
        // signal back-end to return json instead of full page:
        req.setRequestHeader('Accept', 'application/json');
        req.setRequestHeader('Content-Type', file.type);
        // 'Content-Length' is automatic and not allowed to be set.
        req.setRequestHeader('X-File-Name', file.name);
        req.send(file);
    });
};


// ---------------------------------------------------------------------------
// drag, drop handlers - could be moved

// execute uploads in sequence
async function exec_sequence(tasks) {
    console.debug('execute task sequence…');
    let count = 0;
    for (const task of tasks) {
        console.debug('starting task:', count);
        await task();  // create Promise and wait for it
        count++;
    }
}


function drag_end_handler(evt) {
    evt.preventDefault();
    console.debug('drag: end/exit/leave');
    droptarget.removeClass('hover');
};


droptarget.on({
    dragend: drag_end_handler,
    dragexit: drag_end_handler,
    dragleave: drag_end_handler,
    dragenter: (evt) => {
        evt.preventDefault();
        console.debug('drag: enter');
        droptarget.addClass('hover');
    },
    dragover: (evt) => {
        evt.preventDefault();  // yes, this is needed.
    },

    drop: (evt) => {
        evt.preventDefault();
        console.log('drop: occurred');
        uplist.empty();
        droptarget.removeClass('hover');

        // what did we get?
        const files = evt.originalEvent.dataTransfer.files;
        if (files.length) {

            // check types first
            if (check_unsavory_files(null, files)) {
                // this is the second error msg delivered, needs refr.
                console.error('upload submit: unsupported files, skipped.');
                return
            }

            // check sizes second
            const small_files = [], large_files = [], tasks = [];
            let total_size = 0;

            for (const file of files) {
                total_size += file.size
                // sort
                if (file.size > FILE_SIZE_THRESHOLD) {
                    large_files.push(file);
                } else {
                    small_files.push(file);
                }
                //~ <li><progress id=f10 class=file value=25 max=100></progress>
                    //~ <i class="fa fa-file-o"></i> Maracuja
                //~ </li><progress id=f10 class=file value=0
                                    //~ max=100></progress>
                uplist.append(`<li id=f00>
                               <i id=stat class="fa fa-hourglass-half mr-2"
                                   ></i>
                               <i class="fa fa-file-o"></i>
                               ${file.name}</li>`);
            }

            console.debug('upload: total file size:',
                           loc.format(total_size), 'bytes');
            if (total_size > MAX_CONTENT_LENGTH) {
                const msg = render_err_maxsize(loc, total_size);
                console.error('upload:', msg);
                uplist.empty();
                show_err_dialog(msg);
                return
            }

            // prepare and get started
            droptarget.show_busy();
            if (small_files.length) {
                const fdata = new FormData();
                for (const file of small_files) {
                    fdata.append('files[]', file, file.name);
                }
                tasks.push( () =>  // defers
                    upload_files_form(window.location.pathname, fdata,
                                      small_files.length)
                );
            }
            // send each lg file separately
            for (const file of large_files) {
                tasks.push( () =>  // defers
                    upload_file(window.location.pathname, file)
                );
            }
            exec_sequence(tasks);  // do async uploads in order :-P

        } else {
            console.error('upload:', err_nofiles);
            show_err_dialog(err_nofiles);
        }
    },
});

