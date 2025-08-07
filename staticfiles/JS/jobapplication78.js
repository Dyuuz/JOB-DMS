// Open application modal
function jbOpenApplyModal(jobTitle, companyName) {
    document.getElementById('jbModalJobTitle').textContent = jobTitle;
    document.getElementById('jbModalCompanyName').textContent = companyName;
    document.getElementById('jbApplyModal').style.display = 'flex';
}

// Close modal
function jbCloseModal() {
    document.getElementById('jbApplyModal').style.display = 'none';
}

// Handle form submission
document.getElementById('jbApplicationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Application submitted successfully!');
    jbCloseModal();
    // In a real app, you would send the data to your backend here
});

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    if (e.target === document.getElementById('jbApplyModal')) {
        jbCloseModal();
    }
});

// Search functionality
const jbSearchBox = document.querySelector('.jb-search-box');
jbSearchBox.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.jb-card').forEach(card => {
        const title = card.querySelector('.jb-position-title').textContent.toLowerCase();
        const company = card.querySelector('.jb-company-name').textContent.toLowerCase();
        card.style.display = (title.includes(searchTerm) || company.includes(searchTerm))
            ? ''
            : 'none';
    });
});

// Filter functionality
document.querySelectorAll('.jb-filter-dropdown').forEach(dropdown => {
    dropdown.addEventListener('change', jbFilterJobs);
});

function jbFilterJobs() {
    const typeFilter = document.querySelectorAll('.jb-filter-dropdown')[0].value;
    const locationFilter = document.querySelectorAll('.jb-filter-dropdown')[1].value;

    document.querySelectorAll('.jb-card').forEach(card => {
        const type = card.querySelector('.jb-type').textContent;
        const location = card.querySelector('.jb-detail-item:nth-child(1) span').textContent;

        const typeMatch = typeFilter === 'All Job Types' || type.includes(typeFilter);
        const locationMatch = locationFilter === 'All Locations' ||
                            location.toLowerCase().includes(locationFilter.toLowerCase());

        card.style.display = (typeMatch && locationMatch) ? '' : 'none';
    });
}
