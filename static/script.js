$("#create-post-submit").on("click", function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/create-post",
        data: $("#create-post").serialize(),
        success: function(response) {
            // Handle success response here
        },
        error: function(response) {
            // Handle error response here
        }
    });
});