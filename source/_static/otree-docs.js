$(document).ready(function(){

    // Patch objects
    String.prototype.title = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }

    String.prototype.join = function(arr) {
        if(arr.length == 0)
            return "";
        if(arr.length == 1)
            return arr[0];
        var joined = arr[0];
        for(var idx=1; idx < arr.length; idx++)
            joined += this + arr[idx];
        return joined;
    }


    // dynamic link
    var LAUNCHER_VERSION_URL = "https://raw.githubusercontent.com/oTree-org/otree-launcher/master/otree_launcher/res/version.json";
    var LAUNCHER_HREF = "https://github.com/oTree-org/otree-launcher/archive/master.zip";

    var $dynamicLinkDiv = $("#otree-launcher-dynamic-link");

    if(!!$dynamicLinkDiv.length){
        $.getJSON(LAUNCHER_VERSION_URL, function(data){
            var version = ".".join(data.version);
            var download = "oTree_launcher-" + version + ".zip";

            var parts = [
                "<a href='" + LAUNCHER_HREF + "' ",
                "download='" + download + "'>",
                download,
                "</a>"
            ];
            var $link = $("".join(parts));

            $dynamicLinkDiv.empty();
            $dynamicLinkDiv.append($link);
        }).fail(function() {
            var parts = [
                "<a href='" + LAUNCHER_HREF + "'>",
                "oTree_launcher-stable.zip",
                "</a>"
            ];
            var $link = $("".join(parts));

            $dynamicLinkDiv.empty();
            $dynamicLinkDiv.append($link);
        });
    }

});
