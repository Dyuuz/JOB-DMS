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
            const messageCell = document.querySelector(`td.status-message[data-applicant-id="${applicantId}"]`);
            if (status === 'Interview') {
                messageCell.textContent = response.data.next_step;
            }
        })
        .catch(error => {
            const errorMsg = error.response.data.error;
            showToast(errorMsg);
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
            // alert(`From: ${initialStatus} to ${this.value}`);

            if (statusClass && statusClass.includes('offer')) {
                showToast("Cannot change status after it's set to 'Offer'");
                this.value = `Offer-${applicantId}`;
                // alert(`Failed to change from offer ${this.value}`);
                return;
            }

            else if (statusClass && statusClass.includes('interview') && this.value.includes('Applied')) {
                showToast("Cannot change status to 'Applied' after it's set to 'Interview'");
                this.value = `Interview-${applicantId}`;
                // alert(`Failed to change to interview ${this.value}`);
                return;
            }

            else if (statusClass && statusClass.includes('rejected')) {
                showToast("Cannot change status after it's set to 'Rejected'");
                this.value = `Rejected-${applicantId}`;
                // alert(`Failed to change from rejected ${this.value}`);
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
            const selectElement = document.querySelector(`select[data-applicant-id="${pk}"]`);

            switch(prefix) {
                case 'Applied':
                    this.classList.add('applicanttrack-status-applied');
                    statusupdate(pk, prefix);
                    selectElement.dataset.initialStatus = prefix;
                    selectElement.value = `${prefix}-${pk}`;
                    break;
                case 'Interview':
                    this.classList.add('applicanttrack-status-interview');
                    statusupdate(pk, prefix);
                    selectElement.dataset.initialStatus = prefix;
                    selectElement.value = `${prefix}-${pk}`;
                    break;
                case 'Offer':
                    this.classList.add('applicanttrack-status-offer');
                    statusupdate(pk, prefix);
                    selectElement.dataset.initialStatus = prefix;
                    selectElement.value = `${prefix}-${pk}`;
                    break;
                case 'Rejected':
                    this.classList.add('applicanttrack-status-rejected');
                    statusupdate(pk, prefix);
                    selectElement.dataset.initialStatus = prefix;
                    selectElement.value = `${prefix}-${pk}`;
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
