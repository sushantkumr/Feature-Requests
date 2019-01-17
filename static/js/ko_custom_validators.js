ko.validation.rules['number'] = {
    validator: function(val) {
        return $.isNumeric(val);
    },
    message: 'This field must have a numerical value.'
};

ko.validation.rules['positive'] = {
    validator: function(val) {
        return Number(val) > 0;
    },
    message: 'This field must have a positive numerical value.'
};

ko.validation.rules['nonNegative'] = {
    validator: function(val) {
        return val >= 0;
    },
    message: 'This field must have a non-negative numerical value.'
};

ko.validation.rules['lessThanOrEqual'] = {
    validator: function(val, otherVal) {
        if (typeof otherVal === 'function') {
            otherVal = otherVal();
        }
        return Number(val) <= Number(otherVal);
    },
    message: function(otherVal) {
        if (typeof otherVal === 'function') {
            otherVal = otherVal();
        }
        return 'Value should be less than or equal to ' + otherVal;
    }
};

ko.validation.rules['passwordMatch'] = {
    validator: function(val, otherVal) {
        return val === otherVal;
    },
    message: 'Passwords do not match.'
};

ko.validation.rules['password'] = {
    validator: function(val) {
        return (val.length >= 12 && val.length <= 100);
    },
    message: 'Password should be 12 to 100 characters long.'
};

ko.validation.rules['username'] = {
    validator: function(val) {
        return (val.length >= 5 && val.length <= 100);
    },
    message: 'Username should be 5 to 100 characters long.'
};

ko.validation.rules['usernameChars'] = {
    validator: function(val) {
        return /^[a-zA-Z0-9_]*$/.test(val);
    },
    message: 'Only characters a-z, A-Z, 0-9 and _ are allowed.'
};

ko.validation.registerExtenders();
