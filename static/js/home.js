// static/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.favorite-button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const csrftoken = getCookie('csrftoken');
            const button = this;

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
                    Swal.fire({
                        icon: 'success',
                        title: 'Добавлено в избранное',
                        showConfirmButton: false,
                        timer: 1500,
                        toast: true,
                        position: 'top-end',
                        background: '#343a40',
                        color: '#ffffff',
                        showClass: {
                            popup: 'animate__animated animate__fadeInRight'
                        },
                        hideClass: {
                            popup: 'animate__animated animate__fadeOutRight'
                        }
                    });
                    button.textContent = 'В избранном';
                    button.disabled = true;
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Ошибка',
                        text: data,
                        toast: true,
                        position: 'top-end',
                        background: '#f8d7da',
                        color: '#721c24',
                        showClass: {
                            popup: 'animate__animated animate__fadeInRight'
                        },
                        hideClass: {
                            popup: 'animate__animated animate__fadeOutRight'
                        }
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Ошибка',
                    text: 'Что-то пошло не так!',
                    toast: true,
                    position: 'top-end',
                    background: '#f8d7da',
                    color: '#721c24',
                    showClass: {
                        popup: 'animate__animated animate__fadeInRight'
                    },
                    hideClass: {
                        popup: 'animate__animated animate__fadeOutRight'
                    }
                });
                console.error('Error:', error);
            });
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
