$(document).ready(function () {
    let postType = null;
    let csrfToken = $(".base-data").data("csrf-token")
    let pishtazPostTypeBtn = $(".pishtaz")
    let defaultPostTypeBtn = $(".manual")

    pishtazPostTypeBtn.on("click", function () {
        postType = "PSH";
        $(this).addClass("active")
        defaultPostTypeBtn.removeClass("active")
    });

    defaultPostTypeBtn.on("click", function () {
        postType = "MN"
        $(this).addClass("active")
        pishtazPostTypeBtn.removeClass("active")
    });

    $(".submit-order").on("click", function () {
        let button = $(this);
        let validData = true
        let formData = {};
        $(".order-form").serializeArray().forEach(function (item) {
            formData[item.name] = item.value;
            if (!item.value && !item.name=="des") {
                validData = false
            }
        });
        if (postType && validData) {
            $(".post-type-error").css("display", "none")
            $.ajax({
                type: "POST",
                url: "/orders/checkout-process/",
                data: JSON.stringify({
                    data: formData,
                    post_type: postType
                }),
                contentType: "application/json",
                headers: { "X-CSRFToken": csrfToken },
                success: function (data) {
                    if (data.error) {
                        fireAlert(text = "لطفا اطلاعات رو به درستی وارد کنید", icon = "info")
                    } if (!postType) {
                        $(".post-type-error").css("display", "inline-block")
                    } else {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url
                        } else {
                            return;
                        }
                    }
                }
            })
        } else {
            fireAlert(text = "لطفا اطلاعات رو به درستی وارد کنید", icon = "info")
            if (!postType) {
                $(".post-type-error").css("display", "inline-block")
            }
        }
    });
});
