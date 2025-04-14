// View Details button functionality
document.querySelectorAll('.view-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const row = e.target.closest('tr');
        const company = row.cells[0].textContent;
        const position = row.cells[1].textContent;
        alert(`Viewing details for:\n${position} at ${company}`);
        // In a real app, this would open a modal or navigate to a detail page
    });
});

// Withdraw Application button functionality
document.querySelectorAll('.withdraw-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        if (confirm('Are you sure you want to withdraw this application?')) {
            const row = e.target.closest('tr');
            const company = row.cells[0].textContent;
            console.log(`Withdrawing application to ${company}`);
            // In a real app, this would make an API call
            row.style.opacity = '0.5';
            row.remove();
        }
    });
});

// Search functionality
const searchBox = document.querySelector('.search-box');
searchBox.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.applications-table tbody tr').forEach(row => {
        const company = row.cells[0].textContent.toLowerCase();
        const position = row.cells[1].textContent.toLowerCase();
        row.style.display = (company.includes(searchTerm) || position.includes(searchTerm))
            ? ''
            : 'none';
    });
});

// Filter dropdown functionality
const filterDropdown = document.querySelector('.filter-dropdown');
filterDropdown.addEventListener('change', (e) => {
    const filterValue = e.target.value;
    document.querySelectorAll('.applications-table tbody tr').forEach(row => {
        if (filterValue === 'All Statuses') {
            row.style.display = '';
            return;
        }

        const status = row.cells[3].textContent.toLowerCase();
        const filter = filterValue.toLowerCase();
        row.style.display = status.includes(filter) ? '' : 'none';
    });
});
