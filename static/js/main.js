function like(elem) {
  if ($(elem).hasClass('is-liked')) {
    $(elem).removeClass('is-liked');
  } else {
    $(elem).addClass("is-liked");
  }
}

function uploadFile() {
  $("#file_upload").click();
}

function toTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function showAlert(message) {
  $("#fyp-alert").text(message);
  $("#fyp-alert").css("bottom", "5%");
  setTimeout(function () {
    $("#fyp-alert").css("bottom", "-50%");
  }, 2000)
}
