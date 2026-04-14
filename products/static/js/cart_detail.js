
$(document).ready(function () {
    let dataTag = $(".cart-detail-data");
    let increaseCartItem = dataTag.data("increase-cart-item");
    let cartClear = dataTag.data("cart-clear")
    let decreaseFromCart = dataTag.data("decrease-from-cart")
    let csrfToken = $(".base-data").data("csrf-token")
    let removeFromCartUrl = dataTag.data("remove-from-cart")
    const isDarkMode = $("html").hasClass('dark');
    const alertOptions = {
        background: isDarkMode ? 'oklch(0.21 0.034 264.665)' : '#fff',
        color: isDarkMode ? 'oklch(0.985 0.002 247.839)' : 'oklch(0.13 0.028 261.692)',
        confirmButtonColor: isDarkMode ? 'oklch(0.488 0.243 264.376)' : 'oklch(0.623 0.214 259.815)',
        cancelButtonColor: isDarkMode ? '#f44336' : '#d33',
    };
    let itemCountText = $(".item-count-text")
    let cartItemCount = $(".cart-item-count")
    let totalPriceNoPost = $(".total-price-no-post")
    let itemCountDetail = $(".item-count-detail")
    let cartTotalPriceDetail = $(".cart-total-price-detail")
    let IDK = $(".idk")
    let mainEle = $("main")




    $(".item-increase-detail").on("click", function () {
        let button = $(this);
        let cartItemDetail = button.closest(".cart-item-detail")
        let ItemId = cartItemDetail.data("product-id");
        $.ajax({
            type: "POST",
            url: increaseCartItem,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": ItemId },
            success: function (data) {
                if (data.success) {
                    if (!data.unavailable) {
                        $(".mini-item-input-" + ItemId).attr("value", data.item_quantity)
                        $(".total-price .total_price_cart").text(`${data.item_total_price} تومان`);
                        // $(".mini-item-input-" + "{{product.pk}}").closest(".hidden-item-total-price").text(`${data.item_total_price} تومان`);
                        $(".hidden-itm-cart-t-p-" + ItemId).text(data.item_total_price);
                        totalPriceNoPost.text(`${data.final_price} تومان`);
                        cartItemDetail.find(".detail-costum-input-" + ItemId).attr("value", data.item_quantity)
                        cartTotalPriceDetail.text(`${data.final_price} تومان`)
                        $(".product-detail-total-price-" + ItemId).text(data.item_total_price)
                    } else {
                        fireAlert(text = "میزان انتخابی فراتز از موجودی است!", icon = 'info', title = "درخواست بیش از موجودی")
                    }
                }
                else {
                    fireAlert(text = "خطایی رخ داد!", icon = 'error', title = "خطا!")
                }
            }
        });
    });

    $(".cart-clear-btn").on("click", function () {
        let button = $(this);
        $.ajax({
            type: "GET",
            url: cartClear,
            dataType: "html",
            success: function (data) {
                mainEle.html(data)
                mainEle.removeClass("container")
                mainEle.add("container mb-20")
                $(".cart-item").remove()
                $(".item-count-text ").text(`(0 مورد)`)
                cartItemCount.text(0);
                totalPriceNoPost.text("0 تومان")
            }
        });
    });

    $(".decrease-from-cart-detail").on("click", function () {
        let button = $(this);
        let itemElement = button.closest(".cart-item-detail")
        let ItemId = itemElement.data("product-id");
        $.ajax({
            type: "POST",
            url: decreaseFromCart,
            data: { "csrfmiddlewaretoken": csrfToken, "product_id": ItemId, "send_from_detail": true },
            success: function (data) {
                if (data.success) {
                    if (data.html) {
                        mainEle.html(data.html)
                        mainEle.removeClass("container")
                        mainEle.add("container mb-20")
                        IDK.text(`قیمت کالاها (${data.total_items})`)
                        itemCountDetail.text(`(${data.total_items} کالا)`)
                        cartItemCount.text(data.total_items);
                        $(".cart-item").remove()
                        itemElement.remove()
                        totalPriceNoPost.text(`${data.final_price} تومان`);
                        itemCountText.text(`(${data.total_items} مورد)`)
                        cartTotalPriceDetail.text(`${data.final_price} تومان`)
                    }
                    else {
                        if (!data.out_off_cart) {

                            $(".mini-item-input-" + ItemId).attr("value", data.item_quantity)
                            $(".total-price .total_price_cart").text(`${data.item_total_price} تومان`);
                            // $(".mini-item-input-" + "{{product.pk}}").closest(".hidden-item-total-price").text(`${data.item_total_price} تومان`);
                            $(".hidden-itm-cart-t-p-" + ItemId).text(data.item_total_price);
                            totalPriceNoPost.text(`${data.final_price} تومان`);
                            $(".product-detail-total-price-" + ItemId).text(data.item_total_price)
                            itemElement.find(".detail-costum-input-" + ItemId).attr("value", data.item_quantity)
                            cartTotalPriceDetail.text(`${data.final_price} تومان`)
                        } else {
                            IDK.text(`قیمت کالاها (${data.total_items})`)
                            itemCountDetail.text(`(${data.total_items} کالا)`)
                            cartItemCount.text(data.total_items);
                            $(".mini-item-input-" + ItemId).closest(".cart-item").remove()
                            itemElement.remove()
                            totalPriceNoPost.text(`${data.final_price} تومان`);
                            $(".item-count-text ").text(`(${data.total_items} مورد)`)
                            cartTotalPriceDetail.text(`${data.final_price} تومان`)
                            itemCountText.text(`(${data.total_items} مورد)`)
                        }
                    }
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon = "error", title = "خطا!")
                }
            }
        });
    });


    $(".remove-from-cart-detail").on("click", function () {
        let button = $(this)
        let itemElement = button.closest(".cart-item-detail")
        let itemId = button.closest(".data-container").data("product-id");
        $.ajax({
            type: "POST",
            url: removeFromCartUrl,
            data: { "product_id": itemId, "csrfmiddlewaretoken": csrfToken, "send_from_detail": true },
            success: function (data) {
                if (data.success) {
                    if (data.html) {
                        mainEle.html(data.html)
                        mainEle.removeClass("container")
                        mainEle.add("container mb-20")
                        itemElement.remove()
                        cartTotalPriceDetail.text(`${data.final_price} تومان`)
                        IDK.text(`قیمت کالاها (${data.total_items})`)
                        $(".item-count-detail ").text(`(${data.total_items} کالا)`)
                        cartItemCount.text(data.total_items);
                        $(".mini-item-input-" + data.product_id).closest(".cart-item").remove();
                        totalPriceNoPost.text(`${data.final_price} تومان`);
                        $(".item-count-text ").text(`(${data.total_items} مورد)`)
                    } else {
                        itemElement.remove()
                        cartTotalPriceDetail.text(`${data.final_price} تومان`)
                        IDK.text(`قیمت کالاها (${data.total_items})`)
                        $(".item-count-detail ").text(`(${data.total_items} کالا)`)
                        cartItemCount.text(data.total_items);
                        $(".mini-item-input-" + data.product_id).closest(".cart-item").remove();
                        totalPriceNoPost.text(`${data.final_price} تومان`);
                        $(".item-count-text ").text(`(${data.total_items} مورد)`)
                    }
                }
                else {
                    fireAlert(text = "خطایی رخ داد!" , icon = "error" , title = "حطا!")

                }
            }
        });
    });
});