const input = document.querySelector("input.search-city-input")
const cityList = document.querySelectorAll("ul.city-list li")
let timeout = null




function fireAlert(text, icon, title = null) {
    const isDarkMode = document.documentElement.classList.contains('dark');
    const alertOptions = {
        background: isDarkMode ? 'oklch(0.21 0.034 264.665)' : '#fff',
        color: isDarkMode ? 'oklch(0.985 0.002 247.839)' : 'oklch(0.13 0.028 261.692)',
        confirmButtonColor: isDarkMode ? 'oklch(0.488 0.243 264.376)' : 'oklch(0.623 0.214 259.815)',
        cancelButtonColor: isDarkMode ? '#f44336' : '#d33',
    };

    Swal.fire({
        title: title ? title : "",
        text: text,
        icon: icon,
        confirmButtonText: 'باشه',
        showCancelButton: false,
        cancelButtonText: 'لغو',
        background: alertOptions.background,
        color: alertOptions.color,
        confirmButtonColor: alertOptions.confirmButtonColor,
        cancelButtonColor: alertOptions.cancelButtonColor
    });
}


input.addEventListener("input", function (e) {
    let entry = e.target.value
    timeout = setTimeout(function () {
        if (entry) {
            cityList.forEach(function (ele) {
                if (ele.innerText.includes(entry)) {
                    ele.style.display = "block"
                }
                else {
                    ele.style.display = "none"
                }
            });
        }
    }, 500)
})

// Constants for class names
const ACTIVE_CLASS = 'active';
const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';
const ROTATE_CLASS = 'rotate-90';

// Selectors
const themeToggleButtons = document.querySelectorAll('.toggle-theme');
const searchButton = document.querySelector('.search-btn-open');
const searchModal = document.querySelector('.search-modal');
const openCartButton = document.querySelector('.open-cart');
const cart = document.querySelector('.cart');
const overlay = document.querySelector('.overlay');
const searchOverlay = document.querySelector('.search-overlay');
const closeCartButton = document.querySelector('.close-cart');
const mobileMenu = document.querySelector('.mobile-menu');
const openMenuButton = document.querySelector('.open-menu-mobile');
const closeMenuButton = document.querySelector('.close-menu-mobile');
const openCategory = document.querySelector('.open-category');
const categorySlide = document.querySelector('.category-slide');
const closeCategorySlide = document.querySelector('.close-category-slide');
const citylistMenu = document.querySelector('.citylist-menu');
const citylistOpen = document.querySelector('.citylist-open');
const openCartMobileButton = document.querySelector('.open-mobile-cart');
const mobileCart = document.querySelector('.mobile-cart');
const openMobileSearch = document.querySelector('.open-mobile_search-modal');
const closeMobileSearch = document.querySelector('.close-mobile_search-modal');
const MobileSearch = document.querySelector('.mobile_search-modal');
const navbar = document.querySelector('.bottom-navbar');
let lastScrollTop = 0;


// / Utility Functions
const toggleClass = (element, className, condition) => {
    if (condition) {
        element.classList.add(className);
    } else {
        element.classList.remove(className);
    }
};

// Theme Toggle Function
const toggleTheme = () => {
    const isDarkMode = localStorage.getItem('theme') === DARK_THEME;
    document.documentElement.classList.toggle(DARK_THEME, !isDarkMode);
    localStorage.setItem('theme', isDarkMode ? LIGHT_THEME : DARK_THEME);
};


// Event Listeners for Theme Toggle
// Add click listeners to toggle theme buttons
themeToggleButtons.forEach(button => {
    button.addEventListener('click', toggleTheme);
});

// Event Listener for Search Button
searchButton?.addEventListener('click', () => {
    searchModal.classList.add('active');
    searchButton.classList.add('active');
    searchOverlay.classList.add('active');
});

// Event Listener for Overlay Click 
overlay?.addEventListener('click', () => {
    overlay.classList.remove('active');
    searchModal.classList.remove('active');
    searchButton.classList.remove('active');
    cart.classList.remove('active');
    citylistMenu.classList.remove('active');
    mobileMenu.classList.remove('active')
});

// Event Listener for Search Overlay Click
searchOverlay?.addEventListener('click', () => {
    searchOverlay.classList.remove('active');
    searchModal.classList.remove('active');
    sortModal.classList.remove('active')
    filterModal.classList.remove('active')
});

// Event Listener for Opening Cart
openCartButton?.addEventListener('click', () => {
    cart.classList.add('active');
    overlay.classList.add('active');
});

// Event Listener for Closing Cart
closeCartButton?.addEventListener('click', () => {
    cart.classList.remove('active');
    overlay.classList.remove('active');
});

// Event Listener for City List Menu
citylistOpen?.addEventListener('click', () => {
    citylistMenu.classList.add('active');
    overlay.classList.add('active');
});

openCartMobileButton?.addEventListener('click', () => {
    overlay.classList.add('active')
    mobileCart.classList.add('active')
});

