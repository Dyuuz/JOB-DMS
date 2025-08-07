// DOM Elements
const globalModal = document.getElementById('globalModal');
const modalMessage = document.getElementById('modalMessage');
const modalIcon = document.getElementById('modalIcon');
const modalClose = document.getElementById('modalClose');

// Show alert function
function showGlobalAlert(message, type = 'info') {
    // Set message
    modalMessage.textContent = message;

    // Set icon type
    modalIcon.className = 'modal-icon-global';
    if (type === 'success') {
        modalIcon.classList.add('modal-icon-success');
        modalIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        `;
    } else if (type === 'error') {
        modalIcon.classList.add('modal-icon-error');
        modalIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        `;
    } else {
        modalIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
        `;
    }

    // Show modal
    globalModal.classList.add('is-active');
}

// Close modal
function closeGlobalModal() {
    globalModal.classList.remove('is-active');
}

// Event listeners
modalClose.addEventListener('click', closeGlobalModal);
globalModal.addEventListener('click', (e) => {
    if (e.target === globalModal) closeGlobalModal();
});

// Dialog control functions
function showDeleteDialog(filename, documentId) {
    const dialog = document.getElementById('deleteDialog');
    const message = document.getElementById('dialogMessage');

    message.textContent = `"${filename}" will be permanently deleted. This action cannot be undone.`;
    dialog.classList.add('active');

    // Store the document ID for later use
    dialog.setAttribute('data-document-id', documentId);
}

function hideDeleteDialog() {
    document.getElementById('deleteDialog').classList.remove('active');
}

// Event listeners
document.getElementById('cancelBtn').addEventListener('click', hideDeleteDialog);
document.getElementById('confirmBtn').addEventListener('click', function() {
    const documentId = document.getElementById('deleteDialog').getAttribute('data-document-id');
    // Add your delete logic here
    deleteDoc(documentId)
    hideDeleteDialog();
});

// Close when clicking outside dialog
document.getElementById('deleteDialog').addEventListener('click', function(e) {
    if (e.target === this) {
        hideDeleteDialog();
    }
});

function deleteDoc(id) {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // const docdelete = document.querySelector(`.file-name[data-id='${id}']`);
    const docCard = document.querySelector(`.doc-card-new[data-id='${id}']`);
    //const docdelete = document.querySelector('.doc-name');
    //const dat = docdelete.dataset.id;
    //alert(docdelete.textContent);

    axios.delete(`/api/document/${id}/delete/`, {
    headers: {
        'X-CSRFToken': csrf_token
    }
    })
    .then(response => {
        docCard.style.display = 'none';
    })
    .catch(error => {
        const errorMsg = error.response.data.error;
        if (errorMsg.includes('Cannot delete some instances of model')) {
            const message = 'This document cannot be deleted because it is associated with your job records.';
            showGlobalAlert(message, type = 'error')
        }
        else{
            const message = 'An error occurred while deleting the document. Try again later.';
            showGlobalAlert(message, type = 'error')
        }
    });
}

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
