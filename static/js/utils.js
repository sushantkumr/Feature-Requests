var ec = ec || {};
ec.utils = {};

ec.utils.get_ajax_url = function(module, file, method) {
    return '/ajax?module=' + module + '&file=' + file + '&method=' + method;
};

ec.utils.ajax = function(module, file, method, data, success, error) {
    success = success || console.log;
    error = error || function() {
        console.log(arguments);
        ec.utils.bootboxError('An unexpected error occurred while processing your request. Please try again after some time.');
    };

    if (typeof success === 'function' &&
        typeof error === 'function' &&
        typeof module === 'string' &&
        typeof file === 'string' &&
        typeof method === 'string' &&
        typeof data === 'object') {
        return $.ajax({
            method: 'POST',
            contentType: 'application/json',
            url: ec.utils.get_ajax_url(module, file, method),
            data: JSON.stringify(data),
            success: success,
            error: error
        });
    }
    else {
        console.error('Invalid param type found:', module, file, method, data, success, error);
    }
};

ec.utils.refreshPage = function() {
    window.location.reload();
};

ec.utils.bootboxError = function(message, callback) {
    var _callback = ec.utils.doNothing;
    if (typeof message == 'object') {
        if (message.pageRefresh) {
            _callback = ec.utils.refreshPage;
        }
        else if (message.callback) {
            _callback = message.callback;
        }
        else if (typeof callback === 'function') {
            _callback = callback;
        }
        if (typeof message.message === 'string') {
            message = message.message;
        }
        else {
            message = JSON.stringify(message);
        }
    }
    bootbox.alert({
        title: 'Error',
        message: message,
        callback: _callback
    });
};

ec.utils.bootboxInformation = function(message, callback) {
    if (typeof callback !== 'function') {
        callback = function(){};
    }
    bootbox.alert({title: 'Information', message: message, callback: callback});
};

ec.utils.errorHandler = function(response, method) {
    var message = response.message;
    var type = response.type;
    var pageRefresh = response.pageRefresh || false;

    if (typeof message !== 'string') {
        return;
    }

    if (type === 'alert-error') {
        ec.utils.bootboxError({message: message, pageRefresh: pageRefresh});
    }
    else if (type === 'alert-information') {
        ec.utils.bootboxInformation(message);
    }
    else if (typeof method === 'function') {
        method(message);
    }
    else {
        ec.utils.bootboxError(message);
    }
};

ec.utils.getQueryStringValue = function(key) {
    key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
    var match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));
    return match && decodeURIComponent(match[1].replace(/\+/g, " "));
};

ec.utils.deleteConfirmation = function(module, file, method, data, success, error) {
    const message = 'Do you really want to delete this request?'
    bootbox.confirm(message, function(result) {
        if(result) {
            ec.utils.ajax(module, file, method, data, success, error);
        }
        else {
            return;
        }
    });
};
