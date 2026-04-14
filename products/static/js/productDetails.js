

// COLOR SELCET
const colorButtons = document.querySelectorAll(".color-select-btn");
const colorTitle = document.querySelector(".color-title");
const dataElement = document.querySelector(".product-details-data")

colorButtons?.forEach((button) => {
    button.addEventListener("click", () => {
        colorButtons.forEach((btn) => {
            btn.classList.remove("ring-4", "ring-blue-400");
            btn.classList.add("ring-1", "ring-gray-400");
            btn.setAttribute("data-active", "falseذ")

        });

        button.classList.remove("ring-1", "ring-gray-400");
        button.classList.add("ring-4", "ring-blue-400");
        button.setAttribute("data-active", "true")
        const span = button.querySelector("span");
        const classList = span.classList;
        const colorClass = Array.from(classList).find(c => c.startsWith("bg-"));

        const colorMap = JSON.parse(dataElement.dataset.colorsMap)
        // const colorMap = {
        //     "bg-black": "مشکی",
        //     "bg-white": "سفید",
        //     "bg-green-400": "سبز",
        //     "bg-blue-500": "آبی"
        // };

        const colorName = colorMap[colorClass] || "نامشخص";
        colorTitle.textContent = `رنگ : ${colorName}`;
    });
});



// TEXT SLIDER 
// document.addEventListener("DOMContentLoaded", () => {
//     const texts = [
//         { text: "🔥 ۱۰۰۰+ فروش در هفته گذشته", color: "text-red-500" },
//         { text: "💯 ۵۰۰+ نفر بیش از ۲ بار این کالا را خریده‌اند", color: "text-green-600" },
//         { text: "🛒 در سبد خرید ۱۰۰۰+ نفر", color: "text-blue-600" }
//     ];

//     let index = 0;
//     const slider = document.getElementById("slider-text");

//     setInterval(() => {
//         index = (index + 1) % texts.length;
//         slider.classList.add("opacity-0");

//         setTimeout(() => {
//             slider.innerHTML = `<p class="${texts[index].color}">${texts[index].text}</p>`;
//             slider.classList.remove("opacity-0");
//         }, 300);
//     }, 3000);
// });



// CHANGE TAB 
document.addEventListener("DOMContentLoaded", () => {
    const buttonsTab = document.querySelectorAll(".tab-btn");
    const contents = document.querySelectorAll(".tab-content");

    buttonsTab.forEach((btn) => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-target");

            buttonsTab.forEach((b) => {
                b.classList.remove("text-blue-500");
                b.classList.add("text-gray-500", "dark:text-gray-300");
            });
            btn.classList.remove("text-gray-500", "dark:text-gray-300");
            btn.classList.add("text-blue-500");

            contents.forEach((content) => {
                if (content.classList.contains(target)) {
                    content.classList.remove("hidden");
                    content.classList.add("block");
                } else {
                    content.classList.remove("block");
                    content.classList.add("hidden");
                }
            });
        });
    });
});

let moreDesBtn = document.getElementById("more-des")
let productDescription = document.querySelector(".product-description")
let linearBlur = document.querySelector(".linear-blur")

moreDesBtn.addEventListener("click", function (e) {
    let act = e.target.dataset.act
    if (act === "extend") {
        productDescription.style.maxHeight = "100%"
        moreDesBtn.setAttribute("data-act", "jam")
        moreDesBtn.innerText = "جمع کردن"
        linearBlur.style.display = "none"
    } else {
        productDescription.style.maxHeight = "75px"
        moreDesBtn.setAttribute("data-act", "extend")
        moreDesBtn.innerText = "مشاهده بیشتر"
        linearBlur.style.display = "inline-block"
    }
})




// SHOW MORE COMMENTS
const moreCommentBtn = document.querySelector('.more-comment-btn');
const moreCommentText = document.querySelector('.more-comment-text');
const moreCommentIcon = document.querySelector('.more-comment-icon');
const hiddenCommentItems = document.querySelectorAll('.hidden-comment-item');

if (moreCommentBtn) {
    moreCommentBtn.addEventListener('click', () => {
        hiddenCommentItems.forEach(item => {
            item.classList.toggle('hidden');
            item.classList.toggle('block');
        });

        if (moreCommentText.innerHTML === 'مشاهده بیشتر') {
            moreCommentText.innerHTML = 'مشاهده کمتر';
        } else {
            moreCommentText.innerHTML = 'مشاهده بیشتر';
        }

        moreCommentIcon.classList.toggle('rotate-180');
    });
}




// PRODUCT SLIDER

const openSliderModals = document.querySelectorAll('.open-sliderModal')
const sliderModal = document.querySelector('.slider-modal')
const overlayProductPage = document.querySelector('.overlay')
const closeSliderModal = document.querySelector('.close-sliderModal')

