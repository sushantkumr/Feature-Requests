$(document).ready(function() {
    
    let today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1; //January is 0!
    let yyyy = today.getFullYear();

    if(dd<10) {
        dd = '0' + dd;
    }

    if(mm<10) {
        mm = '0' + mm;
    }

    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById('targetDate').setAttribute("min", today);

    function NewFeatureRequestsViewModel () {
        var self = this;
        self.id = ko.observable();
        self.error = ko.observable();
        self.newTitle = ko.observable().extend({required: true});
        self.newDescription = ko.observable().extend({required: true});
        self.newClient = ko.observable().extend({required: true});
        self.newPriority = ko.observable().extend({required: true});
        self.newTargetDate = ko.observable().extend({required: true});
        self.newProductArea = ko.observable().extend({required: true});

        self.productAreaList = ko.observableArray(['Billing', 'Policies', 'Claims', 'Reports']);
        self.clientList = ko.observableArray();

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
                    self.newPriority(response.data.client_priority);
                    self.newTargetDate(moment(response.data.target_date).format('YYYY-MM-DD'));
                    self.newProductArea(response.data.product_area);
                    if(response.data.clientList == 'ALL') {
                        self.clientList([
                            {id: 0, name: 'ALL'},
                            {id: 1, name: 'Client A'},
                            {id: 2, name: 'Client B'},
                            {id: 3, name: 'Client C'},
                        ]);
                    }
                    else {
                        self.clientList([{name: response.data.clientList}]);
                    }
                    self.newClient({name: response.data.client});
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
