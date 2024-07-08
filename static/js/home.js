// static/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.favorite-button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const csrftoken = getCookie('csrftoken');

            fetch(`/add-to-favorites/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ item_id: itemId })
            })
            .then(response => response.text())
            .then(data => {
                if (data === 'Item added to favorites') {
                    this.textContent = 'В избранном';
                    this.classList.remove('btn-dark');
                    this.classList.add('btn-success');
                    this.disabled = true;
                } else {
                    alert(data);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

// Получение CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
