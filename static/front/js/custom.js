  $(document).ready(function() {
    // Anakart seçimi değiştiğinde işlemcileri getir
    $("#anakart").change(function() {
      var anakartId = $(this).val();
      $.getJSON("/islemciler/" + anakartId, function(data) {
        var options = "";
        $.each(data, function(index, item) {
          options += "<option value='" + item.id + "'>" + item.marka + " - Fiyat: " + item.fiyat + "</option>";
        });
        $("#islemci").html(options);
      });
    });

    // İşlemci seçimi değiştiğinde ramleri getir
    $("#islemci").change(function() {
      var islemciId = $(this).val();
      $.getJSON("/ramler/" + islemciId, function(data) {
        var options = "";
        $.each(data, function(index, item) {
          options += "<option value='" + item.id + "'>" + item.marka + " - Fiyat: " + item.fiyat + "</option>";
        });
        $("#ram").html(options);
      });
    });

    // Sepete ekle butonuna tıklandığında seçilen bileşenleri sepete ekle
    $("#sepete-ekle").click(function() {
      var anakartId = $("#anakart").val();
      var islemciId = $("#islemci").val();
      var ramId = $("#ram").val();

      var bilgisayar = {
        "anakartId": anakartId,
        "islemciId": islemciId,
        "ramId": ramId
      };

      // Sepete ekleme işlemini gerçekleştirecek bir AJAX isteği gönder
      $.ajax({
        type: "POST",
        url: "/sepete-ekle",
        data: JSON.stringify(bilgisayar),
        contentType: "application/json",
        success: function(response) {
          // Sepete eklendiğine dair bildirim göster
          showNotification("Bileşenler sepete eklendi!");
        },
        error: function() {
          // Hata durumunda bildirim göster
          showNotification("Bir hata oluştu. Bileşenler sepete eklenemedi!");
        }
      });
    });

    function showNotification(message) {
      var notificationDiv = document.getElementById("notification");
      notificationDiv.textContent = message;
      notificationDiv.style.display = "block";
    }
  });
