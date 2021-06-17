function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateReservationList(data) {
    let roomReservationListBlock = $(".room-reservation-list");
    if (roomReservationListBlock.length) {
                    for (let i=0; i<data.length; i++) {
                        let innerHTML = "<div class=\"room-reservation-item\">\n" +
                            `                <span>C ${data[i].started_at} по ${data[i].ended_at}</span>\n` +
                            "            </div>"
                        roomReservationListBlock.append(innerHTML);
                    }
                 }
}


var csrftoken = getCookie('csrftoken');
var HOST = "http://127.0.0.1:8000/"