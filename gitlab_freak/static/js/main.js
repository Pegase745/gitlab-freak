(function() {

    $("[name='dep-checkbox']").bootstrapSwitch({
        size: "small",
        labelText: "Deps",
        onSwitchChange: function(event, state) {
            event.preventDefault();
            var data = {
                "project_id": $(this).data("id"),
                "project_type": $(this).data("type"), 
            };

            var url = "/register";

            if (!state) {
                url = "/unregister";
            }

            $.ajax(url, {
                data : JSON.stringify(data),
                contentType : 'application/json',
                type : 'POST',
                success: function () {
                    return console.log('done post');
                }
            });
        }
    });

}).call(this);
