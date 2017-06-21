$(document).ready(function(){

    $.ajax({
        type: "GET",
        url: "/get-posts",
        success: function(response) {
            // Handle success response here
            console.log(response);

            if (response.length === 0) {
                // Handle zero posts returned here
            } else {

                var table = $("<table class='table table-striped view-posts-table'></table>");

                $(".view-posts-content").append(table);
                $(".view-posts-table").append("<thead><tr><th>Post Title</th><th>View Post</th><th>Edit Post</th><th>Delete Post</th></tr></thead>");
                $(".view-posts-table").append("<tbody></tbody>");

                for(i = 0; i < response.length; i++)
                    $(".view-posts-table").append("<tr><td class='col-md-9'>"+response[i].title+"</td><td class='col-md-1'><button class='btn-view-post'>View Post</button</td><td class='col-md-1'><button class='btn-edit-post'>Edit Post</button></td><td class='col-md-1'><button class='btn-delete-post'>Delete Post</button></td></tr>");

            }
        },
        error: function(response) {
            // Handle error response here
            console.log("oops...");
        }
    });

});