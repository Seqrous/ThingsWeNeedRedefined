$(".button-modal").each(function(index) {
    $(this).on("click", function() {
        let buttonId = $(this).attr("id")
        let household_slug = buttonId.split("-")[3].concat('/')
        let user = buttonId.split("-")[2].concat('/')
        let redirect = '/'.concat(user, household_slug, "add-product/")
        $("#add-product-form").attr("action", redirect)
    })
})
