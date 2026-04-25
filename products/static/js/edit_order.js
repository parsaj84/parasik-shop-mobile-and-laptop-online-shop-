$(document).ready(function () {
    let dataTag = $(".edit-order-data")
    let urlOrderEditAjax = dataTag.data("url-order-edit-ajax")
    let urlRefrallRequestForm = dataTag.data("url-refrall-request-form")
    let urlRefrallRequestProcess = dataTag.data("url-refrall-request-process")
    let orderID = dataTag.data("order-id")
    let csrfToken = $(".base-data").data("csrf-token")

    $(".submit-order-edit").on("click", function () {
        let form = $(".edit-order-form")
        let serializedArrayData = form.serializeArray()
        let validData = true
        let data = {}
        const phonePattern = /^09\d{9}$/;
        const postalCodeRegex = /^\d{10}$/;
        serializedArrayData.forEach(function (ele) {
            if (ele.name !== "des" && !ele.value) {
                validData = false
            } if (ele.name === "phone" && !phonePattern.test(ele.value)) {
                validData = false
            } if (ele.name === "postal_code" && !postalCodeRegex.test(ele.value)) {
                validData = false
            }
            data[ele.name] = ele.value
        });
        data["csrfmiddlewaretoken"] = csrfToken
        data["order_id"] = orderID
        if (validData) {
            $.ajax({
                url: urlOrderEditAjax,
                method: "POST",
                data: data,
                success: function (data) {
                    if (data.success) {
                        if (data.delivery_error) {
                            fireAlert(text = "سفارش در مرحله ارسال قرار داشته و دیگر امکان ویرایش در اطلاعات وجود ندارد", icon = 'info')
                        } else if (data.error_invalid_information) {
                            fireAlert(text = "لطفا اطلاعات رو بدرستی وارد کنید!", icon = 'info', title = "اطلاعات نامعتبر")
                        }
                        else {
                            fireAlert(text = "اطلاعات سفارش با موفقیت ویرایش شد!", icon = 'success', title = "ویرایش شد")
                        }
                    } else if (data.error) {
                        fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطایی!")
                    }
                }
            });
        } else {
            fireAlert(text = "لطفا اطلاعات رو بدرستی وارد کنید!", icon = "info", title = "اطلاعات نامعتبر");
        }
    });

    let refrallOverlay = $(".refrall-item-form-overlay")
    refrallOverlay.on("click", ".close-refrall-modal", function (e) {
        let btn = $(this)
        btn.closest(".refrall-modal-dialog").remove()
        refrallOverlay.removeClass("active")
    });



    refrallOverlay.on("click", "#itemRefrallImageEntry", function (e) {
        let input = $(this).find("input[type=file]")
        input[0].click()
    });

    refrallOverlay.on("submit", ".refrall-item-form", function (e) {
        e.preventDefault()
        let sizeLimit = 2 * 1024 * 1024
        let formEle = $(this)
        let itemId = formEle.closest(".refrall-modal-dialog").data("item-id")
        let form = new FormData(formEle[0])
        let errorNoImage = formEle.find(".error-no-image")
        let errorNoreason = formEle.find(".error.reason")
        let errorImageSize = formEle.find(".error-image-size")
        let validData = true
        form.entries().forEach(function (ele) {
            if (ele[0] === "resoen" && !ele[1]) {
                errorNoreason.text("مقدار این فیلد اجباری است")
                validData = false
            } if (ele[0] === "item_img") {
                if (!ele[1].size) {
                    if (errorNoImage.hasClass("hidden")) {
                        errorNoImage.removeClass("hidden")
                        validData = false
                    }
                } else if (!ele[1].size >= sizeLimit) {
                    errorImageSize.removeClass("hidden")
                    validData = false
                }
            }
        });
        form.append("csrfmiddlewaretoken", csrfToken)
        form.append("item_id", itemId)
        if (validData) {
            errorNoImage.addClass("hidden")
            errorImageSize.addClass("hidden")
            errorNoreason.text("")
            $.ajax({
                url: urlRefrallRequestForm,
                method: "POST",
                data: form,
                processData: false,
                contentType: false,
                
                success: function (data) {
                    if (data.success) {
                        if (!data.can_refrall) {
                            fireAlert(text = "امکان مورجوعی روی این سفارش وجود ندارد(از زمان تحویل به پست بیش از ده روز گذشته است)", icon = "info", title = "عدم امکان مرجوعی")
                        } else if (data.refrall_reqeust_exists) {
                            fireAlert(text = "درخواست مرجوعی قبلا روی این ایتم ثبت شده!", icon = 'info', title = "درخواست مرجوعی قبلا ثبت شده!")
                        } else {
                            fireAlert(text = "درخواست مرجوعی برای شما ثبت شد و نتیجه پس از بررسی اعلام خواهد شد!", icon = 'success', title = "ثبت شد!")
                            refrallOverlay.removeClass("active")
                            formEle.closest(".refrall-modal-dialog").remove()
                        }
                    } else if (data.error) {
                        fireAlert(text = "خطایی رخ داد!", icon = "error", title = "خطایی!")
                    }
                }
            });
        }
    });

    function processFIle(file) {
        return new Promise(function (resolve, reject) {
            let filereader = new FileReader()
            try {
                filereader.addEventListener("load", function () {
                    resolve(this.result)
                });
            } catch (error) {
                reject("خطا در پردازش تصویر")
            }
            filereader.readAsDataURL(file)
        });
    }

    refrallOverlay.on("input", "#itemRefrallImageEntry input[type=file]", async function (e) {
        let enteredImageSection = $(this).parent().find(".entered-item-image")
        let imageSizeError = $(this).parent().find(".error-image-size")
        let processError = $(this).parent().find(".error-process")
        let file = e.currentTarget.files[0]
        let sizeLimit = 2 * 1024 * 1024
        if (file.size <= sizeLimit) {
            if (!imageSizeError.hasClass("hidden")) {
                imageSizeError.addClass("hidden")
            }
            try {
                let reuslt = await processFIle(file)
                if (!processError.hasClass("hidden")) {
                    processError.addClass("hidden")
                }
                let imageTag = document.createElement("img")
                imageTag.setAttribute("src",reuslt)
                enteredImageSection.html(imageTag)
            } catch (error) {
                if (processError.hasClass("hidden")) {
                    processError.removeClass("hidden")
                }
            }

        } else {
            if (imageSizeError.hasClass("hidden")) {
                imageSizeError.removeClass("hidden")
            }
        }
    });

    $(".refrall-req-btn").on("click", function (e) {
        let btn = $(this)
        let itemId = btn.data("item-id")
        $.ajax({
            url: urlRefrallRequestProcess,
            method: "POST",
            data: {
                "csrfmiddlewaretoken": csrfToken,
                "item_id": itemId,
            },
            success: function (data) {
                if (data.success) {
                    if (data.refrall_before_send) {
                        if (data.deleted_order) {
                            location.pathname = data.redirect_url
                        } else {
                            fireAlert(text = "کالای موردنظر مرجوع شد و هزینه ان به شما عودت خواهد شد", icon = 'success', title = "مرجوع شد!")
                            btn.closest(".product-item").remove()
                            $("#item-total-price").text(data.items_new_price)
                            $("#order-total-price").text(`${data.order_new_price} تومان`)
                        }

                    } else if (data.refrall_after_send) {
                        if (data.can_refrall) {
                            refrallOverlay.html(data.html)
                            refrallOverlay.addClass("active")
                        } else {
                            fireAlert(text = "امکان مرجوعی روی کالای مورد نظر وجود ندارد!", icon = 'info', title = "عدم امکان مرجوعی")
                        }
                    }
                } else if (data.error) {
                    fireAlert(text = "خطایی رخ داد!", icon = "error", title = "خطایی!")
                }
            }
        });
    });


});