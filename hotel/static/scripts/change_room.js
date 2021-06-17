function onSubmitChangeRoomForm() {
    $.ajax(
        {
            url:HOST + `hotel-api/rooms/${room_pk}`,
            method: "get",
            success: function (data) {
                 $("#number").val(data.number);
                 $("#floor").val(data.floor);
                 $("#number_of_rooms").val(data.number_of_rooms);
                 $("#description").val(data.description);
                 let options = $("#room_class option")
                options.each(function () {
                    if ($(this).text() == data.room_class) {
                        $(this).attr("selected", "");
                    }
                })
            },
        }
    )
    $("#change-room-btn").on("click", function () {
        let sendedData = {"number":$("#number").val(),
                           "floor":$("#floor").val(),
                           "number_of_rooms":$("#number_of_rooms").val(),
                           "description":$("#description").val(),
                           "room_class":$("#room_class").val()}
        $(".alert.alert-danger").attr("hidden", "");
        $.ajax({
            url: HOST + `hotel-api/rooms/${room_pk}`,
            method: "put",
            data:sendedData ,
            "headers": {'X-CSRFToken': csrftoken},
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
    onSubmitChangeRoomForm();
}

$(document).ready(loadPage())