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
        self.error = ko.observable();
        self.newTitle = ko.observable().extend({required: true});
        self.newDescription = ko.observable().extend({required: true});
        self.newClient = ko.observable().extend({required: true});
        self.newPriority = ko.observable().extend({required: true, number: true, positive: true});
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
                    console.log(response.data[0]["name"]);
                    console.log(response.data.length)
                    self.clientList(response.data);
                    if(response.data.length == 1) {
                        self.newClient({name: response.data[0]["name"]});
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
