function onSubmitSendMessage() {
    $("#send-message-btn").on("click", function () {
        let sendedData = {"csrfmiddlewaretoken": csrftoken,
                            "text":$("#text").val()}
        $.ajax({
            url: HOST + "hotel-api/send_message/",
            method: "post",
            data:sendedData ,
            success: function (data) {
                 let dialog = $(".dialog");
                 let message = "<div class=\"message-text\">\n" +
                        `                <span>${data.text}</span>\n` +
                        `                <span class=\"message-time\">${data.pub_date}</span>\n` +
                        "            </div>";
                 dialog.append(message);
            },
        });
	});
}

$(document).ready(onSubmitSendMessage());