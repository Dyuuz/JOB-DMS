// Update the event listeners
document.querySelectorAll('.fa-eye').forEach(icon => {
    icon.addEventListener('click', (e) => {
        e.preventDefault();
        const jobId = e.target.closest('tr').dataset.id;
        // Open detailed view modal
        alert(`Viewing details for job ID: ${jobId}`);
        console.log('Viewing details for job ID:', jobId);
    });
});

document.querySelectorAll('.fa-user-times').forEach(icon => {
    icon.addEventListener('click', async (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to withdraw this application?')) {
            const row = e.target.closest('tr');
            // API call to withdraw application
            console.log('Withdrawing application:', row.cells[0].textContent);
            row.remove();
        }
    });
});
