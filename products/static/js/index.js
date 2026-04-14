
$(document).ready(function (e) {

    let productsContainer = $(".products-index-container")
    const dataElement = document.getElementById("index-data")
    const secondElem = document.querySelector('#seconds');
    const minuteElem = document.querySelector('#minutes');
    const hourElem = document.querySelector('#hours');
    let urlAddToCart = dataElement.dataset["urlAddToCart"]
    let urlAddToFavourite = dataElement.dataset["urlAddToFavourite"]
    let csrfToken = $(".base-data").data("csrf-token")


    // Get initial values from Django context
    const initialHours = parseInt(dataElement.dataset.hours, 10) || 0;
    const initialMinutes = parseInt(dataElement.dataset.minutes, 10) || 0;
    const initialSeconds = parseInt(dataElement.dataset.secounds, 10) || 0;

    // Convert to total seconds
    let totalSeconds = initialHours * 3600 + initialMinutes * 60 + initialSeconds;

    function updateDisplay(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        hourElem.textContent = hours.toString().padStart(2, '0');
        minuteElem.textContent = minutes.toString().padStart(2, '0');
        secondElem.textContent = seconds.toString().padStart(2, '0');
    }

    function startTimer() {
        function updateTimer() {
            if (totalSeconds <= 0) {
                // Optionally reset or stop timer here
                clearInterval(timerInterval);
                return;
            }
            updateDisplay(totalSeconds);
            totalSeconds--;
        }
        updateTimer(); // Initial call
        var timerInterval = setInterval(updateTimer, 1000);
    }


    startTimer();

    productsContainer.on("click", function (e) {
        
        if (e.target.matches(".product-colors button") || e.target.matches(".product-colors button span")) {
            
            let siblings = [...e.target.closest(".product-colors").children]
            siblings.forEach(function (colorElement) {
                colorElement.setAttribute("data-active", "false")
                colorElement.classList.remove("ring-4", "ring-blue-400")
                colorElement.classList.add("ring-1", "ring-gray-400")
            });
            let isBtn = e.target.tagName === "BUTTON"
            if (isBtn) {
                e.target.classList.add("ring-4", "ring-blue-400")
                e.target.classList.remove("ring-1", "ring-gray-400")
                e.target.setAttribute("data-active", "true")
            } else {
                let tag = e.target.closest("button")
                tag.classList.add("ring-4", "ring-blue-400")
                tag.classList.remove("ring-1", "ring-gray-400")
                tag.setAttribute("data-active", "true")
            }
        } else {
            return;
        }
    });

    productsContainer.on("click", ".favourite-btn", function () {
        let productId = $(this).closest(".product-card").data("product-id");
        let button = $(this);
        $.ajax({
            type: "POST",
            url: urlAddToFavourite,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": productId },
            success: function (data) {
                if (data.is_authenticated) {
                    if (!data.error) {
                        if (data.in_favourite) {
                            button.addClass("text-blue-500")
                        }
                        else {
                            button.removeClass("text-blue-500")
                        }

                    } else {
                        fireAlert(text = "محصول در دیتابیس وجود ندارد", icon = 'error', title = "خطا!")
                    }
                } else {
                    fireAlert(text = "برای افزودن به علاقه مندی ها نیاز به ثبت نام/ورود دارید", icon = "info")
                }
            }
        });
    });

    productsContainer.on("click", ".add-to-cart-btn", function () {
        let button = $(this);
        let productCard = button.closest(".product-card")
        let product_id = productCard.data("product-id");
        let colorId = ""
        if (productCard.data("has-color-select")) {
            colorId = productCard.find(".color-select-btn[data-active='true']").data("color-id")
            
        }

        $.ajax({
            type: "POST",
            url: urlAddToCart,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": product_id, "color_id": colorId },
            success: function (data) {
                if (data.success) {
                    $(".cart-item-count").text(data.total_items)
                    $(".total-price-no-post").text(`${data.final_price} تومان`)
                    if (data.in_cart) {
                        button.addClass("text-blue-500");
                        $(".hidden-cart-items").append(data.html);
                        $(".item-count-text").text(`(${data.total_items} مورد)`)
                    } else {
                        if (data.unavailable) {
                            fireAlert(text = "محصول ناموجود است", icon = "error", title = "خطا!")
                            button.removeClass("text-blue-500");
                        } else {
                            button.removeClass("text-blue-500");
                            $(".mini-item-input-" + product_id).closest(".cart-item").remove();
                            $(".item-count-text").text(`(${data.total_items} مورد)`)
                        }
                    }
                } else {
                    fireAlert(text = "محصول در دیتابیس وجود ندارد", icon = "error", title = "خطا!")
                }


            }
        });
    });

});
