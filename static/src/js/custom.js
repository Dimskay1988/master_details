odoo.define('master_details.custom', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    FormController.include({
        _updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName === 'contract.work') {
                var self = this;
                rpc.query({
                    model: 'contract.work',
                    method: 'search_read',
                    args: [[['id', '=', this.handle.getContext().active_id]], ['description', 'job_ids', 'job_ids.group_ids']],
                }).then(function (result) {
                    console.log(result)
                    if (result && result.length) {
                        var work = result[0];
                        var description = work.description || '';
                        var jobIds = work.job_ids || [];
                        var groupIds = [];
                        jobIds.forEach(function (job) {
                            if (job.group_ids) {
                                groupIds = groupIds.concat(job.group_ids);
                            }
                        });

                        var message = _t("Description: ") + description + "\n";
                        message += _t("Job IDs:\n");
                        jobIds.forEach(function (job) {
                            message += "  - " + job.name + "\n";
                        });
                        message += _t("Group IDs:\n");
                        groupIds.forEach(function (group) {
                            message += "  - " + group.description + " (Diameter: " + group.diameter + ")\n";
                        });

                        self.renderer.displayNotification({
                            type: 'warning',
                            title: _t('Work Details'),
                            message: message,
                        });
                    }
                });
            }
        },
    });
});
