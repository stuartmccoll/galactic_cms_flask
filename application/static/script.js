$("#create-post-submit").on("click", function(e) {
    $(this).attr("disabled", "disabled");
    // Prevent the form from refreshing the page
    e.preventDefault();

    if ($("#post-title").val() == "" || $("#post-content").val() == "") {
        displayNotification("failure", "Please enter", "all mandatory fields", 3000, 1000);
    } else {
        $.ajax({
            type: "POST",
            url: "/admin/create-post",
            data: $("#create-post").serialize(),
            success: function(response) {
                // Handle success response here
                $(".form-control").val("");
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
            url: "/admin/edit-post/"+post_id,
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

$("#update-settings-submit").on("click", function(e) {
    $(this).attr("disabled", "disabled");
    // Prevent the form from refreshing the page
    e.preventDefault();
    if ($("#first-name").val() == "" || $("#last-name").val() == "") {
        displayNotification("failure", "Please enter", "all mandatory fields", 3000, 1000);
    } else {
        $.ajax({
            type: "POST",
            url: "/admin/user-settings",
            data: $("#user-settings").serialize(),
            success: function(response) {
                // Handle success response here
                displayNotification("success", "User settings", "updated successfully", 5000, 1000);
            },
            error: function(response) {
                // Handle error response here
                displayNotification("failure", "Error occurred when", "updating user settings", 5000, 1000);
            }
        });
    }
});

$(".theme-activate").on("click", function(e) {

    e.preventDefault();

    var theme_name = $(this).parent().prop('className').replace("theme-", "");

    $.ajax({
        type: "POST",
        url: "/admin/themes/activate/" + theme_name,
        success: function(response) {
            sessionStorage.notification = "success";
            location.reload();
        },
        error: function(response) {
            sessionStorage.notification = "error";
            location.reload();
            // Handle error response here
        }
    });

});

$(function() {
    if ( sessionStorage.notification === "success" ) {
        displayNotification("success", "Theme has been", "activated successfully", 5000, 1000);
        sessionStorage.notification = "";
    } else if (sessionStorage.notification === "error") {
        displayNotification("failure", "Error occured when", "activating theme", 5000, 1000);
        sessionStorage.notification = "";
    }
});

$(".btn-edit-post").on("click", function() {

    var post_id = event.target.id.toString().replace("edit-post-", "");
    window.location.href = "/admin/edit-post/"+post_id;

});

$(".btn-delete-post").on("click", function () {
     var post_id = event.target.id.toString().replace("delete-post-", "");
     $(".modal-body").attr("id", post_id);
     $(".modal-header").addClass("modal-header-delete");
     $(".modal-title").text("Delete Post");
     $(".modal-body").text("Are you sure you want to delete this post?");
     $(".modal-footer").html("<button class='btn-modal-cancel' data-dismiss='modal'><span class='glyphicon glyphicon-remove' aria-hidden='true'></span> Cancel</button> <button class='btn-confirm-delete-post' data-dismiss='modal'><span class='glyphicon glyphicon-trash' aria-hidden='true'></span> Confirm Delete</button>");
});

$(".modal-footer").on("click", ".btn-confirm-delete-post", function() {

    var post_id = $(".modal-body").attr("id");
    
    $.ajax({
        type: "GET",
        url: "/admin/delete-post/" + post_id,
        success: function(response) {
            // Obtain the class name of the relevant row then remove it from the table
            console.log(response);
            if (response === "Post deleted successfully") {
                var row_name = ".row-"+post_id;
                $(row_name).remove();
                displayNotification("success", "Blog post", "deleted successfully", 5000, 1000);
            }
        },
        error: function(response) {
            displayNotification("failure", "Error occurred when", "deleting blog post", 5000, 1000);
        } 
    });

});

$(".modal").on("hidden.bs.modal", function(){
    $(".modal-body").attr("id", "");
    $(".modal-header").removeClass().addClass("modal-header");
    $(".modal-title").text("");
    $(".modal-body").text("");
    $(".modal-footer").empty();
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
            $("#update-settings-submit").removeAttr("disabled");
        }, timer2);
    }, timer1);

}