
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
document.addEventListener("DOMContentLoaded", function () {
    const dataTAg = $(".post-list-data")
    const phoneToggle = document.getElementById("hs-valid-toggle-switch");
    const phoneLabel = document.querySelector('label[for="hs-valid-toggle-switch"].text-gray-800');
    let urlPostFilter = dataTAg.data("post-filter-ajax")
    let filterBaseData = {
        "pid" : dataTAg.data("pid"),
        "base_cat_id" : dataTAg.data("base-cat-id")
    }
    const accordions = document.querySelectorAll('.accordion-btn');
    if (accordions.length > 0) { 
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





    // toggleAccordion at Shop Page


    phoneToggle?.addEventListener("change", function () {
        if (phoneToggle.checked) {
            phoneLabel.classList.add("text-blue-500");
            phoneLabel.classList.remove("text-gray-800");
        } else {
            phoneLabel.classList.remove("text-blue-500");
            phoneLabel.classList.add("text-gray-800");
        }
    });

    const sortModal = document.querySelector('.sort-modal')
    const sortModalOpen = document.querySelector('.sort-modal-open')
    const sortModalClose = document.querySelector('.sort-modal-close')
    const searchOverlay = document.querySelector('.search-overlay');

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

    function queryUpdator(mainQuery, addingQuery, act) {
        if (!mainQuery) return "?" + addingQuery
        if (!mainQuery.includes("cat_id=") && addingQuery.includes("cat_id=")) {
            mainQuery += "&cat_id="
        }
        if (act === "add") {
            let core = mainQuery.replace("?", "");
            let parts = core.split("&")
            let newKey = addingQuery.split("=")[0]
            let newVal = addingQuery.split("=")[1]
            let filtered = parts.map((ele) => {
                if (ele.startsWith("cat_id")) {
                    let ids = ele.split("=")[1].split(",")
                    let filteredIds = ids.filter((ele) => {
                        return !(ele === newVal)
                    })
                    if (newKey == "cat_id") {
                        filteredIds.push(newVal)
                    }
                    filteredIds = filteredIds.filter((ele) => {
                        return ele
                    })
                    return "cat_id" + "=" + filteredIds.join(",")
                }
                else {
                    if (ele.startsWith(newKey)) {
                        return null
                    } else {
                        return ele
                    }
                }
            });
            filtered = filtered.filter(ele => ele !== null);
            if (!addingQuery.startsWith("cat_id")) {
                filtered.push(addingQuery)
            }
            return filtered.length ? "?" + filtered.join("&") : ""
        }
        if (act === "remove" && mainQuery) {
            let newKey = addingQuery.split("=")[0]
            let newVal = addingQuery.split("=")[1]
            if (newKey == "cat_id") {
                let core = mainQuery.replace("?", "")
                let parts = core.split("&")
                let finalParts = parts.map((ele) => {
                    if (ele.startsWith("cat_id")) {
                        let ids = ele.split("=")[1].split(",")
                        let filteredIds = ids.filter((ele) => {
                            return !(ele === newVal)
                        });
                        return "cat_id" + "=" + filteredIds.join(",")
                    } else {
                        return ele
                    }
                })
                return "?" + finalParts.join("&")
            }
        }
        return mainQuery;
    }
    let postCount = $(".post-count")
    let orderOptions = $(".order-option")
    let productsContainer = $(".posts-container")




    $(".cat-filter-input").on("input", function (e) {
        let input = $(this);
        let catId = input.closest(".cat-filter").data("cat-id")
        let checked = input.is(":checked")
        let query = null
        if (checked) {
            query = queryUpdator(location.search, `cat_id=${catId}`, "add")
        } else {
            query = queryUpdator(location.search, `cat_id=${catId}`, "remove")
        }
        $.ajax({
            url: urlPostFilter + query,
            method: "GET",
            data : filterBaseData,
            success: function (data) {
                if (data.success) {
                    productsContainer.html(data.html)
                    postCount.text(`${data.post_count} مقاله`)
                    history.pushState({}, "", query)
                } else {
                    fireAlert(text = "خطایی رخ داد!", icon="error")
                }
            }
        });
    });
    productsContainer.on("click", ".posts-pagination-ajax", function (e) {
        let btn = $(this);
        let pageNum = btn.data("page")
        let query = queryUpdator(location.search, `page=${pageNum}`, "add")
        $.ajax({
            url: urlPostFilter + query,
            data : filterBaseData,
            method: "GET",
            success: function (data) {
                if (data.success) {
                    productsContainer.html(data.html)
                    history.pushState({}, "", query)
                    window.scroll(0,0)
                } else {
                    fireAlert(text = "خطایی رخ داد!" , icon="error")
                }
            }
        });
    });
    orderOptions.on("click", function (e) {
        let listItem = $(this);
        let orderOption = listItem.data("value");
        let query = queryUpdator(location.search, `order=${orderOption}`, "add");
        orderOptions.removeClass("text-blue-500");
        orderOptions.addClass("text-gray-400");
        listItem.removeClass("text-gray-400");
        listItem.addClass("text-blue-500");
        $.ajax({
            url: urlPostFilter + query,
            method: "GET",
            data: filterBaseData,
            success: function (data) {
                if (data.success) {
                    productsContainer.html(data.html)
                    history.pushState({}, "", query)
                } else {
                   fireAlert(text = "خطایی رخ داد!" , icon="error")

                }
            }
        });
    });
    $(".clear-filters").on("click", function () {
        location.search = ""
    })
    window.addEventListener("popstate", function () {
        location.search = location.search
    })
});