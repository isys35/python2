function loadMessages() {
    $.ajax(
        {
            url:HOST + `hotel-api/messages/${user_id}`,
            method: "get",
            success: function (data) {
                for (let i=0; i<data.length; i++){
                    let innerHtml = "<div class=\"message-text\">\n" +
                        `                <span>${data[i].text}</span>\n` +
                        "                <span class=\"message-time\"></span>\n" +
                        "            </div>";
                    $(".dialog").append(innerHtml);
                }
                if (data) {
                    $(".head-username").text(data[0].username);
                }
            },
        }
    )
}



$(document).ready(loadMessages())