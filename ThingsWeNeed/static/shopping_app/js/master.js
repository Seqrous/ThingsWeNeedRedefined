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

$(".buy-product-button").each(function(index) {
  $(this).on("click", function() {
      let buttonId = $(this).attr("id")
      let user = buttonId.split('-')[1].concat('/')
      let slug = buttonId.split('-')[2]
      let householdSlug = slug.concat('/')
      let productId = buttonId.split('-')[3].concat('/')
      let productName = buttonId.split('-')[4]
      redirect = '/'.concat(user, householdSlug, productId, 'confirm-purchase/')
      formId = "#confirm-purchase-form".concat(slug)
      form = $("#confirm-purchase-form-".concat(slug))
      form.attr('action', redirect)
      $("#confirm-purchase-dialog-p-".concat(slug)).html('Selected item: '.concat(productName))
      $("#confirm-purchase-dialog-".concat(slug)).show()
  })
})

// COLLAPSIBLE
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

// HISTORY COLLAPSIBLE
let historyColl = $('.history-collapsible')
historyColl.each(function(index) {
  $(this).on("click", function () {
    let collId = $(this).attr("id")
    let householdSlug = collId.split("-")[0]
    let history_content = $("#".concat(householdSlug, "-history-content"))

    if (history_content.css("display") === "block") {
      history_content.css("display", "none")
      $(this).html("&#9660")
    } else {
      history_content.css("display", "block")
      $(this).html("&#9650")
    }
  })
})


// POPOVER
$(function () {
    $('[data-toggle="popover"]').popover()
})

$('.popover-dismiss').popover({
    trigger: 'focus'
})

