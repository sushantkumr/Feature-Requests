$(document).ready(function() {

    function FeatureRequestsViewModel () {
        var self = this;
        self.featureRequests = ko.observableArray();
        self.getFeatureRequests = function() {
            ec.utils.ajax('feature_requests', 'views', 'get_feature_requests', {}, function(response) {
                if (!response.success) {
                    ec.utils.errorHandler(response);
                    return;
                }
                self.featureRequests(response.data);
            });
        }
        self.getFeatureRequests();
    };

    _viewModel = new FeatureRequestsViewModel();
    ko.applyBindings(_viewModel);
});
