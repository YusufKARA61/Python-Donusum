$(document).ready(function() {
    var currentPath = window.location.pathname;
    var menuLinks = $('.menu-link');
  
    menuLinks.each(function() {
      var link = $(this).attr('href');
  
      if (link === currentPath || currentPath.startsWith(link)) {
        $(this).addClass('active');
        $(this).parents('.collapse').addClass('show');
        $(this).parents('.sidebar-link').addClass('active');
      }
  
      $(this).on('click', function(e) {
        menuLinks.removeClass('active');
        $(this).addClass('active');
        $(this).parents('.collapse').addClass('show');
        $(this).parents('.sidebar-link').addClass('active');
      });
    });
  });

  function showConfirmation() {
    $('#confirmation-modal').modal('show');
  }
  
  function cancelDeletion() {
    $('#confirmation-modal').modal('hide');
  }

  var deleteURL = "{{ url_for('sil_proje', proje_id='projeId') }}";

  function deleteItem(projeId) {
    // Silme işlemini AJAX ile Flask rotasına gönder
    $.ajax({
      url: deleteURL.replace('projeId', projeId),
      method: "POST",
      success: function(response) {
        // Silme işlemi başarılı olduğunda yapılacak işlemler
        // Örneğin, mesaj gösterme veya sayfa yenileme
        alert(response.message);
        window.location.reload();
      },
      error: function(xhr, status, error) {
        // Hata durumunda yapılacak işlemler
        console.log(error);
      }
    });
  }
  
  
  
  
  
  
  
  