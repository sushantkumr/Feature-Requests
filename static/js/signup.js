$(document).ready(function() {

    function SignUpViewModel () {
        let self = this;
        self.display = ko.observable('showChangePassword');
        self.error = ko.observable();
        self.username = ko.observable().extend({required: true, username: true, usernameChars: true});
        self.password = ko.observable().extend({required: true, password: true});
        self.confirmPassword = ko.observable().extend({required: true, password: true, passwordMatch: self.password});
        self.client = ko.observable().extend({required: true});
        self.clientList = ko.observableArray([
            {id: 0, name: 'ALL'},
            {id: 1, name: 'Client A'},
            {id: 2, name: 'Client B'},
            {id: 3, name: 'Client C'},
          ]);

        self.signup = function() {

            const errors = ko.validation.group([self.username, self.password, self.confirmPassword]);
            if (errors().length > 0) {
                errors.showAllMessages(true);
                return;
            }

            const data = {
                username: self.username(),
                password: self.password(),
                confirm_password: self.confirmPassword(),
                client: self.client(), 
            };

            self.error('');
            $.ajax({
                method: 'POST',
                contentType: 'application/json',
                url: '/signup',
                data: JSON.stringify(data),
                success: function (response) {
                    if (response.success) {
                        window.location = '/';
                    }
                    else {
                        self.error('Error: ' + response.message);
                    }
                },
                error: function(a, b, c) {
                    console.log(a, b, c);
                    ec.utils.bootboxError('An unexpected error occurred while creating an account. Please try again later.');
                }
            });
        }
    }    

    const _signupViewModel = new SignUpViewModel();
    ko.applyBindings(_signupViewModel);
});
