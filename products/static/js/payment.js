$(document).ready(function () {
    let dataTag = $(".payment-data")
    let urlOffCodeAjax = dataTag.data("off-code-ajax")
    let csrfToken = $(".base-data").data("csrf-token")

    let offPrice = $(".off-code-container")
    let offCodeContainer = $(".off-code-container")
    let offCodeContainerPre = $(".off-code-container-pre")
    let finalPrice = $(".final-price")

    let paymentMethodBtns = document.querySelectorAll(".payment-method")

    paymentMethodBtns.forEach(function(ele) {
        ele.addEventListener("click" , function(e) {
            paymentMethodBtns.forEach(function(ele) {
                ele.classList.remove("active")
            });
            ele.classList.add("active")
        });
    })

    $("#offCodeSubmitForm").on("submit", function (e) {
        e.preventDefault()
        let formEle = $(this)
        let offCode = formEle.find(".off-code-input").val()
        let offCodeError = formEle.find(".off-code-error")
        if (offCode) {
            offCodeError.css("display", "none")
            $.ajax({
                type: "POST",
                url: urlOffCodeAjax,
                data: { "off-code": offCode, "csrfmiddlewaretoken": csrfToken },
                success: function (data) {
                    if (data.success) {
                        if (data.off_type === "PRDC") {
                            if (!data.error_not_reached_limit) {
                                offCodeContainerPre.css("display", "none")
                                offCodeContainer.css("display", "flex")
                                offPrice.text(`${data.price_decreament} تومان`)
                                offCodeError.css("display", "none")
                                finalPrice.text(`${data.final_price} تومان`)
                            } else {
                                offCodeError.text("مقدار خرید کمتر از سقف تعیین شده است")
                                offCodeError.css("display", "inline")
                            }
                        } if (data.off_type === "FRSE") {
                            $(".send-price-list-item p.value").html("رایگان")
                        }
                    } else {
                        if (data.error_off_code_none || data.error_invalid_code) {
                            offCodeError.text("کد تخفیف نامعتبر است!")
                            offCodeError.css("display", "inline")
                        }
                    }
                }
            });
        } else {
            offCodeError.text("لطفا کد تخفیف را وارد کنید!")
            offCodeError.css("display", "inline")
        }
    });
});

