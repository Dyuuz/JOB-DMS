document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const companyCards = Array.from(document.querySelectorAll('.company-card'));

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();

        companyCards.forEach(card => {
            const name = card.querySelector('.company-name').textContent.toLowerCase();
            const industry = card.querySelector('.company-industry').textContent.toLowerCase();
            const role = card.querySelector('.meta-item').textContent.toLowerCase();

            if (name.includes(searchTerm) || industry.includes(searchTerm) || role.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        // Check if all cards are hidden
        const visibleCards = companyCards.filter(card => card.style.display !== 'none');
        const emptyState = document.querySelector('.empty-state');

        if (visibleCards.length === 0) {
            if (!emptyState) {
                const grid = document.getElementById('companiesGrid');
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'empty-state';
                emptyDiv.innerHTML = `
                    <div class="empty-icon">
                        <i class="fas fa-building-circle-exclamation"></i>
                    </div>
                    <h3 class="empty-title">No Companies Found</h3>
                    <p class="empty-text">Try adjusting your search to find your companies.</p>
                `;
                grid.appendChild(emptyDiv);
            }
        } else if (emptyState) {
            emptyState.remove();
        }
    });
});
