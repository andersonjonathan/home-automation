/**
 * Created by jonathan on 2016-01-14.
 */
/**
 * Created by jonathan on 2015-11-09.
 */
function init_csrf() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
function send_command(element, mode, url) {
    init_csrf();

    var $element = $(element);
    var $parent = $($element.parent().get(0));

    $parent.children('a').each(function () {
        var child = $(this);
        child.removeClass('active');
        child.removeClass('btn-success');
        child.removeClass('btn-danger');
        child.removeClass('btn-primary');
        child.addClass('btn-default');
    });
    $element.addClass('active');
    $element.addClass(mode);
    

    $.ajax({
        "type": "get",
        "dataType": "json",
        "url": url,
        "success": function (result) {
            if (result.status === "ok") {

            } else {
                console.log(result.status);
            }
        }
    });

}