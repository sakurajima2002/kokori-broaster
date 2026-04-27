export function openCartModal() {
    const modal = document.getElementById('cart-modal');
    const backdrop = document.getElementById('cart-backdrop');
    const drawer = document.getElementById('cart-drawer');
    
    if (modal && backdrop && drawer) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        setTimeout(() => {
            backdrop.classList.remove('opacity-0');
            drawer.classList.remove('translate-x-full');
        }, 10);
    }
}

export function closeCartModal() {
    const backdrop = document.getElementById('cart-backdrop');
    const drawer = document.getElementById('cart-drawer');
    const modal = document.getElementById('cart-modal');
    
    if (backdrop && drawer && modal) {
        backdrop.classList.add('opacity-0');
        drawer.classList.add('translate-x-full');
        
        setTimeout(() => {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        }, 300);
    }
}

window.openCartModal = openCartModal;
window.closeCartModal = closeCartModal;

document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'cart-modal-content') {
        const root = event.detail.target.querySelector('[data-cart-count]');
        if (root) {
            const count = root.getAttribute('data-cart-count');
            const cartCountBadges = document.querySelectorAll('.cart-count-badge');
            cartCountBadges.forEach(badge => {
                badge.textContent = count;
                if (count === '0') {
                    badge.classList.add('hidden');
                } else {
                    badge.classList.remove('hidden');
                }
            });
        }
    }
});