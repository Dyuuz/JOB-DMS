const suggestionB = document.querySelector('.suggestion-box');
const portfolioB = document.querySelector('.portfolio-box');
const experienceB = document.querySelector('.experience-box');
const phoneB = document.querySelector('.phone-box');

suggestionB.addEventListener("click", function(e) {
  if (e.target && e.target.innerText !== "Preparing suggestions..." && e.target.innerText !== "Error fetching suggestion.") {
    const inputsug = document.getElementById('id_cover_letter');
    inputsug.value = e.target.innerText.trim();
    suggestionB.style.display = 'none';
    inputsug.focus();
  }
});

portfolioB.addEventListener("click", function(e) {
  if (e.target && e.target.innerText !== "Preparing data..." && e.target.innerText !== "Error fetching suggestion.") {
    const inputsug = document.getElementById('id_portfolio');
    inputsug.value = e.target.innerText.trim();
    portfolioB.style.display = 'none';
    inputsug.focus();
  }
});

experienceB.addEventListener("click", function(e) {
  if (e.target && e.target.innerText !== "Preparing data..." && e.target.innerText !== "Error fetching suggestion.") {
    const inputsug = document.getElementById('id_experience');
    inputsug.value = e.target.innerText.trim();
    experienceB.style.display = 'none';
    inputsug.focus();
  }
});

phoneB.addEventListener("click", function(e) {
  if (e.target && e.target.innerText !== "Preparing data..." && e.target.innerText !== "Error fetching suggestion.") {
    const inputsug = document.getElementById('id_phone');
    inputsug.value = e.target.innerText.trim();
    phoneB.style.display = 'none';
    inputsug.focus();
  }
});




document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('id_cover_letter');
    const portfolio = document.getElementById('id_portfolio');
    const experience = document.getElementById('id_experience');
    const phone = document.getElementById('id_phone');

    input.addEventListener('input', function () {
        const inputlength = input.value.length;
        const suggestionBox = document.querySelector('.suggestion-box');
        let timeoutId = null;

        if (inputlength > 10) {
            suggestionBox.style.display = 'block';
            suggestionBox.innerText = "Preparing suggestions...";

            // Clear previous timer
            clearTimeout(timeoutId);

            // Set new debounce timer
            timeoutId = setTimeout(() => {
                axios.get('/suggest-cover-letter', {
                    params: { text: input.value }
                })
                .then(response => {
                    suggestionBox.innerText = response.data.suggestion || "No suggestion found.";
                })
                .catch(error => {
                    suggestionBox.innerText = "Error fetching suggestion.";
                    console.error('Error fetching data:', error);
                });
            }, 5000);  // Delay in milliseconds
        } else {
            // alert("Please enter more than 10 characters to get suggestions.");
        }
    });

    portfolio.addEventListener('input', function () {
        const inputlength = portfolio.value.length;
        const suggestionBox = document.querySelector('.portfolio-box');
        const suggestionContent = suggestionBox.innerText;
        // alert(suggestionContent);

        // if (inputlength > 2 && suggestionContent !== "https://github.com/Dyuuz" && portfolio.value !== "https://github.com/Dyuuz") {
        if (inputlength  > 2 ) {
            suggestionBox.style.display = 'block';
            suggestionBox.innerText = "Preparing data...";

            // Set new debounce timer
            timeoutId = setTimeout(() => {
                axios.get('/suggest-portfolio')
                .then(response => {
                    suggestionBox.innerText = response.data.suggestion || "No suggestion found.";
                })
                .catch(error => {
                    suggestionBox.innerText = "Error fetching suggestion.";
                    console.error('Error fetching data:', error);
                });
            }, 5000);
        } else {
            // alert("Please enter more than 10 characters to get suggestions.");
        }
    });

    experience.addEventListener('input', function () {
        const inputlength = experience.value.length;
        const suggestionBox = document.querySelector('.experience-box');
        const suggestionContent = suggestionBox.innerText;

        if (inputlength >= 1) {
            suggestionBox.style.display = 'block';
            suggestionBox.innerText = "Preparing data...";

            // Set new debounce timer
            timeoutId = setTimeout(() => {
                axios.get('/suggest-experience')
                .then(response => {
                    suggestionBox.innerText = response.data.suggestion || "No suggestion found.";
                })
                .catch(error => {
                    suggestionBox.innerText = "Error fetching suggestion.";
                    console.error('Error fetching data:', error);
                });
            }, 5000);
        } else {
            // alert("Please enter more than 10 characters to get suggestions.");
        }
    });

    phone.addEventListener('input', function () {
        const inputlength = phone.value.length;
        const suggestionBox = document.querySelector('.phone-box');
        const suggestionContent = suggestionBox.innerText;

        if (inputlength > 1 ) {
            suggestionBox.style.display = 'block';
            suggestionBox.innerText = "Preparing data...";

            // Set new debounce timer
            timeoutId = setTimeout(() => {
                axios.get('/suggest-phone')
                .then(response => {
                    suggestionBox.innerText = response.data.suggestion || "No suggestion found.";
                })
                .catch(error => {
                    suggestionBox.innerText = "Error fetching suggestion.";
                    console.error('Error fetching data:', error);
                });
            }, 5000);
        } else {
            // alert("Please enter more than 10 characters to get suggestions.");
        }
    });

});