openSliderModals.forEach(el => {
    el.addEventListener('click', () => {
        sliderModal.classList.add('active')
        overlayProductPage.classList.add('active')
    })
})

overlayProductPage.addEventListener('click', () => {
    overlayProductPage.classList.remove('active')
    sliderModal.classList.remove('active')
})

closeSliderModal.addEventListener('click', () => {
    sliderModal.classList.remove('active')
    overlayProductPage.classList.remove('active')
})


// sliders 
document.addEventListener('DOMContentLoaded', function () {
    // Product details slider
    let detailsSwiper = new Swiper('.ProductDetailsSlider', {
        slidesPerView: 1,
        spaceBetween: 20,
        navigation: {
            nextEl: '.button-next-ProductDetailsSlider',
            prevEl: '.button-prev-ProductDetailsSlider',
        },
        rtl: true,
    });

    // Related products slider (BestSelling)
    let bestSellingSwiper = new Swiper('.BestSelling', {
        // slidesPerView: 4, // Adjust as needed
        spaceBetween: 20,
        navigation: {
            nextEl: '.BestSelling-next-slide',
            prevEl: '.BestSelling-prev-slide',
        },
        rtl: true,
        breakpoints: {
            640: { slidesPerView: 2 },
            1000: { slidesPerView: 3 },
            1280: { slidesPerView: 4 },
        }
    });
});

