function onSubmitReservationRoomForm() {
    $("#create-reservation-room-btn").on("click", function () {
        let sendedData = {"csrfmiddlewaretoken": csrftoken,
                            "started_at":$("#started_at").val(),
                            "ended_at":$("#ended_at").val(),
                            "room":room_pk}
        console.log(sendedData);
        $(".alert.alert-danger").attr("hidden", "");
        $.ajax({
            url: HOST + `hotel-api/create_reservation/`,
            method: "post",
            data: sendedData,
            success: function (data) {
                 window.location.href = HOST + `hotel/`;
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


function loadReservations() {
    if ($(".reservation-container").length){
        $.ajax({
            url: HOST + `hotel-api/room_reservations/${room_pk}`,
            method: "get",
            success: function (data) {
                 updateReservationList(data);
            },
        });
    }
}

function loadPage() {
    loadReservations();
    onSubmitReservationRoomForm();
}

$(document).ready(loadPage())