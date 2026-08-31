// VegFood Main JS Interactivity (2026 UI/UX)

document.addEventListener('DOMContentLoaded', () => {
    // --- Mobile Drawer Controls ---
    const hamburger = document.querySelector('.hamburger');
    const mobileDrawer = document.getElementById('mobile-nav-drawer');
    const mobileBackdrop = document.getElementById('mobile-nav-backdrop');
    const mobileClose = document.querySelector('.mobile-nav-close');

    if (hamburger && mobileDrawer && mobileBackdrop) {
        const toggleMobileNav = (open) => {
            if (open) {
                mobileDrawer.classList.add('open');
                mobileBackdrop.classList.add('open');
                document.body.style.overflow = 'hidden';
            } else {
                mobileDrawer.classList.remove('open');
                mobileBackdrop.classList.remove('open');
                document.body.style.overflow = '';
            }
        };

        hamburger.addEventListener('click', () => toggleMobileNav(true));
        mobileClose.addEventListener('click', () => toggleMobileNav(false));
        mobileBackdrop.addEventListener('click', () => toggleMobileNav(false));
    }

    // --- Toast / Message dismiss timer ---
    const toasts = document.querySelectorAll('.message-toast');
    toasts.forEach(toast => {
        // Automatically remove toast after 4 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    });

    // Helper to trigger a client-side Toast Alert
    window.showToast = (message, tags = 'success') => {
        let container = document.querySelector('.messages-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'messages-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `message-toast ${tags}`;
        toast.innerHTML = `
            <span class="message-text">${message}</span>
            <button class="close-toast">&times;</button>
        `;

        toast.querySelector('.close-toast').addEventListener('click', () => {
            toast.remove();
        });

        container.appendChild(toast);

        // Auto remove
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    };

    // --- CSRF Cookie Helper ---
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

    // --- AJAX Cart Updates ---
    const cartUpdateForms = document.querySelectorAll('.ajax-cart-update-form');
    cartUpdateForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = form.action;
            const formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update navigation badges
                    const badges = document.querySelectorAll('.cart-badge');
                    badges.forEach(badge => {
                        badge.textContent = data.total_items;
                        badge.style.display = data.total_items > 0 ? 'inline-block' : 'none';
                    });

                    // If we are on the cart page, update the DOM elements
                    const row = form.closest('.cart-item-row');
                    if (row) {
                        const quantityDisplay = row.querySelector('.qty-value');
                        const itemTotalDisplay = row.querySelector('.item-total-val');
                        
                        if (quantityDisplay) quantityDisplay.textContent = data.quantity;
                        if (itemTotalDisplay) itemTotalDisplay.textContent = `$${data.item_total.toFixed(2)}`;

                        if (data.quantity === 0) {
                            row.remove();
                            // If cart becomes empty, reload to show empty state
                            if (data.total_items === 0) {
                                window.location.reload();
                            }
                        }
                    }

                    // Update summary prices
                    const subtotalVal = document.getElementById('summary-subtotal');
                    const deliveryVal = document.getElementById('summary-delivery');
                    const grandVal = document.getElementById('summary-grand-total');

                    if (subtotalVal) subtotalVal.textContent = `$${data.subtotal.toFixed(2)}`;
                    if (deliveryVal) {
                        deliveryVal.textContent = data.delivery_charge > 0 ? `$${data.delivery_charge.toFixed(2)}` : 'FREE';
                    }
                    if (grandVal) grandVal.textContent = `$${data.grand_total.toFixed(2)}`;

                    window.showToast("Cart updated successfully!", "success");
                } else {
                    window.showToast("Error updating cart.", "error");
                }
            })
            .catch(err => {
                console.error(err);
                window.showToast("Error communicating with server.", "error");
            });
        });
    });
});
