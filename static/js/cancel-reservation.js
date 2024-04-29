document.addEventListener("DOMContentLoaded", function() {
    const cancelLinks = document.querySelectorAll('.cancel-link');

    cancelLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // This will prompt the user to confirm their action
            if (!confirm('Are you sure you want to cancel this reservation?')) {
                event.preventDefault(); // If they click 'Cancel', prevent the link from being followed
            }
        });
    });
});
