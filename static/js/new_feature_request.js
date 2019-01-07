$(document).ready(function() {

    function NewFeatureRequestsViewModel () {
        var self = this;
        self.newTitle = ko.observable();
        self.newDescription = ko.observable();
        self.newClient = ko.observable();
        self.newPriority = ko.observable();
        self.newTargetDate = ko.observable();
        self.newProductArea = ko.observable();

        self.productAreaList = ko.observableArray(['Billing', 'Policies', 'Claims', 'Reports']);
        self.clientList = ko.observableArray(['Client A', 'Client B', 'Client C']);

        const data = {
                    title: self.newTitle(),
                    description: self.newDescription(),
                    client: self.newClient(),
                    priority: self.newPriority(),
                    target_date: self.newTargetDate(),
                    product_area: self.newProductArea()
        };

        self.submitRequest = function() {
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