// ajax requests
$(document).ready(function () {
    const cartContainer = $(".cart-container")
    let hiddenMinCartBar = cartContainer.find(".hidden-min-cart-bar")
    let removeFromCartBtn = cartContainer.find("#remove-from-cart-btn")
    let dataTag = $(".product-details-data")
    let addToCartList = dataTag.data("add-to-cart-list")
    let productId = dataTag.data("product-id")
    let urlDataAddToCart = dataTag.data("url-add-to-cart-detail")
    let urlCartIncrease = dataTag.data("url-cart-increase")
    let urlCartDecrease = dataTag.data("url-cart-decrease")
    let urlUserOponionSubmit = dataTag.data("url-user-oponion-submit")
    let csrfToken = $(".base-data").data("csrf-token")
    let urlRemoveFromCart = dataTag.data("remove-from-cart")
    let productName = dataTag.data("product-name")
    let urlAddToFavourite = dataTag.data("add-to-favourite")
    let commentSubmit = dataTag.data("url-comment-submit")
    let productDes = dataTag.data("product-des")


    $(".add-to-cart-btn").on("click", function () {
        let button = $(this);
        let itemId = button.closest(".product-card").data("product-id");

        $.ajax({
            type: "POST",
            url: addToCartList,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": itemId },
            success: function (data) {
                $(".cart-item-count").text(data.total_items)
                $(".item-count-text").text(`(${data.total_items} مورد)`)
                if (data.in_cart) {
                    button.addClass("text-blue-500");
                    $(".hidden-cart-items").append(data.html);
                } else {
                    if (data.unavailable) {
                        fireAlert(text = "محصول ناموجود است!", icon = "error", title = "خطا")
                        button.removeClass("text-blue-500");
                    } else {
                        button.removeClass("text-blue-500");
                        $(".mini-item-input-" + productId).closest(".cart-item").remove();
                    }
                }

            }
        });
    });

    cartContainer.on("click", ".increase-btn", function () {
        let button = $(this);
        let itemID = button.closest(".product-id-container").data("product-id");
        $.ajax({
            type: "POST",
            url: urlCartIncrease,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": itemID },
            success: function (data) {
                if (data.success) {
                    if (!data.unavailable) {
                        cartContainer.find(".custom-input-detail").attr("value", data.item_quantity);
                        $(".mini-item-input-" + productId).attr("value", data.item_quantity)
                        cartContainer.find(".total-price .total_price_cart").text(`${data.item_total_price} تومان`);
                        // $(".mini-item-input-" + "{{product.pk}}").closest(".hidden-item-total-price").text(`${data.item_total_price} تومان`);
                        $(".hidden-itm-cart-t-p-" + itemID).text(data.item_total_price);
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                    } else {
                        fireAlert(text = "موجودی محصول به خارج از درخواست شماست!", icon = "info", title = "اتمام موجودی!")
                    }
                } else {
                    fireAlert(text = "خطایی هنگام اضافه کردن محصول رخ داد!", icon = "error", title = "خطا!")
                }
            }
        });
    });

    cartContainer.on("click", ".decrement", function () {
        let button = $(this);
        let itemID = $(this).closest(".product-id-container").data("product-id");

        $.ajax({
            type: "POST",
            url: urlCartDecrease,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": itemID },
            success: function (data) {
                if (data.success) {
                    if (!data.out_off_cart) {
                        cartContainer.find(".custom-input-detail").attr("value", data.item_quantity);
                        $(".mini-item-input-" + productId).attr("value", data.item_quantity)
                        cartContainer.find(".total-price .total_price_cart").text(`${data.item_total_price} تومان`);
                        // $(".mini-item-input-" + "{{product.pk}}").closest(".hidden-item-total-price").text(`${data.item_total_price} تومان`);
                        $(".hidden-item-total-price-" + productId).text(`${data.item_total_price} تومان`);
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                    } else {

                        $(".mini-item-input-" + productId).closest(".cart-item").remove()
                        $(".cart-item-count").text(data.total_items);

                        removeFromCartBtn.find("span").text("افزودن به سبد خرید");
                        cartContainer.find(".hidden-min-cart-bar").css("display", "none");
                        removeFromCartBtn.attr("id", "add-to-cart-btn");
                        removeFromCartBtn.removeClass("remove-from-cart-btn").addClass("add-to-cart-btn");
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                        $(".item-count-text").text(`(${data.total_items} مورد)`)
                    }
                } else {
                    const isDarkMode = $("html").hasClass('dark');
                    const alertOptions = {
                        background: isDarkMode ? 'oklch(0.21 0.034 264.665)' : '#fff',
                        color: isDarkMode ? 'oklch(0.985 0.002 247.839)' : 'oklch(0.13 0.028 261.692)',
                        confirmButtonColor: isDarkMode ? 'oklch(0.488 0.243 264.376)' : 'oklch(0.623 0.214 259.815)',
                        cancelButtonColor: isDarkMode ? '#f44336' : '#d33',
                    };
                    Swal.fire({
                        title: "خطا!",
                        text: "خطایی رخ داد!",
                        icon: 'error',
                        confirmButtonText: 'باشه',
                        showCancelButton: false,
                        cancelButtonText: 'لغو',
                        background: alertOptions.background,
                        color: alertOptions.color,
                        confirmButtonColor: alertOptions.confirmButtonColor,
                        cancelButtonColor: alertOptions.cancelButtonColor
                    });
                }
            }
        });
    });

    $(".user-oponion").on("click", ".user-oponion-usefull", function (e) {
        let btn = $(this)
        let commentId = btn.closest(".user-oponion").data("comment-id");
        $.ajax({
            url: urlUserOponionSubmit,
            method: "POST",
            data: { "csrfmiddlewaretoken": csrfToken, "comment_id": commentId, "is_usefull": true },
            success: function (data) {
                if (data.success) {
                    if (data.is_authenticated) {
                        btn.find("span").text(data.yes_count)
                        btn.parent().find(".user-oponion-notusefull span").text(data.no_count)
                    } else {
                        fireAlert(text = "برای ثبت نظر باید ثبت نام کنید.", icon = 'info', title = "خطا احراز هویت")
                    }
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon = "error", title = "خطا!")
                }
            }
        })
    });

    $(".user-oponion").on("click", ".user-oponion-notusefull", function (e) {
        let btn = $(this)
        let commentId = btn.closest(".user-oponion").data("comment-id");
        $.ajax({
            url: urlUserOponionSubmit,
            method: "POST",
            data: { "csrfmiddlewaretoken": csrfToken, "comment_id": commentId, "is_usefull": false },
            success: function (data) {
                if (data.success) {
                    if (data.is_authenticated) {
                        btn.find("span").text(data.no_count)
                        btn.parent().find(".user-oponion-usefull span").text(data.yes_count)
                    } else {
                        fireAlert(text =  "برای ثبت نظر باید ثبت نام کنید.", icon = 'info', title = "خطا احراز هویت")
                    }
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطا!")
                }
            }
        })
    });

    cartContainer.on("click", "#add-to-cart-btn", function () {
        let button = $(this);
        let buttonSpan = $("#add-to-cart-btn span");
        let itemId = $(this).closest(".cart-container").data("item-id");
        let colorID = $(".color-select-btn[data-active='true'").data("color-id")
        $.ajax({
            type: "POST",
            url: urlDataAddToCart,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": itemId , "color_id" : colorID ? colorID : ""},
            success: function (data) {
                if (data.success) {
                    if (!data.unavailable) {
                        fireAlert(text = `محصول ${productName} !با موفقیت به سبد خرید اضافه شد`, icon = "success", title = "افزوده شد!")

                        $(".cart-item-count").text(data.total_items);
                        buttonSpan.text("حذف از سبد خرید");
                        hiddenMinCartBar.css("display", "flex  ");
                        hiddenMinCartBar.find("input").attr("value", data.item_quantity);
                        cartContainer.find(".total-price .total_price_cart").text(`${data.item_total_price} تومان`);
                        button.attr("id", "remove-from-cart-btn");
                        button.removeClass("add-to-cart-btn").addClass("remove-from-cart-btn")
                        $(".item-count-text").text(`(${data.total_items} مورد)`)
                        $(".hidden-cart-items").append(data.html);
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                    } else {
                        fireAlert(text = "موجودی محصول تمام شده است!", icon = "error", title = "خطا!")
                    }
                }
            }
        });
    });

    cartContainer.on("click", "#remove-from-cart-btn", function () {
        let button = $(this);
        let buttonSpan = $("#remove-from-cart-btn span");
        let itemId = $(this).closest(".cart-container").data("item-id");

        $.ajax({
            type: "POST",
            url: urlRemoveFromCart,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": itemId },
            success: function (data) {
                if (data.success) {
                    if (!data.in_cart) {
                        fireAlert(text = "محصولی برای حذف در سبد خرید شما وجود ندارد!", icon = "error", title = "خطا!")
                    } else {
                        fireAlert(text = `محصول ${productName} با موفقیت از سبد خرید حذف شد`, icon = "success", title = "حذف شد!")
                        $(".cart-item-count").text(data.total_items);

                        $(".item-count-text").text(`(${data.total_items} مورد)`);
                        buttonSpan.text("افزودن به سبد خرید");
                        hiddenMinCartBar.css("display", "none");
                        button.attr("id", "add-to-cart-btn");
                        button.removeClass("remove-from-cart-btn").addClass("add-to-cart-btn");
                        $(".mini-item-input-" + productId).closest(".cart-item").remove();
                        // button.addClass("add-to-cart-btn");
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                    }
                } else {
                    fireAlert(text = "خطایی حین حذف رخ داد!", icon = "error", title = "خطا!")
                }
            }
        });
    });

    $("#relatedProducts").on("click", ".favourite-btn", function () {
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
                        fireAlert(text = "محصول در دیتابیس وجود ندارد", icon = "error", title = "خطا!")
                    }
                } else {
                    fireAlert(text = "برای افزودن به علاقه مندی ها نیاز به ثبت نام/ورود دارید", icon = "info")
                }

            }
        });
    });

    $(".add-to-favourite-btn").on("click", function (e) {

        let btn = $(this)
        $.ajax({
            url: urlAddToFavourite,
            data: { "product_id": productId, "csrfmiddlewaretoken": csrfToken },
            method: "POST",
            success: function (data) {
                if (data.is_authenticated) {
                    if (!data.error) {
                        if (data.in_favourite) {
                            btn.addClass("text-blue-500")
                        }
                        else {
                            btn.removeClass("text-blue-500")
                        }
                    } else {
                        fireAlert(text = "محصول در دیتابیس وجود ندارد", icon = "error", title = "خطا!")
                    }
                } else {
                    fireAlert(text = "برای افزودن به علاقه مندی ها نیاز به ثبت نام/ورود دارید", icon = "info")
                }
            }
        })
    });


    let suggestBtns = document.querySelectorAll("button[name=suggest]")

    suggestBtns.forEach(function (ele) {
        ele.removeAttribute("checked")
        ele.addEventListener("click", function (e) {
            e.preventDefault()
            suggestBtns.forEach(function (ele) {
                ele.classList.remove("active")
                let input = ele.nextElementSibling
                input.removeAttribute("checked")
            });
            ele.classList.add("active")
            let input = ele.nextElementSibling
            input.setAttribute("checked", "")
        })
    });

    $("#commentForm").on("submit", function (e) {
        e.preventDefault();
        let form = $(this)
        let data = {}
        let validData = true
        let serializedArray = form.serializeArray()
        let hasSuggest = serializedArray.some(function (ele) {
            return ele.name === "suggest"
        })
        form.find(".input-error").css("display", "none")
        serializedArray.forEach(function (ele) {
            if (!ele.value) {
                let error = form.find(`.input-error.${ele.name}`)
                error.css("display", "inline")
                validData = false
            } if (!hasSuggest) {
                let error = form.find('.input-error.suggest')
                error.css("display", "inline")
                validData = false
            }
            else {
                data[ele.name] = ele.value
            }
        });
        data["csrfmiddlewaretoken"] = csrfToken
        if (validData) {
            $.ajax({
                url: commentSubmit,
                type: "POST",
                data: data,
                success: function (data) {
                    if (data.success) {
                        if (data.is_authenticated) {
                            fireAlert(text = "کامنت شما با موفقیت ثبت شد و پس از بررسی قرار خواهد گرفت.", icon = "success", title = "ثبت شد!")
                        } else {
                            fireAlert(text = "برای ثبت نظر باید ثبت نام|ورود انجام دهید.", icon = "info")
                        }
                    } else {
                        fireAlert(text = "خطا!", icon = "error", title = "خطا")
                    }
                }
            });
        }
    });
});