openMenuButton?.addEventListener('click', () => {
    mobileMenu.classList.add('active')
    overlay.classList.add('active')
})
closeMenuButton?.addEventListener('click', () => {
    mobileMenu.classList.remove('active')
    overlay.classList.remove('active')
})





openCategory?.addEventListener('click', () => {
    toggleClass(categorySlide, ACTIVE_CLASS, true);
});

closeCategorySlide?.addEventListener('click', () => {
    toggleClass(categorySlide, ACTIVE_CLASS, false);
});

// Category Details
const initializeCategoryDetails = () => {
    document.querySelectorAll('.open-detail-category').forEach(item => {
        item.addEventListener('click', () => {
            const detailCategory = item.nextElementSibling;
            if (detailCategory) {
                toggleClass(detailCategory, ACTIVE_CLASS, true);
            }
        });
    });

    document.querySelectorAll('.close-detail-category').forEach(closeButton => {
        closeButton.addEventListener('click', () => {
            const detailCategory = closeButton.closest('.detail-category');
            if (detailCategory) {
                toggleClass(detailCategory, ACTIVE_CLASS, false);
            }
        });
    });
};

// Submenu Toggle
const initializeSubmenuToggle = () => {
    document.querySelectorAll('.open-submenu').forEach(item => {
        item.addEventListener('click', function () {
            const submenu = this.nextElementSibling;
            const svg = this.querySelector('svg');
            const isActive = submenu.classList.contains(ACTIVE_CLASS);

            document.querySelectorAll('.menu-category-submenu').forEach(sub => {
                sub.classList.remove(ACTIVE_CLASS);
            });
            document.querySelectorAll('.open-submenu svg').forEach(svgItem => {
                svgItem.classList.add(ROTATE_CLASS);
            });

            if (!isActive) {
                toggleClass(submenu, ACTIVE_CLASS, true);
                toggleClass(svg, ROTATE_CLASS, false);
            }
        });
    });
};


// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initializeCategoryDetails();
    initializeSubmenuToggle();
});

