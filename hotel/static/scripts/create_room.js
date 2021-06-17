function onSubmitCreateRoomForm() {
    $("#create-room-btn").on("click", function () {
        let sendedData = {"csrfmiddlewaretoken": csrftoken,
                            "number":$("#number").val(),
                            "floor":$("#floor").val(),
                            "number_of_rooms":$("#number_of_rooms").val(),
                            "description":$("#description").val(),
                            "room_class":$("#room_class").val()}
        $(".alert.alert-danger").attr("hidden", "");
        $.ajax({
            url: HOST + "hotel-api/room-create/",
            method: "post",
            data:sendedData ,
            success: function (data) {
                 window.location.href = HOST + `hotel/room/${data.id}`;
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
    onSubmitCreateRoomForm();
}

$(document).ready(loadPage())