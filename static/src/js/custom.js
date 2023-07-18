odoo.define('masterdetails.custom_script', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');

    var YourCustomClass = core.Class.extend({
        start: function () {
            // Retrieve all records from contract.guide model
            rpc.query({
                model: 'contract.guide',
                method: 'search_read',
                args: [[]],
                kwargs: { fields: ['eil_nr', 'parent_id', 'group', 'diameter', 'operations'] }
            }).then(function (records) {
                console.log('Records from contract.guide:', records);
            });

            console.log('Custom script has been loaded.');
        }
    });

    // Instantiate your class and start it
    var yourCustomInstance = new YourCustomClass();
    yourCustomInstance.start();
});