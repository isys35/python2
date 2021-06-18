
function loadCheckIns() {
    $.ajax(
        {
            url:HOST + `hotel-api/checkins/`,
            method: "get",
            success: function (data) {
                for (let i=0; i<data.length; i++){
                    let innerHtml = "";
                    if (data[i].last_message_today) {
                        innerHtml = "<div class=\"check-in-info\">\n" +
                     `            <h2>Номер ${data[i].room}</h2>\n` +
                     `            <p>Живёт: ${data[i].user}</p>\n` +
                     `            <p>Заехал: ${data[i].started_at}</p>\n` +
                     `            <p>Выезжает: ${data[i].ended_at}</p>\n` +
                     "            <div class=\"last-message\">\n" +
                     "                <div class=\"last-message-head\">\n" +
                     "                    <span>Последнее сообщение сегодня:</span>\n" +
                     "                </div>\n" +
                     "                <div class=\"last-message-text-block\">\n" +
                     "                    <div class=\"last-message-text\">\n" +
                     `                        <span>${data[i].last_message_today.text}</span>\n` +
                     `                        <span class=\"last-message-time\">${data[i].last_message_today.pub_date}</span>\n` +
                     "                    </div>\n" +
                     "                    <a href=\"/hotel/messages-history/\">Посмотреть историю сообщений</a>\n" +
                     "                </div>\n" +
                     "                </div>\n" +
                     "        </div>"
                    } else {
                        innerHtml = "<div class=\"check-in-info\">\n" +
                     `            <h2>Номер ${data[i].room}</h2>\n` +
                     `            <p>Живёт: ${data[i].user}</p>\n` +
                     `            <p>Заехал: ${data[i].started_at}</p>\n` +
                     `            <p>Выезжает: ${data[i].ended_at}</p>\n` +
                     "            <div class=\"last-message\">\n" +
                     "             </div>\n" +
                     "        </div>"
                    }
                    $(".admin-info-container").append(innerHtml);
                }
            },
        }
    )
}


$(document).ready(loadCheckIns())