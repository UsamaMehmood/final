function send_friend_request(e, url) {
    var this_elem = $(e);
    var from = this_elem.data("from");
    var to = this_elem.data("to");

    $.ajax({
        url: url,
        type: "post",
        data: {
            from: from,
            to: to,
        },
        success: function (data) {
            this_elem.css("pointer-events", "none");
            this_elem.text("Request sent!");
        }
    })
}
