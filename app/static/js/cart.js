document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.remove-item').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const key = this.dataset.key;
            fetch('/api/cart/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: key })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    this.closest('.card').remove();
                    location.reload();
                }
            })
            .catch(() => {});
        });
    });
});