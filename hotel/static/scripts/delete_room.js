function onSubmitDeleteRoomForm() {
    $("#delete-room-btn").on("click", function () {
        $.ajax({
            url: HOST + `hotel-api/rooms/${room_pk}`,
            method: "delete",
            "headers": {'X-CSRFToken': csrftoken},
            success: function (data) {
                 window.location.href = HOST + `hotel/`;
            },
        });
	});
}


function loadPage() {
    onSubmitDeleteRoomForm();
}

$(document).ready(loadPage())