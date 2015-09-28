(function() {

    $("[name='my-checkbox']").bootstrapSwitch({
        size: "small",
        labelText: "Deps",
        onSwitchChange: function(event, state) {
            event.preventDefault();
            return console.log(state, event.isDefaultPrevented());
        }
    });

}).call(this);
