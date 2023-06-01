$(document).ready(function() {
    $("#yapi_sinifi").change(function() {
      var yapiSinifi = $(this).val();

      $.ajax({
        type: "POST",
        url: "/projeler",
        data: JSON.stringify({ yapi_sinifi: yapiSinifi }),
        contentType: "application/json",
        success: function(response) {
          var options = "";
          $.each(response, function(index, proje) {
            options += "<option value='" + proje + "'>" + proje + "</option>";
          });
          $("#projeler").html(options);
        },
        error: function() {
          console.log("Bir hata oluştu. Projeler getirilemedi!");
        }
      });
    });
  });

