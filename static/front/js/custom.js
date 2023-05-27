jQuery(document).ready(function() {
	
	"use strict";
	// Your custom js code goes here.
	
function showNotification(message) {
        var notificationDiv = document.getElementById("notification");
        notificationDiv.textContent = message;
        notificationDiv.style.display = "block";
}

});