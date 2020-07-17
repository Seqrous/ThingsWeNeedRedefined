$(".button-modal").each(function(index) {
    $(this).on("click", function() {
        let buttonId = $(this).attr("id")
        let householdSlug = buttonId.split("-")[3].concat('/')
        let user = buttonId.split("-")[2].concat('/')
        let redirect = '/'.concat(user, householdSlug, "add-product/")
        $("#add-product-form").attr("action", redirect)
    })
})

$(".remove-product-button").each(function(index) {
    $(this).on("click", function() {
        let buttonId = $(this).attr("id")
        let user = buttonId.split('-')[1].concat('/')
        let householdSlug= buttonId.split('-')[2].concat('/')
        let productId = buttonId.split('-')[3].concat('/')
        redirect = '/'.concat(user, householdSlug, productId, 'remove/')
        form = $(this).parent()
        form.attr('action', redirect)
    })
})