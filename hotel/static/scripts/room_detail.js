function loadRoomDetail() {
    let roomBlock = $(".room-container");
    if (roomBlock.length) {
        $.ajax({
            url: HOST + `hotel-api/rooms/${room_pk}`,
            method: "get",
            success: function (data) {
                 $("span.room-number").text(data.number);
                 $("span.room-floor").text(data.floor);
                 $("span.room-number_of_rooms").text(data.number_of_rooms);
                 $("span.room-room_class").text(data.room_class);
                 $("span.room-description").text(data.description);
                 updateReservationList(data.booked);
            }
        });
    }
}

function loadPage() {
    loadRoomDetail();
}

$(document).ready(loadPage())

