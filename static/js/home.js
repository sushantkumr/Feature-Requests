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

        this.updateOrder = function(arg) {
            const movedFRclient = arg.item["client"];
            const movedFRid = arg.item["id"];
            let listOfFRForClient = [];
            let newPriority;
            console.log(self.featureRequests());
            for(index = 0; index < self.featureRequests().length; index++) {
                fr = self.featureRequests()[index];
                if (fr["client"] == movedFRclient) {
                    listOfFRForClient.push(fr);
                }
            }

            for(index = 0; index < listOfFRForClient.length; index++) {
                if (listOfFRForClient[index]["id"] == movedFRid)
                    newPriority = index + 1;
            }

            const data = {
                id: movedFRid,
                client: movedFRclient,
                new_priority: newPriority,
            };

            ec.utils.ajax('feature_requests', 'views', 'update_for_drag_drop', data, function(response) {
                if (!response.success) {
                    ec.utils.errorHandler(response);
                    return;
                }
                self.featureRequests(response.data);
            });            
        };
    };

    _viewModel = new FeatureRequestsViewModel();
    ko.bindingHandlers.sortable.afterMove = _viewModel.updateOrder;
    ko.applyBindings(_viewModel);
});
