
$(document).ready(function () {
    const form = document.getElementById('otp-form')
    const secoundForm = document.getElementById("otp-form-1")
    if (!form) return

    const inputs = secoundForm ? [...form.querySelectorAll('input[type=text]'), ...secoundForm.querySelectorAll("input[type=text")] : [...form.querySelectorAll('input[type=text]')]
    const submit = form.querySelector('button[type=submit]')

    const handleKeyDown = (e) => {
        if (
            !/^[0-9]{1}$/.test(e.key)
            && e.key !== 'Backspace'
            && e.key !== 'Delete'
            && e.key !== 'Tab'
            && !e.metaKey
        ) {
            e.preventDefault()
        }

        if (e.key === 'Delete' || e.key === 'Backspace') {
            const index = inputs.indexOf(e.target);
            if (index > 0) {
                inputs[index - 1].value = '';
                inputs[index - 1].focus();
            }
        }
    }

    const handleInput = (e) => {
        const { target } = e
        const index = inputs.indexOf(target)
        if (target.value) {
            if (index < inputs.length - 1) {
                inputs[index + 1].focus()
            } else {
                submit.focus()
            }
        }
    }

    const handleFocus = (e) => {
        e.target.select()
    }

    const handlePaste = (e) => {
        e.preventDefault()
        const text = e.clipboardData.getData('text')
        if (!new RegExp(`^[0-9]{${inputs.length}}$`).test(text)) {
            return
        }
        const digits = text.split('')
        inputs.forEach((input, index) => input.value = digits[index])
        submit.focus()
    }

    inputs.forEach((input) => {
        input.addEventListener('input', handleInput)
        input.addEventListener('keydown', handleKeyDown)
        input.addEventListener('focus', handleFocus)
        input.addEventListener('paste', handlePaste)
    })
    let interval = null
    function setTime(eleSelector, secounds) {
        let timerElement = document.querySelector(eleSelector)
        timerElement.parentElement.style.display = "flex"
        timerElement.parentElement.nextElementSibling.style.display = "none"
        clearInterval(interval)
        interval = setInterval(function () {
            if (secounds > 0) {
                let minutes = Math.floor(secounds / 60)
                let secoundCal = Math.floor(secounds % 60)
                let minuteString = minutes >= 1 ? `0${minutes}` : "00"
                let secoundsString = secoundCal >= 10 ? `${secoundCal}` : `0${secoundCal}`
                secounds -= 1
                timerElement.innerText = `${minuteString}:${secoundsString}`
            } else {
                clearInterval(interval)
                timerElement.parentElement.style.display = "none"
                timerElement.parentElement.nextElementSibling.style.display = "flex"
            }
        }, 1000)
    }

    function validateInput(value) {
        const phonePattern = /^09\d{9}$/;
        if (!value) {
            return "این فیلد نمی‌تواند خالی باشد";
        } else if (!phonePattern.test(value)) {
            return "لطفا شماره موبایل معتبر وارد کنید";
        }
        return false;
    }

    let editModal = $(".edit-modal")
    let phoneEntries = editModal.find(".phone-entry")

    let dataTag = $(".dashboard-account-data")
    let urlPasswordEditAjax = dataTag.data("url-password-edit-ajax")
    let urlGenerateValidationCode = dataTag.data("url-generate-validation-code")
    let urlEditPhonePhoneEntry = dataTag.data("url-edit-phone-phone-entry")
    let urlEditPhoneValidationPrevious = dataTag.data("edit-phone-validation-previous")
    let urlEditPhoneNewPhoneValidation = dataTag.data("edit-phone-new-phone-validation")
    let urlCitySetAjax = dataTag.data("city-set-ajax")
    let csrfToken = $(".base-data").data("csrf-token")
    

    let editLevelPhoneEntry = $(".edit-level.edit-phone-entry")
    let editLevelPhoneEntryForm = editLevelPhoneEntry.find("form")
    let editLevelPhoneEntryInput = editLevelPhoneEntry.find("input[type=text]")
    let editLevelPhoneEntrySubmitBtn = editLevelPhoneEntry.find("button[type=submit]")
    let editErrorPhoneEntry = editLevelPhoneEntry.find(".text-error.active")

    let editLevelValidationCode = editModal.find(".edit-level.previous-phone-validation")
    let editLevelValidationCodeInput = editLevelValidationCode.find("input[type=text]")
    let editLevelValidationCodeForm = editLevelValidationCode.find("form")
    let editLevelValidationCodeError = editLevelValidationCode.find(".text-error.active")

    let editLevelNewPhoneValidataion = $(".edit-level.new-phone-validation")
    let newPhoneSpan = editLevelNewPhoneValidataion.find(".new-phone")
    let editLevelNewPhoneValidataionInput = editLevelNewPhoneValidataion.find("input[type=text]")
    let editLevelNewPhoneValidataionError = editLevelNewPhoneValidataion.find(".text-error.active")
    let editLevelNewPhoneValidataionForm = editLevelNewPhoneValidataion.find("form")

    let editLevelPasswordChange = $(".edit-level.edit-password")
    let editLevelPasswordChangeForm = editLevelPasswordChange.find("form")
    let editLevelPasswordChangeInput = editLevelPasswordChange.find("input")
    let editLevelPasswordChangeErrorNew = editLevelPasswordChange.find(".text-error.active.new-password")
    let editLevelPasswordChangeErrorPre = editLevelPasswordChange.find(".text-error.active.previous-password")
    let passwordBar = editLevelPasswordChange.find(".password-bar")

    let generateCode = editModal.find(".resend-code")

    $(".change-pass-btn").on("click", function (e) {
        e.preventDefault()
        editModal.addClass("active")
        editLevelPasswordChange.addClass("active")
    });

    editLevelPasswordChangeForm.on("submit", function (e) {
        e.preventDefault();
        let form = $(this);
        let serializedArrayData = form.serializeArray()
        let data = {}
        let validData = true
        let newPasswordConfirmError = form.find(".text-error.active.new-password-confirm")

        serializedArrayData.forEach(function (ele) {
            let errorTag = form.find(`.text-error.active.${ele.name}`)
            data[ele.name] = ele.value
            if (!ele.value) {
                validData = false
                errorTag.text("این فیلد اجباری است")
            }
        })
        if (data["new-password"] !== data["new-password-confirm"]) {
            validData = false
            newPasswordConfirmError.text("تایید رمز عبور و رمز عبور جدید باید یکسان باشد")
        }
        data["csrfmiddlewaretoken"] = csrfToken
        
        if (validData) {
            $.ajax({
                url: urlPasswordEditAjax,
                method: "POST",
                data: data,
                success: function (data) {
                    if (data.success) {
                        if (data.invalid_previous_password) {
                            form.find(".text-error.active.previous-password").text("رمز فعلی اشتباه است.")
                        } else if (data.invalid_password_confirm) {
                            newPasswordConfirmError.text("تایید رمز عبور باید با رمز عبور جدید یکسان باشد")
                        } else {
                            form.find(".text-error.active").text("")
                            editLevelPasswordChangeInput.val("")
                            editModal.removeClass("active")
                            editLevelPasswordChange.removeClass("active")
                            passwordBar.toggleClass("bg-green-500", "bg-gray-400")
                            form.find(".submit-btn").addClass("submit-btn-invisable")
                        }
                    } else if (data.error) {
                        fireAlert(text = "خطا!", icon = "error", title = "خطا")
                    }
                }
            });
        };
    });



    $(".change-phone-btn").on("click", function (e) {
        editModal.addClass("active")
        editLevelPhoneEntry.addClass("active")
    })


    editLevelPhoneEntryInput.on("input", function (e) {
        let entry = $(this).val()
        let valdiationResult = validateInput(entry)
        if (valdiationResult) {
            editErrorPhoneEntry.text(valdiationResult)
            if (!editLevelPhoneEntry.find("button").hasClass("submit-btn-invisable")) {
                editLevelPhoneEntry.find("button").addClass("submit-btn-invisable")
            }
        } else {
            editLevelPhoneEntry.find("button").removeClass("submit-btn-invisable")
            editErrorPhoneEntry.text("")
        }
    });

    generateCode.on("click", function (e) {
        let btn = $(this)
        let timerTag = btn.prev(".login-timer_text")
        
        $.ajax({
            url: urlGenerateValidationCode,
            method: "GET",
            success: function (data) {
                if (data.success) {
                    setTime(`#${timerTag[0].querySelector(".login-timer").getAttribute("id")}`, 120)
                } else {
                    alert("error")
                }
            }
        });
    });

    editLevelPhoneEntryForm.on("submit", function (e) {
        e.preventDefault()
        let entry = editLevelPhoneEntryInput.val()
        $.ajax({
            url: urlEditPhonePhoneEntry,
            method: "POST",
            data: { "phone": entry, "csrfmiddlewaretoken": csrfToken },
            success: function (data) {
                if (data.success) {
                    editErrorPhoneEntry.removeClass("active");
                    editLevelPhoneEntryInput.val("");
                    editErrorPhoneEntry.text("");
                    editLevelPhoneEntry.removeClass("active")
                    editLevelValidationCode.addClass("active");
                    setTime(".previous-phone-validation-timer", 120)
                } else if (data.error) {
                    editErrorPhoneEntry.text(data.error);
                    editErrorPhoneEntry.addClass("active")
                }
            }
        });
    });

    editModal.on("click", function (e) {
        let modal = $(this)
        let modalEle = $(this)[0]
        let trigger = e.target
        if (trigger == modalEle) {
            clearInterval(interval)
            let activeModal = modal.find(".edit-level.active")
            let activeModalInput = activeModal.hasClass("edit-password") ? activeModal.find("input[type=text],input[type=password]") : activeModal.find("input[type=text]")
            let activeModalError = activeModal.find(".text-error.active")
            if (activeModal.hasClass("edit-password")) {
                passwordBar.each(function (index, ele) {
                    if (ele.classList.contains("bg-green-500")) {
                        ele.classList.replace("bg-green-500", "bg-gray-300")
                    } if (ele.classList.contains("bg-red-500")) {
                        ele.classList.replace("bg-red-500", "bg-gray-300")
                    } else if (ele.classList.contains("bg-amber-400")) {
                        ele.classList.replace("bg-amber-400", "bg-gray-300")
                    }
                    activeModal.find(".password-validation-info").css("display", "none")
                });
                activeModal.find(".submit-btn").addClass("submit-btn-invisable")
            }
            if (activeModal.hasClass("edit-phone-entry")) {
                activeModal.find(".submit-btn").addClass("submit-btn-invisable")
            }
            activeModal.removeClass("active")
            activeModalInput.val("")
            activeModalError.text("")
            modal.removeClass("active")
        }
    });


    editLevelValidationCodeForm.on("submit", function (e) {
        e.preventDefault()
        let entry = []
        editLevelValidationCodeInput.each(function (index, elem) {
            entry.push(elem.value)
        });
        entry.filter(function (digit) {
            return digit !== ""
        });
        if (entry.length == 5) {
            $.ajax({
                url: urlEditPhoneValidationPrevious,
                method: "POST",
                data: { "validation_code": entry.join(""), "csrfmiddlewaretoken": csrfToken },
                success: function (data) {
                    if (data.success) {
                        editLevelValidationCode.removeClass("active")
                        editLevelValidationCodeInput.val("")
                        editLevelValidationCodeError.text("")
                        editLevelNewPhoneValidataion.addClass("active")
                        newPhoneSpan.text(data.phone)
                        setTime(".new-phone-validation-timer", 120)
                    } else {
                        editLevelValidationCodeError.text(data.error)
                    }
                }
            })
        } else {
            editLevelValidationCodeError.text("لطفا کد تایید را کامل وارد کنید")
        }
    });
    editLevelNewPhoneValidataionForm.on("submit", function (e) {
        e.preventDefault()
        let entry = []
        editLevelNewPhoneValidataionInput.each(function (index, elem) {
            entry.push(elem.value)
        })
        entry.filter(function (digit) {
            return digit !== ""
        });
        if (entry.length === 5) {
            $.ajax({
                url: urlEditPhoneNewPhoneValidation,
                data: { "validation_code": entry.join(""), "csrfmiddlewaretoken": csrfToken },
                method: "POST",
                success: function (data) {
                    if (data.success) {
                        editLevelNewPhoneValidataion.removeClass("active")
                        editLevelNewPhoneValidataionInput.val("")
                        editLevelNewPhoneValidataionError.text("")
                        $(".phone-edit-show").text(data.phone)
                        $(".previous-phone").text(data.phone)
                        editModal.removeClass("active")
                    } else if (data.error) {
                        editLevelNewPhoneValidataionError.text("")
                    }
                }
            })
        } else {
            editLevelNewPhoneValidataionError.text("لطفا کد تایید را کامل وارد کنید.")
        }
    })


    $(".province-select").on("input", function () {
        let optionVlue = $(this).val();
        $.ajax({
            type: "POST",
            url: urlCitySetAjax,
            data: { "csrfmiddlewaretoken": csrfToken, "province": optionVlue },
            dataType: "html",
            success: function (data) {
                $(".city-options").html(data)
            }
        });


    });
});