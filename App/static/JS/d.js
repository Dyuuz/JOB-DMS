document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.documents-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const searchInput = document.querySelector('.search-input');
    const sortDropdown = document.querySelector('.sort-dropdown');
    const sortableHeaders = table.querySelectorAll('th.sortable');
    const emptyState = document.getElementById('empty-state');

    // Helper function to show/hide empty state
    function toggleEmptyState(show) {
        emptyState.style.display = show ? 'block' : 'none';
        tbody.style.display = show ? 'none' : 'table-row-group';
    }

    // Search functionality
    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();
        let hasMatches = false;

        rows.forEach(row => {
            const name = row.cells[0].textContent.toLowerCase();
            const type = row.cells[3].textContent.toLowerCase();
            const match = name.includes(query) || type.includes(query);
            row.style.display = match ? '' : 'none';
            if (match) hasMatches = true;
        });

        toggleEmptyState(!hasMatches);
    });

    // Sort functionality
    function sortTable(sortBy, direction) {
        const index = Array.from(table.querySelectorAll('th')).findIndex(th => th.dataset.sort === sortBy);
        if (index === -1) return;

        const sortedRows = rows.sort((a, b) => {
            const aValue = a.cells[index].textContent;
            const bValue = b.cells[index].textContent;

            // Special handling for dates and sizes
            if (sortBy === 'date') {
                return direction === 'asc'
                    ? new Date(aValue) - new Date(bValue)
                    : new Date(bValue) - new Date(aValue);
            } else if (sortBy === 'size') {
                const parseSize = (size) => {
                    const [num, unit] = size.split(' ');
                    const multiplier = unit === 'KB' ? 1024 : unit === 'MB' ? 1024 * 1024 : unit === 'GB' ? 1024 * 1024 * 1024 : 1;
                    return parseFloat(num) * multiplier;
                };
                return direction === 'asc'
                    ? parseSize(aValue) - parseSize(bValue)
                    : parseSize(bValue) - parseSize(aValue);
            } else {
                return direction === 'asc'
                    ? aValue.localeCompare(bValue)
                    : bValue.localeCompare(aValue);
            }
        });

        // Clear and re-add sorted rows
        tbody.innerHTML = '';
        sortedRows.forEach(row => tbody.appendChild(row));
    }

    // Dropdown sort
    sortDropdown.addEventListener('change', function() {
        const [sortBy, direction] = this.value.split('-');
        sortTable(sortBy, direction);
        updateSortUI(sortBy, direction);
    });

    // Header click sort
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const sortBy = this.dataset.sort;
            let direction = 'asc';

            if (this.classList.contains('sorted-asc')) {
                direction = 'desc';
            } else if (this.classList.contains('sorted-desc')) {
                direction = 'asc';
            }

            sortDropdown.value = `${sortBy}-${direction}`;
            sortTable(sortBy, direction);
            updateSortUI(sortBy, direction);
        });
    });

    // Update sort UI indicators
    function updateSortUI(sortBy, direction) {
        sortableHeaders.forEach(header => {
            header.classList.remove('sorted-asc', 'sorted-desc');

            if (header.dataset.sort === sortBy) {
                header.classList.add(direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
                const icon = header.querySelector('.sort-icon');
                icon.className = direction === 'asc'
                    ? 'fas fa-sort-up sort-icon'
                    : 'fas fa-sort-down sort-icon';
            }
        });
    }

    // Initialize with default sort
    sortTable('date', 'desc');
    updateSortUI('date', 'desc');
});
