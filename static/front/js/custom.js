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

document.addEventListener("DOMContentLoaded", function() {
  // Tablodaki satırlara tıklama olayını ekle
  var rows = document.querySelectorAll("table tbody tr[data-href]");
  rows.forEach(function(row) {
      row.addEventListener("click", function() {
          window.location.href = row.dataset.href;
      });
      row.style.cursor = "pointer"; // Satıra imleci göster
      row.addEventListener("mouseover", function() {
          row.style.backgroundColor = "#f5f5f5"; // Hover efekti
      });
      row.addEventListener("mouseout", function() {
          row.style.backgroundColor = ""; // Hover efektini kaldır
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var cookieConsent = document.getElementById("cookie-consent");
  var cookieConsentButton = document.querySelector("#cookie-consent button");
  
  // Çerezleri kabul etme butonuna tıklandığında pop-up'ı gizle
  cookieConsentButton.addEventListener("click", function() {
    cookieConsent.style.display = "none";
  });
  
  // Sayfa yüklendiğinde pop-up'ı göster
  cookieConsent.style.display = "block";
});



