document.addEventListener("DOMContentLoaded", function () {
    var preloader = document.getElementById('preloader');
    var content = document.querySelector('.wrapper');
    setTimeout(function () {
        preloader.style.display = 'none';
        content.style.display = 'block';
    }, 900);
});