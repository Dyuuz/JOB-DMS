function statusupdate(applicantId, status) {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    if (applicantId && status) {
        // alert(status);
        // alert(applicantId);

        // Example: send update to server
        axios.patch(`/api/job/${applicantId}/status/`, {
            'status': status,
        }, {
            headers: {
                'X-CSRFToken': csrf_token
            }
        })
        .then(response => {
            showToast("Status updated to " + status);
        })
        .catch(error => {
            const errorMsg = error.response.data.error;
            showToast("Error updating status");
        });

    }
}


function showToast(message) {
  const toast = document.getElementById("status-toast");
  toast.textContent = message;
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 2000);
}

document.addEventListener('DOMContentLoaded', function() {
    const statusSelects = document.querySelectorAll('.applicanttrack-status-select');

    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const statusClass = this.classList[1];
            const initialStatus = this.dataset.initialStatus;
            const applicantId = this.dataset.applicantId;

            if (statusClass && initialStatus.includes('offer')) {
                showToast("Cannot change status after it's set to 'Offer'");
                this.value = `Offer-${applicantId}`;
                this.classList.add('applicanttrack-status-offer');
                return;
            }

            else if (statusClass && initialStatus.includes('interview') && this.value.includes('Applied')) {
                showToast("Cannot change status to 'Applied' after it's set to 'Interview'");
                this.value = `Interview-${applicantId}`;
                this.classList.add('applicanttrack-status-interview');
                return;
            }

            else if (statusClass && initialStatus.includes('rejected')) {
                showToast("Cannot change status after it's set to 'Rejected'");
                this.value = `Rejected-${applicantId}`;
                this.classList.add('applicanttrack-status-rejected');
                return;
            }

            this.classList.remove(
                'applicanttrack-status-applied',
                'applicanttrack-status-interview',
                'applicanttrack-status-offer',
                'applicanttrack-status-rejected'
            );

            value = this.value;
            const parts = value.split("-");
            const prefix = parts[0];
            const pk = parts[1];

            switch(prefix) {
                case 'Applied':
                    this.classList.add('applicanttrack-status-applied');
                    statusupdate(pk, prefix);
                    break;
                case 'Interview':
                    this.classList.add('applicanttrack-status-interview');
                    statusupdate(pk, prefix);
                    break;
                case 'Offer':
                    this.classList.add('applicanttrack-status-offer');
                    statusupdate(pk, prefix);
                    break;
                case 'Rejected':
                    this.classList.add('applicanttrack-status-rejected');
                    statusupdate(pk, prefix);
                    break;
            }
        });
    });

    // View button handler
    const viewButtons = document.querySelectorAll('.applicanttrack-view-btn');

    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const applicantName = this.closest('tr').querySelector('.applicanttrack-applicant-name').textContent;
            // alert('Viewing application for:', applicantName);
            // In a real app, this would open a modal or navigate to a detail page
        });
    });

    // Search and filter functionality
    const searchInput = document.querySelector('.applicanttrack-search-input');
    const filterSelects = document.querySelectorAll('.applicanttrack-filter-select');

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('.applicanttrack-table tbody tr');

        rows.forEach(row => {
            const name = row.querySelector('.applicanttrack-applicant-name').textContent.toLowerCase();
            const email = row.querySelector('.applicanttrack-applicant-email').textContent.toLowerCase();

            if (name.includes(searchTerm) || email.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
