document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('label').forEach(function(label) {
        const selectSpan = label.querySelector('.select');
        const selectElement = selectSpan ? selectSpan.querySelector('select') : null;
        const otherSpan = label.querySelector('.other');
        const otherInput = otherSpan ? otherSpan.querySelector('.other__input input') : null;
        const otherSvg = otherSpan ? otherSpan.querySelector('svg') : null;

        if (selectSpan && selectElement && otherSpan && otherInput && otherSvg) {
            otherSpan.style.display = 'none';

            const isSelectRequired = selectElement.hasAttribute('required');

            selectElement.addEventListener('change', function() {
                if (selectElement.value === 'other') {
                    selectSpan.style.display = 'none';
                    otherSpan.style.display = 'flex';
                    otherInput.focus();
                    if (isSelectRequired) {
                        otherInput.setAttribute('required', '');
                        selectElement.removeAttribute('required');
                    }
                }
            });

            otherSvg.addEventListener('click', function() {
                if (otherSpan.style.display === 'flex') {
                    otherSpan.style.display = 'none';
                    selectSpan.style.display = 'block';
                    selectElement.selectedIndex = 0;
                    if (isSelectRequired) {
                        selectElement.setAttribute('required', '');
                        otherInput.removeAttribute('required');
                    }
                }
            });
        }
    });
});
