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

function loadRooms() {
    let roomsContainer = $(".rooms-container");
    if (roomsContainer) {
        $.ajax({
            url: "hotel-api/rooms/",
            method: "GET",
            success: function (data) {
                for (let i=0; i<data.length; ++i) {
                    let roomHtml = "<div>\n" +
                    "   <div class=\"panel panel-default\">\n" +
                    `       <div class=\"panel-heading\"><a href=\"room/${data[i].id}\">Номер ${data[i].number}</a></div>\n` +
                    `       <div class=\"panel-body\"><a href=\"room/${data[i].id}\">${data[i].room_class} класс</a></div>\n` +
                    "   </div>\n" +
                    "</div>"
                    roomsContainer.append(roomHtml);
                }
            }
        });
    }
}

function loadTypeServices() {
    let typeServicesContainer = $(".type-services-container");
     if (typeServicesContainer) {
         $.ajax({
            url: "hotel-api/services/",
            method: "GET",
            success: function (data) {
                for (let i=0; i<data.length; ++i) {
                    let servicesHtml = "" +
                        "<div class=\"rate\">\n" +
                        "    <div class=\"rate-title\">\n" +
                        `         <span>${data[i].title}</span>\n` +
                        "    </div>\n" +
                        `        <a class=\"rate-btn\" id=\"typeservice_${data[i].id}_1\" href=\"#\"><span class=\"emoji\">😠</span></a>\n` +
                        `         <a class=\"rate-btn\" id=\"typeservice_${data[i].id}_2\" href=\"#\"><span class=\"emoji\">😦</span></a>\n` +
                        `         <a class=\"rate-btn\" id=\"typeservice_${data[i].id}_3\" href=\"#\"><span class=\"emoji\">😑</span></a>\n` +
                        `         <a class=\"rate-btn\" id=\"typeservice_${data[i].id}_4\" href=\"#\"><span class=\"emoji\">😀</span></a>\n` +
                        `         <a class=\"rate-btn\" id=\"typeservice_${data[i].id}_5\" href=\"#\"><span class=\"emoji\">😍</span></a>\n` +
                        "         <div class=\"rate-avg\">\n" +
                        `             <span id=\"rate-avg_${data[i].id}\">${data[i].avg_rate}</span>\n` +
                        `             <span id=\"rate-avg-count_${data[i].id}\" class=\"rate-avg-count\">(${data[i].count_rate})</span>\n` +
                        "         </div>\n" +
                        "</div>"
                    typeServicesContainer.append(servicesHtml);
                }
            }
        });
     }
}

function loadPage() {
    loadRooms();
    loadTypeServices();
}

$(document).ready(loadPage())