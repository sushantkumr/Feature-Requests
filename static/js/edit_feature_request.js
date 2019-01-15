$(document).ready(function() {

    function NewFeatureRequestsViewModel () {
        var self = this;
        self.id = ko.observable();
        self.error = ko.observable();
        self.newTitle = ko.observable().extend({required: true, usernameChars: true, username: true});
        self.newDescription = ko.observable().extend({required: true, usernameChars: true, username: true});
        self.newClient = ko.observable().extend({required: true});
        self.newPriority = ko.observable().extend({required: true});
        self.newTargetDate = ko.observable().extend({required: true});
        self.newProductArea = ko.observable().extend({required: true});

        self.productAreaList = ko.observableArray(['Billing', 'Policies', 'Claims', 'Reports']);
        self.clientList = ko.observableArray(['Client A', 'Client B', 'Client C']);

        self.getRequestDetails = function() {
            self.id(ec.utils.getQueryStringValue('id'));

            const data = {
                'id': self.id()
            }

            ec.utils.ajax('feature_requests', 'views', 'get_feature_request_details', data, function(response) {
                if (!response.success) {
                    ec.utils.errorHandler(response);
                    return;
                }
                else {
                    self.newTitle(response.data.title);
                    self.newDescription(response.data.description);
                    self.newClient(response.data.client);
                    self.newPriority(response.data.client_priority);
                    self.newTargetDate(moment(response.data.target_date).format('YYYY-MM-DD'));
                    self.newProductArea(response.data.product_area);
                };
            });
        }

        self.getRequestDetails();

        self.submitRequest = function() {
            const errors = ko.validation.group([self.newTitle, self.newDescription, self.newClient, self.newPriority, self.newTargetDate, self.newProductArea]);
            if (errors().length > 0) {
                errors.showAllMessages(true);
                return;
            }

            const data = {
                id: self.id(),
                title: self.newTitle(),
                description: self.newDescription(),
                client: self.newClient(),
                priority: self.newPriority(),
                target_date: self.newTargetDate(),
                product_area: self.newProductArea()
            };
            ec.utils.ajax('feature_requests', 'views', 'update_feature_requests', data, function(response) {
                if (!response.success) {
                    ec.utils.errorHandler(response);
                    return;
                }
                ec.utils.bootboxInformation('Your request has been submitted.', function() {
                        window.location = '/';
                });
            });
        }
    };

    _viewModel = new NewFeatureRequestsViewModel();
    ko.applyBindings(_viewModel);
});
