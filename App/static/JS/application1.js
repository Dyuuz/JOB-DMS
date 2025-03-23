// script.js
document.addEventListener('DOMContentLoaded', function () {
    const pages = document.querySelectorAll('.form-page');
    const currentPageElement = document.getElementById('current-page');
    const totalPagesElement = document.getElementById('total-pages');
    const progressBar = document.getElementById('progress');
    let currentPage = 0;

    // Set total pages
    totalPagesElement.textContent = pages.length;

    // Show the first page initially
    showPage(currentPage);
    updateProgressBar();

    // Add event listeners to buttons
    document.querySelectorAll('.next-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            if (validatePage(currentPage)) {
                currentPage++;
                showPage(currentPage);
                updatePageIndicator();
                updateProgressBar();
            }
        });
    });

    document.querySelectorAll('.prev-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            currentPage--;
            showPage(currentPage);
            updatePageIndicator();
            updateProgressBar();
        });
    });

    document.querySelector('.submit-btn').addEventListener('click', function (e) {
        e.preventDefault();
        if (validatePage(currentPage)) {
            alert('Form submitted successfully!');
            // Here you can add code to submit the form data
        }
    });

    function showPage(pageIndex) {
        pages.forEach((page, index) => {
            if (index === pageIndex) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });
    }

    function validatePage(pageIndex) {
        const inputs = pages[pageIndex].querySelectorAll('.input-field');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '#ccc';
            }
        });

        if (!isValid) {
            toastr.options.preventDuplicates = true;
            toastr.clear();
            toastr.error("Please fill out all fields before proceeding.");
            // alert();
        }

        return isValid;
    }

    function updatePageIndicator() {
        currentPageElement.textContent = currentPage + 1;
    }

    function updateProgressBar() {
        const progress = ((currentPage + 1) / pages.length) * 100;
        progressBar.style.width = `${progress}%`;
    }
});
