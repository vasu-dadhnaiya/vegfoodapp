document.addEventListener('DOMContentLoaded', function() {
    // Image Preview Handler
    const imageInputs = document.querySelectorAll('.form-file-input');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewContainer = document.getElementById('image-preview-container');
            const previewImg = document.getElementById('image-preview');
            
            if (file && previewContainer && previewImg) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Delete Confirmation Modal Handler
    const deleteTriggers = document.querySelectorAll('.trigger-delete-modal');
    const modalBackdrop = document.getElementById('delete-modal-backdrop');
    const deleteForm = document.getElementById('modal-delete-form');
    const modalItemName = document.getElementById('modal-item-name');
    const cancelBtn = document.getElementById('modal-cancel-btn');

    if (deleteTriggers && modalBackdrop && deleteForm) {
        deleteTriggers.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const targetUrl = this.getAttribute('data-delete-url');
                const itemName = this.getAttribute('data-item-name') || 'this item';
                
                deleteForm.setAttribute('action', targetUrl);
                if (modalItemName) {
                    modalItemName.textContent = itemName;
                }
                modalBackdrop.classList.add('active');
            });
        });

        if (cancelBtn) {
            cancelBtn.addEventListener('click', function() {
                modalBackdrop.classList.remove('active');
            });
        }

        modalBackdrop.addEventListener('click', function(e) {
            if (e.target === modalBackdrop) {
                modalBackdrop.classList.remove('active');
            }
        });
    }

    // Toggle Availability AJAX Handler
    const toggleBtns = document.querySelectorAll('.btn-toggle-availability');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href') || this.getAttribute('data-url');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const badge = this.querySelector('.status-pill') || this;
                    if (data.is_available) {
                        badge.className = 'status-pill instock';
                        badge.textContent = 'Available';
                    } else {
                        badge.className = 'status-pill outofstock';
                        badge.textContent = 'Unavailable';
                    }
                }
            })
            .catch(err => console.error('Error toggling status:', err));
        });
    });
});
