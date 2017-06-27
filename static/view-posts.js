$(document).ready(function(){

    $.ajax({
        type: "GET",
        url: "/get-posts",
        success: function(response) {

            var table = $("<table class='table table-striped view-posts-table'></table>");
            $(".view-posts-content").append(table);

            if (response.length === 0) {
                $(".view-posts-table").append("<thead><tr><th>Post Title</th><th>View Post</th><th>Edit Post</th><th>Delete Post</th></tr></thead>");
                $(".view-posts-table").append("<tbody><tr><td class='zero-posts' colspan='4'><p>No posts currently exist.</p><p>Why not <a href='./create-post'>add a new post</a>?</p></td></tr></tbody>");
            } else {

                $(".view-posts-table").append("<thead><tr><th>Post Title</th><th>View Post</th><th>Edit Post</th><th>Delete Post</th></tr></thead>");
                $(".view-posts-table").append("<tbody></tbody>");

                for(i = 0; i < response.length; i++)
                    $(".view-posts-table").append("<tr class='row-"+response[i].id+"'><td class='col-md-9'>"+response[i].title+"</td><td class='col-md-1'><button class='btn-view-post'>View Post</button</td><td class='col-md-1'><button class='btn-edit-post'>Edit Post</button></td><td class='col-md-1'><button id='delete-post-"+response[i].id+"' class='btn-delete-post'>Delete Post</button></td></tr>");

            }

            $(".btn-delete-post").on("click", function() {

                var post_id = event.target.id.toString().replace("delete-post-", "");
                
                $.ajax({
                    type: "GET",
                    url: "/delete-post/" + post_id,
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
                })

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
                    }, timer2);
                }, timer1);

            }

        },
        error: function(response) {
            // Handle error response here
            console.log("oops...");
        }
    });

});