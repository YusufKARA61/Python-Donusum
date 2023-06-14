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
  
  
  