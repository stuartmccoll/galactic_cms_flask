$("#create-post-submit").on("click", function(e) {
    $(this).attr("disabled", "disabled");
    // Prevent the form from refreshing the page
    e.preventDefault();

    if ($("#post-title").val() == "" || $("#post-content").val() == "") {
        displayNotification("failure", "Please enter", "all mandatory fields", 3000, 1000);
    } else {
        $.ajax({
            type: "POST",
            url: "/create-post",
            data: $("#create-post").serialize(),
            success: function(response) {
                // Handle success response here
                $("#post-title").val("");
                $("#post-content").val("");
                displayNotification("success", "Blog post", "created successfully", 5000, 1000);
            },
            error: function(response) {
                // Handle error response here
                displayNotification("failure", "Error occurred when", "creating new blog post", 5000, 1000);
            }
        });
    }
});

$("#update-post-submit").on("click", function(e) {
    $(this).attr("disabled", "disabled");

    var post_id = $("#hidden-id").val();

    if ($("#post-title").val() == "" || $("#post-content").val() == "") {
        displayNotification("failure", "Please enter", "all mandatory fields", 3000, 1000);
    } else {
        $.ajax({
            type: "POST",
            url: "/edit-post/"+post_id,
            data: $("#update-post").serialize(),
            success: function(response) {
                // Handle success response here
                displayNotification("success", "Blog post", "updated successfully", 5000, 1000);
                // Prevent the form from refreshing the page
                e.preventDefault();
            },
            error: function(response) {
                // Handle error response here
                displayNotification("failure", "Error occurred when", "updating blog post", 5000, 1000);
            }
        });
    }
});

function displayNotification(type, message1, message2, timer1, timer2) {

    if (type == "failure") {
        $(".failure-message-1").text(message1);
        $(".failure-message-2").text(message2);
        $(".notification-failure").css("display", "block");
    }

    if (type == "success") {
        $(".success-message-1").text(message1);
        $(".success-message-2").text(message2);
        $(".notification-success").css("display", "block");
    }
    
    $(".notification-wrapper").css("display", "block");
    $(".notification-wrapper").addClass("notification-slide-in");

    setTimeout(function(){
        $(".notification-wrapper").removeClass("notification-slide-in");
        $(".notification-wrapper").addClass("notification-slide-out");
        setTimeout(function(){
            $(".notification-wrapper").removeClass("notification-slide-out");
            $(".notification-wrapper").css("display", "none");
            
            if (type === "failure") {
                $(".notification-failure").css("display", "none");
            }

            if (type === "success") {
                $(".notification-success").css("display", "none");
            }

            $("#create-post-submit").removeAttr("disabled");
            $("#update-post-submit").removeAttr("disabled");
        }, timer2);
    }, timer1);

}