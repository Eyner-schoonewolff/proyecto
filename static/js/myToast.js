document.addEventListener("DOMContentLoaded", function() {
    var toastElement = document.querySelector('.toast');
    if (toastElement) {
        var myToast = new bootstrap.Toast(toastElement);
        myToast.show();
    }
});
