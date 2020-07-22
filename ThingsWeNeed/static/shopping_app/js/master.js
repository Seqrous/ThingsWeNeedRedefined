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
      let householdSlug= buttonId.split('-')[2].concat('/')
      let id = buttonId.split('-')[3]
      let productId = id.concat('/')
      redirect = '/'.concat(user, householdSlug, productId, 'confirm-purchase/')
      form = $("#confirm-purchase-form")
      form.attr('action', redirect)
    $("#confirm-purchase-dialog-p").html('Selected item:'.concat(id))
    $("#confirm-purchase-dialog").show()
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

$(function () {
    console.log('aaaaa')
    $('[data-toggle="popover"]').popover()
})

$('.popover-dismiss').popover({
    trigger: 'focus'
})