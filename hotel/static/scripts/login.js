function onSubmitLogin() {
    $("#login-btn").on("click", function () {
        let sendedData = {"csrfmiddlewaretoken": csrftoken,
                            "username":$("#login").val(),
                            "password":$("#pwd").val(),}
        $.ajax({
            url: HOST + "hotel-api/login/",
            method: "post",
            data:sendedData ,
            success: function () {
                 window.location.href = HOST + `hotel/`;
            },
        });
	});
}

$(document).ready(onSubmitLogin());