// NAVBAR MOBILE LOGIC
window.addEventListener('scroll', () => {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    if (currentScroll > lastScrollTop) {
        navbar.classList.add('hidden');
    } else {
        navbar.classList.remove('hidden');
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

openMobileSearch?.addEventListener('click', () => {
    MobileSearch.classList.add('active')
})

closeMobileSearch?.addEventListener('click', () => {
    MobileSearch.classList.remove('active')
})


// MEGA-MENU
document.addEventListener("DOMContentLoaded", function () {
    const categoryItems = document.querySelectorAll(".megamenu_category-item");
    const leftMenus = document.querySelectorAll(".megamenu_left-item");


    categoryItems.forEach((item, index) => {
        item.addEventListener("mouseenter", function () {
            document.querySelector(".megamenu_category-item.active")?.classList.remove("active");
            document.querySelector(".megamenu_left-item.active")?.classList.remove("active");
            item.classList.add("active");

            if (leftMenus[index]) {
                leftMenus[index].classList.add("active");
            }
        });
    });
});







$(document).ready(function () {

    let loadingSection = $("#loadingSection")
    let loadingModal = $("#loaingModal")
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    document.getElementById("submitEmail").addEventListener("submit", function (e) {
        e.preventDefault()
        let entry = e.currentTarget.querySelector("input").value
        if (entry && emailRegex.test(entry)) {
            fireAlert(text = "ایمیل شما با موفقیت ذخیره شد!", icon = "success" , title = "ثبت شد!")
        } else  if(!entry){
        return ;
        } else {
            fireAlert(text = "لطفا ایمیل را بدرستی وارد کنید!", icon = "info")
        }

    });

    document.querySelectorAll(".bottom-navbar-item").forEach(function (ele) {
        let link = ele.querySelector("a")
        if (link.href === location.href) {

            ele.classList.add("dark:text-sky-400")
        }
    });

    $(".custom-input").on("beforeinput", function (E) {
        E.preventDefault()
    })

    $(document).ajaxStart(function (e) {
        loadingSection.css("display", "flex")
        loadingModal.addClass("active")
    });
    $(document).ajaxStop(function (E) {
        loadingSection.css("display", "none")
        loadingModal.removeClass("active")
    });

    const input = document.querySelector("input.search-city-input")
    const cityList = document.querySelectorAll("ul.city-list li")
    let timeout = null

    input.addEventListener("input", function (e) {
        let entry = e.target.value
        timeout = setTimeout(function () {
            if (entry) {
                cityList.forEach(function (ele) {
                    if (ele.innerText.includes(entry)) {
                        ele.style.display = "block"
                    }
                    else {
                        ele.style.display = "none"
                    }
                });
            }
        }, 500)
    })

    // ajax reqeust 
    let dataTag = $(".base-data")
    let urlSetCity = dataTag.data("url-set-city")
    let csrfToken = dataTag.data("csrf-token")
    let increaseCartItem = dataTag.data("increase-cart-item")
    let decreaseCartItem = dataTag.data("decrease-from-cart")
    let searchAjax = dataTag.data("search-ajax")
    let desktopTimeout = null;
    let mobileTimeout = null;
    let productDetailItemCounter = $(".custom-input-detail")
    let productDetailPriceCounter = $(".total-price .total_price_cart")


    $(".cart").on("click", ".hidden-cart-add-itm", function () {
        let button = $(this);
        let parentElement = button.closest(".cart-item")
        let itemId = $(this).closest(".cart-menu-quantity").data("product-id");
        $.ajax({
            type: "POST",
            url: increaseCartItem,
            data: { "product_id": itemId, "csrfmiddlewaretoken": csrfToken },
            success: function (data) {
                if (data.success) {
                    if (!data.unavailable) {
                        parentElement.find(".mini-item-input-" + data.product_id).attr("value", data.item_quantity)
                        parentElement.find(".hidden-itm-cart-t-p-" + data.product_id).text(data.item_total_price)
                        parentElement.find(".hidden-item-total-price-" + data.product_id + " .hidden-itm-cart-t-p").text(data.item_total_price)
                        productDetailItemCounter?.attr("value", data.item_quantity);
                        productDetailPriceCounter.text(`${data.item_total_price} تومان`);
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                        $(".detail-costum-input-" + data.product_id).attr("value", data.item_quantity)
                    } else {
                        fireAlert(text = "موجودی محصول به خارج از درخواست شماست!", icon = 'info', title = "اتمام موجودی!")
                    }
                } else {

                    fireAlert(text = "خطایی هنگام اضافه کردن محصول رخ داد!", icon = 'error', title = "خطا!")
                }
            }
        });
    });
    $(".cart").on("click", ".hidden-cart-decrease-itm", function () {
        let button = $(this);
        let itemId = $(this).closest(".cart-menu-quantity").data("product-id");
        let parentElement = button.closest(".cart-item")
        $.ajax({
            type: "POST",
            url: decreaseCartItem,
            data: { "product_id": itemId, "csrfmiddlewaretoken": csrfToken },
            success: function (data) {
                let removeFromCartBtn = $("#remove-from-cart-btn")
                if (data.success) {
                    if (!data.out_off_cart) {
                        parentElement.find(".mini-item-input-" + data.product_id).attr("value", data.item_quantity)
                        parentElement.find(".hidden-itm-cart-t-p-" + data.product_id).text(data.item_total_price)
                        parentElement.find(".hidden-item-total-price-" + data.product_id + " .hidden-itm-cart-t-p").text(data.item_total_price)
                        productDetailItemCounter?.attr("value", data.item_quantity);
                        productDetailPriceCounter.text(`${data.item_total_price} تومان`);
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                        $(".detail-costum-input-" + data.product_id).attr("value", data.item_quantity)
                    } else {
                        parentElement.remove()
                        $(".cart-item-count").text(data.total_items);
                        $("#itemCountDetail").text(`(${data.total_items} کالا)`)
                        $(".cart-item-detail-" + data.product_id).remove()
                        removeFromCartBtn.find("span").text("افزودن به سبد خرید");
                        removeFromCartBtn.attr("id", "add-to-cart-btn");
                        removeFromCartBtn.removeClass("remove-from-cart-btn").addClass("add-to-cart-btn");
                        $(".hidden-min-cart-bar").css("display", "none");
                        $(".total-price-no-post").text(`${data.final_price} تومان`);
                        $(".add-to-cart-btn-" + data.product_id).removeClass("text-blue-500")
                        $(".item-count-text").text(`(${data.total_items} مورد)`)
                    }
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطا!")
                }
            }
        });
    });

    $("#search-desktop").on("input", function (e) {
        clearTimeout(desktopTimeout);
        let input = $(this);
        desktopTimeout = setTimeout(function () {
            $.ajax({
                type: "GET",
                url: searchAjax,
                data: input.serialize(),
                dataType: "html",
                success: function (data) {
                    $("#search-instant-result").html(data);
                    $(".client-search").text(input.val());
                }
            });
        }, 750); // 400ms debounce
    });

    $("#search-for-mobile").on("input", function (e) {
        clearTimeout(mobileTimeout);
        let input = $(this);
        mobileTimeout = setTimeout(function () {
            $.ajax({
                type: "GET",
                url: searchAjax,
                data: input.serialize(),
                dataType: "html",
                success: function (data) {
                    $("#search-instant-result-mobile").html(data);
                    $(".client-search").text(input.val());
                }
            });
        }, 750); // 400ms debounce
    });

    $(document).ajaxError(function (e) {
        fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطا!")
    });

    $(".city-select").on("click", function () {
        let btn = $(this)
        let cityLookUp = btn.data("city")
        let cityValue = btn.data("city-value")
        $.ajax({
            url: urlSetCity,
            data: { "csrfmiddlewaretoken": csrfToken, "city_value": cityValue, "city_lookup": cityLookUp },
            method: "POST",
            success: function (data) {
                if (data.success) {
                    $(".overlay,.citylist-menu").removeClass("active");
                    $(".citylist-open p").text(data.city);
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطا!")
                }
            }
        });
    });
});
