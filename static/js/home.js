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
        self.confirmDelete = function(row) {
            data = {
                id: row["id"],
                priority: row["client_priority"],
                client: row["client"],
            };

            const message = 'Do you really want to delete this request?'
            bootbox.confirm(message, function(result) {
                if(result) {
                    ec.utils.ajax('feature_requests', 'views', 'delete_request', data, function(response) {
                        if (!response.success) {
                            ec.utils.errorHandler(response);
                            return;
                        }
                        self.featureRequests(response.data);
                    });
                }
            });
        }

        self.getFeatureRequests();

        this.updateOrder = function(arg) {
            const movedFRclient = arg.item["client"];
            let listOfFRForClient = [];
            let newPriorities = {};
            for(index = 0; index < self.featureRequests().length; index++) {
                fr = self.featureRequests()[index];
                if (fr["client"] == movedFRclient) {
                    listOfFRForClient.push(fr);
                }
            }

            for(index = 0; index < listOfFRForClient.length; index++) {
                newPriorities[listOfFRForClient[index]["id"]] = index + 1;
            }

            const data = {
                client: movedFRclient,
                new_priorities: newPriorities,
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
