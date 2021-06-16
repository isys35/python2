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
var csrftoken = getCookie('csrftoken');
/*$(document).ready( function () {
    $(".rate-btn").on('click', function () {
        let type_service_id = $(this).attr('id').split('_')[1];
        let rate = $(this).attr('id').split('_')[2];
        $.ajax({
            url: "put_rate/",
            method: "POST",
            data: {'csrfmiddlewaretoken': csrftoken, 'type_service_id': type_service_id,
                'rate':rate
            },
            success: function (data) {
                $(`#rate-avg_${type_service_id}`).text(data['avg_rate']);
                $(`#rate-avg-count_${type_service_id}`).text(`(${data['count_rate']})`);
            }
        });
        $.ajax({
            url: "avg_rate/",
            method: "GET",
            success: function (data) {
                $(".avg-avg-rate").text(`Средний рейтинг: ${data['avg_rate']}`);
            }
        });
    })
})*/

function load_rooms() {
    let roomsContainer = $(".rooms-container");
    if (roomsContainer) {
        $.ajax({
            url: "hotel-api/rooms/",
            method: "GET",
            success: function (data) {
                for (i=0; i<data.length; ++i) {
                    var roomDom = "<div>\n" +
                    "   <div class=\"panel panel-default\">\n" +
                    `       <div class=\"panel-heading\"><a href=\"room/${data[i].id}\">Номер ${data[i].number}</a></div>\n` +
                    `       <div class=\"panel-body\"><a href=\"room/${data[i].id}\">${data[i].room_class} класс</a></div>\n` +
                    "   </div>\n" +
                    "</div>"
                    roomsContainer.append(roomDom);
                }
            }
        });
    }
}

function load_page() {
    load_rooms();
}

$(document).ready(load_page())