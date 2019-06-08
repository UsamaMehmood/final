$(document).ready(function () {
  $(".form-field").on('focusin', function () {
    $(this).addClass('is-filled');
  });
  $(".form-field").on('focusout', function () {
    if ($(this).find($(".field")).val().length < 1) {
      $(this).removeClass('is-filled');
    }
  });
  $(".post").on('focusin', function () {
    if ($(this).text() === "Write a post...") {$(this).text('')}
  });
  $(".post").on('focusout', function () {
    if ($(this).text().length < 1) {$(this).text("Write a post...")}
  });
});
