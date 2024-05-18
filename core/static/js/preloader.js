document.addEventListener("DOMContentLoaded", function () {
    var preloader = document.getElementById('preloader');
    var content = document.querySelector('.wrapper');
    setTimeout(function () {
        preloader.style.display = 'none';
        content.style.visibility = 'visible';
        content.style.opacity = '1';
    }, 900);
});