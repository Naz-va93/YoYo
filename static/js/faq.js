document.addEventListener('DOMContentLoaded', function () {
    const details = document.querySelectorAll("details");
    details.forEach((targetDetail) => {
        targetDetail.addEventListener("click", () => {
            details.forEach((detail) => {
                if (detail !== targetDetail) {
                    detail.removeAttribute("open");
                }
            });
        });
    });

    document.querySelector('.faq-btn').addEventListener('click', function () {
        const faqContent = document.querySelector('.d-display');
        faqContent.classList.toggle('show');
        if (faqContent.classList.contains('show')) {
            setTimeout(() => {
                faqContent.scrollIntoView({behavior: 'smooth'});
            }, 90);
        }
    });
});
