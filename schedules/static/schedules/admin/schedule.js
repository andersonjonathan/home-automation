(function ($) {
    $(function () {
        var $device_select = $("select#id_device");
        var $on_select = $("select#id_on");
        var $off_select = $("select#id_off");
        $device_select.change(function () {
            $.getJSON("/buttons/" + $(this).val(), {}, function (j) {
                var options = '<option value="">--------&nbsp;</option>';
                for (var i = 0; i < j.buttons.length; i++) {
                    options += '<option value="' + j.buttons[i].optionValue + '">' + j.buttons[i].optionDisplay + '</option>';
                }
                $on_select.html(options);
                $on_select.find("option:first").attr('selected', 'selected');
                $off_select.html(options);
                $off_select.find("option:first").attr('selected', 'selected');
            });
            $device_select.attr('selected', 'selected');
        });
        $.getJSON("/buttons/" + $device_select.val(), {}, function (j) {
            var options = '<option value="">--------&nbsp;</option>';
            for (var i = 0; i < j.buttons.length; i++) {
                options += '<option value="' + j.buttons[i].optionValue + '">' + j.buttons[i].optionDisplay + '</option>';
            }
            var on = $on_select.val();
            var off = $off_select.val();
            $on_select.html(options);
            $off_select.html(options);
            $on_select.find("option").filter(function (i, e) {
                return $(e).val() == on;
            }).attr('selected', 'selected');
            $off_select.find("option").filter(function (i, e) {
                return $(e).val() == off;
            }).attr('selected', 'selected');
        });
        $device_select.attr('selected', 'selected');
    });
})(django.jQuery);