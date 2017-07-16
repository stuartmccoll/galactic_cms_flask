$(document).ready(function(){

    if ($(".failure-message-1").text().length > 0) {

        $(".notification-failure").css("display", "block");
    
        $(".notification-wrapper").css("display", "block");
        $(".notification-wrapper").addClass("notification-slide-in");

        setTimeout(function(){
            $(".notification-wrapper").removeClass("notification-slide-in");
            $(".notification-wrapper").addClass("notification-slide-out");
            setTimeout(function(){
                $(".notification-wrapper").removeClass("notification-slide-out");
                $(".notification-wrapper").css("display", "none");
                $(".notification-failure").css("display", "none");
            }, 1000);
        }, 5000);

    }

});