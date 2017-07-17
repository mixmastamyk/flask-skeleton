//
// javascript handling drag, drop, and file uploading goes here.
//
// TODO: make droptarget icon not interfere in drag
// TODO: Make another drop impossible during upload
// TODO: check unsavory to have one argument with type checking
'use strict';

const loc = new Intl.NumberFormat(LOCALE);  // localize big numbers

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
    `The server responded with the ${type} message:
     <p>${req.status} ${req.statusText}`.replace(/\s+/g, ' ');
const err_network =
    'A low-level network error occurred, or the connection was reset.';
const err_nofiles = 'No files found in drop action.  Please try again.';

const rmtags = (text) => text.replace(/(<([^>]+)>)/ig, '');  // html cleaner


// ---------------------------------------------------------------------------
// view implementation details

const droptarget = $('#droptarget');
const progbar = $('progress#main');
const quantity = $('#quantity');
const uplist = $('#uplist');
const icon_map = {
    'application/pdf': 'file-pdf-o',
    'application/zip': 'file-zip-o',
    'text/css': 'file-code-o',
    'text/html': 'file-code-o',
    'text/xml': 'file-code-o',
};


// add an upload item to the list for each file in the manifest
function add_to_uplist(manifest) {
    for (const file of manifest) {
        uplist.append(`
            <li id=f00>
                <div class="d-flex">
                    <div class="icons">
                        <i class="stat fa fa-spinner fa-spin pr-1"></i>
                        <i class="fa fa-${icon_from_type(file.type)}"></i>
                    </div>
                    <div class="pl-1">${file.name}</div>
                </div>
            </li>`);
    }
    scroll_it_down(uplist);  // once at end
};


// convert a file's mime-type into a "fa" icon
function icon_from_type(mimetype) {
    let icon = icon_map[mimetype];                       // first attempt
    if (!icon) {
        const type = mimetype.split('/', 1)[0];         //  "type/subtype"
        switch(type) {
            case 'audio':
            case 'image':
            case 'text':
            case 'video':
                icon = `file-${type}-o`;
                break;
            case 'application':
                icon = 'file-code-o';
                break;
            default:
                icon = 'file-o';
        };
    };
    return icon
};
// set icons for the drop target
droptarget.set_icon = function (name) {
    this.html(`<i class="fa fa-${name}"></i>`);
};
droptarget.show_busy  = function () { this.set_icon('send'); };
droptarget.show_error = function () { this.set_icon('times-circle'); };
droptarget.show_ready = function () { this.set_icon('inbox'); };


// set icons for the upload list items
function set_uplist_icons(icons, name) {
    icons.addClass('fa-' + name).removeClass('fa-spin fa-spinner');
}


// form submission - change all existing icons to success or failure
function show_results(success) {
    const icons = $('#uplist i.stat');
    if (success) {
        set_uplist_icons(icons, 'check');
    } else {
        set_uplist_icons(icons, 'times');
    };
}


// put instructions - change the last icon only
function show_single_result(success) {
    const icon = $('#uplist li:last-child i.stat');     // note last-child
    if (success) {
        set_uplist_icons(icon, 'check');
    } else {
        set_uplist_icons(icon, 'times');
    };
}


// warn/error when unsupported files found
function show_unsavory_dialog(unsavory, mode='warn') {
    const filelist = ['<p>'];
    for (const name of unsavory) {
        filelist.push(`<i class="fa fa-file-code-o ml-4"></i> ${name}<br>`);
    }

    const logmsg = render_err_unsavory(''),     // w/o filelist
          msgbod = render_err_unsavory(filelist.join('\n'));
    if (mode === 'warn') {
        console.warn('upload:', logmsg);
        show_warn_dialog(msgbod);
    } else if (mode === 'error') {
        console.error('upload:', logmsg);
        show_err_dialog(msgbod);
    };
}


// scroll uplist down to the last item
function scroll_it_down(element) {  // watch out!  https://youtu.be/RZUq6N7Gx1c
    element.scrollTop(element.prop('scrollHeight'));
}


// prevent known-skeezy file types from entering our upload list
function check_unsavory_files(evt, files) {
    if (typeof(files) === 'undefined') {    // handle event or a direct call.
        files = evt.target.files;           // FileList object
    }
    const unsavory = [];

    for (const file of files) {
        const ext = file.name.split('.').pop();
        file._ext = ext;  // save extension for later
        if (DEBUG) {
            console.debug(`check_files: ${file.name}, ${file.type}, size:
               ${loc.format(file.size)}  ext: ${ext}`.replace(/\s+/g, ' '));
        }
        if (UPLOAD_UNSAVORY_EXTS.has(ext)) {  // from config, template
            console.warn('    Unsupported file found: ' + file.name);
            unsavory.push(file.name);
        }
    }
    return unsavory;
}


// ---------------------------------------------------------------------------
// traditional upload form

$('#files').change( (evt) => {     // on file selection change
    const unsavory = check_unsavory_files(evt);
    if (unsavory.length) {
        show_unsavory_dialog(unsavory);
    }
})
$('#upload_form').submit( (evt) => {        // on submit button
    const files = $('input#files')[0].files;

    if (files.length === 0) {
        const msg = render_err_zerofiles();
        console.error('upload on_submit:', msg);
        show_err_dialog(msg);
        evt.preventDefault();
        return
    }

    const unsavory = check_unsavory_files(null, files);
    if (unsavory.length) {
        show_unsavory_dialog(unsavory, 'error');
        evt.preventDefault();
    }
});


// ---------------------------------------------------------------------------
// ajax upload functions

const COMPLETION_DELAY = 2000;  // ms, for perception of work with tiny files.


