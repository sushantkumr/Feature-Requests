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
            console.log(arg)
            console.log("Name: " + arg.item.name);
            console.log("From: " + arg.sourceParent.id);
            console.log("Location: " + (arg.sourceIndex + 1))
            console.log("To: " + arg.targetParent.id)
            console.log("Location: " + (arg.targetIndex + 1))
            /*  */
        };
    };

    //control visibility, give element focus, and select the contents (in order)
    ko.bindingHandlers.visibleAndSelect = {
        update: function(element, valueAccessor) {
            ko.bindingHandlers.visible.update(element, valueAccessor);
            if (valueAccessor()) {
                setTimeout(function() {
                    $(element).find("input").focus().select();
                }, 0); //new tasks are not in DOM yet
            }
        }
    };

    _viewModel = new FeatureRequestsViewModel();
    ko.bindingHandlers.sortable.afterMove = _viewModel.updateOrder;
    ko.applyBindings(_viewModel);
});
