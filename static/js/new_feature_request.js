$(document).ready(function() {

    function NewFeatureRequestsViewModel () {
        var self = this;
        self.error = ko.observable();
        self.newTitle = ko.observable().extend({required: true});
        self.newDescription = ko.observable().extend({required: true});
        self.newClient = ko.observable().extend({required: true});
        self.newPriority = ko.observable().extend({required: true});
        self.newTargetDate = ko.observable().extend({required: true});
        self.newProductArea = ko.observable().extend({required: true});

        self.productAreaList = ko.observableArray(['Billing', 'Policies', 'Claims', 'Reports']);
        self.clientList = ko.observableArray();

        self.getClientList = function() {
            ec.utils.ajax('feature_requests', 'views', 'get_client_list', {}, function(response) {
                if (!response.success) {
                    ec.utils.errorHandler(response);
                    return;
                }
                else {
                    if(response.data == 'ALL') {
                        self.clientList(['Client A', 'Client B', 'Client C']);
                    }
                    else {
                        self.clientList([response.data]);
                        self.newClient(response.data);
                    }
                };
            });
        }

        self.getClientList();

        self.submitRequest = function() {
            const errors = ko.validation.group([self.newTitle, self.newDescription, self.newClient, self.newPriority, self.newTargetDate, self.newProductArea]);
            if (errors().length > 0) {
                errors.showAllMessages(true);
                return;
            }

            const data = {
                title: self.newTitle(),
                description: self.newDescription(),
                client: self.newClient(),
                priority: self.newPriority(),
                target_date: self.newTargetDate(),
                product_area: self.newProductArea()
            };
            ec.utils.ajax('feature_requests', 'views', 'submit_feature_requests', data, function(response) {
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
