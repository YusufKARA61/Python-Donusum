document.addEventListener("DOMContentLoaded", function () {
  var carousel = document.getElementById("carouselBasicExample");
  var carouselInstance = new bootstrap.Carousel(carousel);

  var prevButton = document.querySelector('[data-mdb-slide="prev"]');
  var nextButton = document.querySelector('[data-mdb-slide="next"]');

  prevButton.addEventListener("click", function () {
    carouselInstance.prev();
  });

  nextButton.addEventListener("click", function () {
    carouselInstance.next();
  });
});
