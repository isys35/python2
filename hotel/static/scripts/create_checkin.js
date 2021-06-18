
function loadReservationForCheckIn() {
    $.ajax({
            url: HOST + `hotel-api/room_reservations/${room_pk}`,
            method: "get",
            success: function (data) {
                 for (let i=0; i<data.length; i++) {
                        let innerHTML = `<p>Бронь пользователя ${data[i].user} с ${data[i].started_at} по ${data[i].ended_at}  <a href=\"#username\" class=\"btn btn-success\" onclick="useReservation('${data[i].user}', '${data[i].started_at}', '${data[i].ended_at}')">Исп. бронь</a></p>`
                        $(".check-in-reservations-list").append(innerHTML);
                    }
            },

    });
    let date = new Date();
    $("#started_at").val(date.toISOString().split(".")[0]);
}

function useReservation(username, started_at, ended_at) {
    let startedAt = reformatDateTime(started_at);
    let endedAt = reformatDateTime(ended_at);
    $("#username").val(username);
    $("#started_at").val(startedAt);
    $("#ended_at").val(endedAt);
}


function reformatDateTime(initDatetime) {
    let splitedDateTime = initDatetime.split(" ");
    let date = splitedDateTime[0];
    let time = splitedDateTime[1];
    let splitedDate = date.split(".");
    let splitedTime = time.split(":");
    let day = splitedDate[0];
    let month = splitedDate[1];
    let year = splitedDate[2];
    let hour = splitedTime[0];
    let minute = splitedTime[1];
    return `${year}-${month}-${day}T${hour}:${minute}:00.000`
}


function onSubmitCheckIn() {
    $("#create-checkin-room-btn").on("click", function () {
        let sendedData = {"csrfmiddlewaretoken": csrftoken,
                          "username":$("#username").val(),
                          "started_at":$("#started_at").val(),
                          "ended_at":$("#ended_at").val(),
                           "room": room_pk}
        $(".alert.alert-danger").attr("hidden", "");
        $.ajax({
            url: HOST + "hotel-api/create_checkin/",
            method: "post",
            data:sendedData ,
            success: function (data) {
                 window.location.href = HOST + `hotel/room/${room_pk}`;
            },
            error: function (data) {
                $.each(data.responseJSON, function( k, v ) {
                    let id_el = "#error_" + k;
                    $(id_el).removeAttr("hidden");
                    $(id_el).text(v);
                });
            }
        });
	});
}


function loadPage() {
    loadReservationForCheckIn();
    onSubmitCheckIn();
}

$(document).ready(loadPage());