function prog_handler(evt) {
    if (evt.lengthComputable) {
        console.debug(`upload progress: ${evt.loaded}/${evt.total}`);
        progbar.attr('value', evt.loaded);
        progbar.attr('max', evt.total);
    } else {
        console.debug('upload progress: not computable.');
    }
};


function start_handler(evt) {
    console.debug('upload: start…');
    progbar.attr('value', 0);
    progbar.attr('max', 100);
};


function err_handler(evt) {
    // err handler only fires on low-level network errors, not most http errs
    console.error('upload: ', err_network);
    droptarget.show_error();
    show_err_dialog(err_network);
};


function loadend_handler(evt) {     // upon completion or http error
    const req = evt.target;

    if (req.status >= 200 && req.status < 300) {
        const msg = render_server_resp(req, 'status');
        console.log('upload end:', rmtags(msg));
        req._show_results(true);

    } else if (req.status == 0) {       // net error occurred, see err_handler.
        'no-op';
    } else {                            // http error occurred
        progbar.attr('max', 100);
        progbar.attr('value', 0);
        droptarget.show_error();
        const msg = render_server_resp(req, 'error');
        console.error('upload end:', rmtags(msg));
        req._show_results();
        show_err_dialog(msg);
    }
};


// send small files at once as a form
function upload_files_form(location, formdata, numfiles) {
    return new Promise( (resolve, reject) => {

        console.debug(`upload form: sending ${numfiles} small files as form
                       to ${location}…`.replace(/\s+/g, ' '));
        // prepare request, jq slim build no tiene .ajax
        const req = new XMLHttpRequest();

        // note: add the event listeners before calling open
        req.upload.onabort = err_handler;       // .upload.
        req.upload.onerror = err_handler;
        req.upload.onloadstart = start_handler;
        req.upload.onprogress = prog_handler;
        req.onloadend = loadend_handler;        // download
        req.onload = resolve;                   // notify Promise
        req.onerror = reject;
        req._show_results = show_results;

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
        req.upload.onabort = err_handler;       // note .upload.
        req.upload.onerror = err_handler;
        req.upload.onloadstart = start_handler;
        req.upload.onprogress = prog_handler;
        req.onloadend = loadend_handler;        // download
        req.onload = resolve;                   // notify Promise
        req.onerror = reject;
        req._show_results = show_single_result;

        req.open('PUT', location);
        // signal back-end to return json instead of full page:
        req.setRequestHeader('Accept', 'application/json');
        req.setRequestHeader('Content-Type', file.type);
        // 'Content-Length' is automatic and not allowed to be set.
        req.setRequestHeader('X-File-Name', file.name);
        req.send(file);
    });
};


// Do async uploads in an orderly sequence :-P
async function execute_task_sequence(tasks) {
    console.debug('execute task sequence…');
    for (let [manifest, task] of tasks) {  // TODO let const

        add_to_uplist(manifest);
        if (DEBUG) { await sleep(COMPLETION_DELAY); }   // too darn fast :D
        await task();  // create Promise and wait for it to finish
        if (DEBUG) {
            await sleep(COMPLETION_DELAY);
            progbar.attr('value', 0);
            progbar.attr('max', 100);                   // looks better
        }
    }

    // reset after a delay, to give perception of work
    setTimeout( () => {
        progbar.attr('value', 0);
        droptarget.show_ready();
    }, COMPLETION_DELAY);
}


// ---------------------------------------------------------------------------
// drag, drop handlers

function drag_end_handler(evt) {
    evt.preventDefault();
    console.debug('drag: end/exit/leave');
    droptarget.removeClass('hover');
};


// prevent droppage on other parts of page breaking everything
$(document).on({
    dragover: (evt) => {
        evt.preventDefault();  // yes, this is needed.
    },
    drop: (evt) => {
        evt.preventDefault();
        const msg = `Sorry, you missed the drop box, try again.
                     Look for the box to the top left labeled "Drop Box."
                     <i class="fa fa-smile-o"></i>`.replace(/\s+/g, ' ');
        console.warn('drop: missed target.');
        show_warn_dialog(msg);
    }
});


// configure the drop target
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
        evt.stopPropagation();  // prevents interference from document handler
        console.log('drop: occurred');
        uplist.empty();
        quantity.empty();
        droptarget.removeClass('hover');

        // what did we get?
        const files = evt.originalEvent.dataTransfer.files;
        console.log(`drop: ${files.length} file(s) dropped.`);
        if (files.length) {

            // check types first
            const unsavory = check_unsavory_files(null, files);
            if (unsavory.length) {
                show_unsavory_dialog(unsavory);
                return
            }

            // check sizes second
            const small_files = [], large_files = [], tasks = [];
            let total_size = 0;

            for (const file of files) {
                total_size += file.size
                // sort files into 2 buckets depending on size
                if (file.size > UPLOAD_FSIZE_THRESHOLD) {
                    large_files.push(file);
                } else {
                    small_files.push(file);
                }
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
            quantity.html(`(${files.length} dropped)`);
            droptarget.show_busy();
            if (small_files.length) {
                const fdata = new FormData();
                for (const file of small_files) {
                    fdata.append('files[]', file, file.name);
                }
                tasks.push( [small_files, () =>  // defer promise w/ lambda
                             upload_files_form(window.location.pathname, fdata,
                                               small_files.length)] );
            }
            // send each large file separately
            for (const file of large_files) {
                tasks.push( [[file], () =>  // defer task promise w/ lambda
                             upload_file(window.location.pathname, file)] );
            }
            // get busy
            execute_task_sequence(tasks);

        } else {
            console.error('upload:', err_nofiles);
            show_err_dialog(err_nofiles);
        }
    },
});

