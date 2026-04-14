

document.addEventListener("DOMContentLoaded", function () {
  const accordions = document.querySelectorAll('.accordion-btn');

  if (accordions.length > 0) { // بررسی وجود آکاردئون در صفحه
    accordions.forEach(btn => {
      btn.addEventListener('click', function () {
        const content = this.nextElementSibling;
        const icon = this.querySelector('.accordion-icon');

        if (content.style.maxHeight) {
          content.style.maxHeight = null;
          icon.classList.remove('rotate-180');
        } else {
          document.querySelectorAll('.accordion-content').forEach(item => {
            item.style.maxHeight = null;
            item.previousElementSibling.querySelector('.accordion-icon').classList.remove('rotate-180');
          });

          content.style.maxHeight = content.scrollHeight + "px";
          icon.classList.add('rotate-180');
        }
      });
    });
  }
  const colorBtns = document.querySelectorAll(".product-colors button")
  let productsContainer = document.querySelector(".products-pagination")

  productsContainer.addEventListener("click", function (e) {
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

});





// toggleAccordion at Shop Page
function toggleAccordion(index) {
  const content = document.getElementById(`content-${index}`);
  const icon = document.querySelector(`#icon-${index} svg`);

  if (content.style.maxHeight && content.style.maxHeight !== '0px') {
    content.style.maxHeight = '0';
    icon.classList.remove('-rotate-90');
  } else {
    content.style.maxHeight = content.scrollHeight + 'px';
    icon.classList.add('-rotate-90');
  }
}


// PRICE RANGE
document.querySelectorAll(".price-slider").forEach((sliderContainer) => {
  const priceElements = sliderContainer.querySelectorAll(".price-input p");
  const rangeInputs = sliderContainer.querySelectorAll(".range-input input");
  const range = sliderContainer.querySelector(".slider-bar .progress");
  let priceGap = 1000;

  function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  rangeInputs.forEach((input) => {
    input.addEventListener("input", (e) => {
      let minVal = parseInt(rangeInputs[0].value) * 10;
      let maxVal = parseInt(rangeInputs[1].value) * 10;

      if (maxVal - minVal < priceGap) {
        if (e.target.classList.contains("min-range")) {
          rangeInputs[0].value = (maxVal - priceGap) / 10;
        } else {
          rangeInputs[1].value = (minVal + priceGap) / 10;
        }
      } else {
        priceElements[0].textContent = formatNumber(minVal);
        priceElements[1].textContent = formatNumber(maxVal);
        range.style.left = (rangeInputs[0].value / rangeInputs[0].max) * 100 + "%";
        range.style.right = 100 - (rangeInputs[1].value / rangeInputs[1].max) * 100 + "%";
      }
    });
  });
});


// SOERT MODALS - SHOP PAGE
const sortModal = document.querySelector('.sort-modal')
const sortModalOpen = document.querySelector('.sort-modal-open')
const sortModalClose = document.querySelector('.sort-modal-close')

sortModalOpen?.addEventListener('click', () => {
  searchOverlay.classList.add('active')
  sortModal.classList.add('active')
})

sortModalClose?.addEventListener('click', () => {
  searchOverlay.classList.remove('active')
  sortModal.classList.remove('active')
})

// FILTER MODALS - SHOP PAGE
const filterModal = document.querySelector('.filter-modal')
const filterModalOpen = document.querySelector('.filter-modal-open')
const filterModalClose = document.querySelector('.filter-modal-close')

filterModalOpen?.addEventListener('click', () => {
  searchOverlay.classList.add('active')
  filterModal.classList.add('active')
})

filterModalClose?.addEventListener('click', () => {
  searchOverlay.classList.remove('active')
  filterModal.classList.remove('active')
})



// ajax reqeust 


$(document).ready(function () {
  let productsContainer = $(".products-pagination")
  let orderBy = [...document.querySelector(".order-by").children]
  let orderByModile = [...document.querySelector(".order-by-mobile").children]



  let dataTag = $(".product-list-data")
  let urlFilterAjaxHandler = dataTag.data("url-filter-ajax-handler")
  let urlAddToFavourite = dataTag.data("add-to-favourite")
  let urlAddToCart = dataTag.data("url-add-to-cart")
  let catSlug = dataTag.data("cat-slug")
  let sliderId = dataTag.data("slider-id")
  let amazingId = dataTag.data("amazing-offer-id")
  let filterBaseData = { "cat_slug": catSlug ? catSlug : "", "slider_id": sliderId ? sliderId : "", "amazing_id": amazingId }
  let csrfToken = $(".base-data").data("csrf-token")
  let productCounter = $("#product-counter, .product-counter")


  function formatNumber(value) {
    if (value === null || value === undefined) return '';

    // Accept numeric strings too
    const str = String(value).trim();

    // Try fast path for normal numeric-looking strings: sign + digits + optional decimal
    const m = str.match(/^([+-]?)(\d+)(\.\d+)?$/);
    if (!m) {
      // Try converting to number (handles scientific notation like "1e6")
      const n = Number(str);
      if (!Number.isFinite(n)) return str; // return original if not numeric
      // Convert numeric value to string in plain notation (avoid exponential where possible)
      // Use toString for integers and toFixed for decimals preserving existing decimals if present
      const parts = String(n).split('e');
      if (parts.length === 1) {
        // No exponent
        return formatNumber(String(n));
      } else {
        // For exponential form, use Intl to format as a number then fallback to regex approach
        const plain = n.toLocaleString('en-US', { useGrouping: false, maximumFractionDigits: 20 });
        return formatNumber(plain);
      }
    }

    const sign = m[1] || '';
    const intPart = m[2];
    const decPart = m[3] || '';

    const intWithCommas = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    return sign + intWithCommas + decPart;
  }
  $(".order-by-favorite").on("click", function (e) {
    let btn = $(this);
    let query = generate_query(location.search, "order_by=" + "favorite")
    $.ajax({
      url: urlFilterAjaxHandler + query,
      data: filterBaseData,
      method: "GET",
      success: function (data) {

        orderBy.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        orderByModile.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        btn.css("font-weight", "bold")
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "order_by=") + "favorite")
      }
    })
  });
  $(".order-by-sale").on("click", function (e) {
    let btn = $(this);
    let query = generate_query(location.search, "order_by=" + "sale")

    $.ajax({
      url: urlFilterAjaxHandler + query,
      data: filterBaseData,
      method: "GET",
      success: function (data) {

        orderBy.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        orderByModile.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        btn.css("font-weight", "bold")
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "order_by=") + "sale")
      }
    })
  })
  $(".order-by-price-min").on("click", function (e) {
    let btn = $(this)
    let query = generate_query(location.search, "order_by=") + "min_price";
    $.ajax({
      url: urlFilterAjaxHandler + query,
      data: filterBaseData,
      method: "GET",
      success: function (data) {

        orderBy.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        orderByModile.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        btn.css("font-weight", "bold")
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "order_by=") + "min_price")
      }
    })
  });
  $(".order-by-price-max").on("click", function (e) {
    let btn = $(this)
    let query = generate_query(location.search, "order_by=") + "max_price";
    $.ajax({
      url: urlFilterAjaxHandler + query,
      data: filterBaseData,
      method: "GET",
      success: function (data) {

        orderBy.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        orderByModile.forEach((ele) => {
          ele.style = "font-wight :none;"
        });
        btn.css("font-weight", "bold")
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "order_by=") + "max_price")
      }
    })
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

  $(".attendent-buy").change(function (e) {
    let attendentBuy = null
    if ($(this).is(":checked")) {
      attendentBuy = "true"
    } else {
      attendentBuy = "false"
    }
    $.ajax({
      url: urlFilterAjaxHandler + generate_query(location.search, "attendant_buy=") + `${attendentBuy}`,
      data: filterBaseData,
      method: "GET",
      success: function (data) {

        productCounter.text(`${data.count} کالا`);
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "attendant_buy=") + `${attendentBuy}`)
      }
    })
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
      data: { "csrfmiddlewaretoken": csrfToken, "product_id": product_id , "color_id" : colorId},
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


  $(".inventory-filter").on("change", function () {
    let is_in_inventory = null
    if ($(this).is(":checked")) {
      is_in_inventory = "true"
    } else {
      is_in_inventory = "false"
    }
    $.ajax({
      url: urlFilterAjaxHandler + generate_query(location.search, "inventory=") + `${is_in_inventory}`,
      method: "GET",
      data: filterBaseData,
      success: function (data) {

        productCounter.text(`${data.count} کالا`);
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "inventory=") + `${is_in_inventory}`)
      }
    })
  })
  $(".today-delivery").on("change", function () {
    let todayDelivery = null
    if ($(this).is(":checked")) {
      todayDelivery = "true"
    } else {
      todayDelivery = "false"
    }
    $.ajax({
      url: urlFilterAjaxHandler + generate_query(location.search, "today_delivery=") + `${todayDelivery}`,
      method: "GET",
      data: filterBaseData,
      success: function (data) {

        productCounter.text(`${data.count} کالا`);
        productsContainer.html(data.template)
        history.pushState("", {}, generate_query(location.search, "today_delivery=") + `${todayDelivery}`)
      }
    })
  });



  let timeout;
  $(".min-range, .max-range").on("input", function () {
    let min = $(".min-range").val();
    let max = $(".max-range").val();
    $(".min-input").text(formatNumber(min));
    $(".max-input").text(formatNumber(max));
    $(".min-input-mobile").text(formatNumber(min));
    $(".max-input-mobile").text(formatNumber(max));


    // Create separate parameters correctly
    let url = urlFilterAjaxHandler;
    let query = location.search;

    // First add max_price
    let newQuery = generate_query(query, `max_price=${max}`);
    // Then add min_price to the resulting query
    newQuery = generate_query(newQuery, `min_price=${min}`);
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      $.ajax({
        url: url + newQuery,
        method: "GET",
        data: filterBaseData,
        success: function (data) {
          productCounter.text(`${data.count} کالا`);

          productsContainer.html(data.template);
          history.pushState("", {}, newQuery);
        }
      });
    }, 500)

  });


  $(".min-range-mobile, .max-range-mobile").on("input", function () {
    let min = $(".min-range-mobile").val();
    let max = $(".max-range-mobile").val();
    $(".min-input-mobile").text(formatNumber(min));
    $(".max-input-mobile").text(formatNumber(max));


    // Create separate parameters correctly
    let url = urlFilterAjaxHandler;
    let query = location.search;

    // First add max_price
    let newQuery = generate_query(query, `max_price=${max}`);
    // Then add min_price to the resulting query
    newQuery = generate_query(newQuery, `min_price=${min}`);
    clearTimeout(timeout)
    timeout = setTimeout(() => {

      $.ajax({
        url: url + newQuery,
        method: "GET",
        data: filterBaseData,
        success: function (data) {
          productCounter.text(`${data.count} کالا`);

          productsContainer.html(data.template);
          history.pushState("", {}, newQuery);
        }
      });
    }, 500)

  });



  ;
  // });
  function generate_query(query, added_query) {
    // If no query string exists, start with "?"
    if (!query) {
      return "?" + added_query;
    }
    // Remove the "?" if present for easier manipulation
    query = query.replace("?", "");

    // Split into individual parameters
    let params = query.split("&").filter(param => param); // Filter removes empty strings

    // Get the parameter name from added_query (everything before "=")
    let newParamName = added_query.split("=")[0];

    // Remove any existing parameter with the same name
    params = params.filter(param => !param.startsWith(newParamName + "="));

    // Add the new parameter
    params.push(added_query);

    // Reconstruct the query string
    return "?" + params.join("&");
  }
  $(".category-checkbox-input").change(function () {
    let radio = $(this);
    let cat_id = radio.closest(".category-checkbox").data("category-id");
    if (radio.is(":checked")) {
      $.ajax({
        method: "GET",
        url: urlFilterAjaxHandler + generate_query(location.search, "cat_id=") + `${cat_id}`,
        data: { "cat_id": cat_id, "cat_slug": catSlug, "slider_id": sliderId },
        success: function (data) {

          productCounter.text(`${data.count} کالا`);

          productsContainer.html(data.template)
          history.pushState("", {}, generate_query(location.search, "cat_id=") + `${cat_id}`)
        }
      })
    }
  });
  $(".seller-send").change(function () {
    let sellerSend = null
    if ($(this).is(":checked")) {
      sellerSend = "true"
    } else {
      sellerSend = "false"
    }
    $.ajax({
      method: "GET",
      url: urlFilterAjaxHandler + generate_query(location.search, "seller_send=") + `${sellerSend}`,
      data: filterBaseData,
      success: function (data) {

        productCounter.text(`${data.count} کالا`);
        history.pushState("", {}, generate_query(location.search, "seller_send=") + `${sellerSend}`);
        productsContainer.html(data["template"]);
      }
    });
  });
  productsContainer.on("click", ".pagination-number", function (e) {
    e.preventDefault();
    let tag = $(this);
    let pageNumber = tag.data("page");
    $.ajax({
      url: urlFilterAjaxHandler + generate_query(location.search, "page=") + `${pageNumber}`,
      method: "GET",
      data: filterBaseData,
      success: function (data) {
        history.pushState("", {}, generate_query(location.search, "page=") + `${pageNumber}`)
        productsContainer.html(data.template)
        window.scroll(0,0)
      }
    });
  });
  window.addEventListener("popstate", function () {
    location.search = location.search
  });
  $(".clear-filters").on("click", function () {
    location.search = ""
  })
});

