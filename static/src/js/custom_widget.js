odoo.define('your_module.custom_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractField = require('web.AbstractField');

    var YourCustomWidget = AbstractField.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _render: function () {
            this.$el.text('Custom Widget');
        },
    });

    core.form_widget_registry.add('your_custom_widget', YourCustomWidget);

    return {
        YourCustomWidget: YourCustomWidget,
    };
});
