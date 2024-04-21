$(document).ready(function() {
    $('.btn-danger').click(function() {
        var userId = $(this).data('user-id');
        var isConfirmed = confirm('Are you sure you want to delete this?');
        if(isConfirmed) {
            $.ajax({
                url: '/delete/' + userId + '/',
                type: 'POST',
                data: { 'csrfmiddlewaretoken': '{{ csrf_token }}' },
                success: function(response) {
                    if(response.success) {
                        alert("User deleted successfully.");
                        window.location.reload(); // Reload the page to update the list
                    }
                }
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.custom-alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.display = 'none';
        }, 5000); // 5000 milliseconds = 5 seconds
    });
});