$(document).ready ( function(){
    function readURL(input) {
        var url = input.value;
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#preview').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        } else {
            $('#preview').attr('src', '/static/base_spotlite/img/profile-blank.jpg');
        }
    }

    $("#file_photo").change(function() {
    readURL(this);
    });

    $(function() {

        // Prepare
        var History = window.History; // Note: We are using a capital H instead of a lower h
        if ( !History.enabled ) {
            // History.js is disabled for this browser.
            // This is because we can optionally choose to support HTML4 browsers or not.
            return false;
        }

        // Bind to StateChange Event
        History.Adapter.bind(window,'statechange',function() { // Note: We are using statechange instead of popstate
            var State = History.getState();
            // $('#content').load(State.url);
            // Instead of the line above, you could run the code below if the url returns the whole page instead of just the content (assuming it has a `#content`):
            $.get(State.url, function(response) {
                var d = document.createElement('div');
                d.innerHTML = response;
                $('#content').html($(d).find('#content').html());
            });
        });

        // Capture all the links to push their url to the history stack and trigger the StateChange Event
        $('a').click(function(evt) {
            evt.preventDefault();
            History.pushState('', $(this).text(), $(this).attr('href'));
        });

        $('a.signout').click(function(evt) {
            evt.preventDefault();
            History.pushState('', '', $(this).attr('href'));
            window.location.replace('/auth/logout');
        });

    });
});