/**
 * Kokori Artisan Admin - Modal Controller
 * A lightweight, reusable modal manager for the staff dashboard.
 */

const AdminModals = {
    /**
     * Open a modal by ID and handle body locking
     * @param {string} modalId 
     */
    open: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            if (modal.classList.contains('flex-col') || modal.classList.contains('items-center')) {
                // If it needs flex display, ensure it's set
                modal.classList.add('flex');
            }
            document.body.style.overflow = 'hidden';
            
            // Focus first input if exists
            const firstInput = modal.querySelector('input, textarea');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    },

    /**
     * Close a modal by ID and restore body scrolling
     * @param {string} modalId 
     */
    close: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            document.body.style.overflow = '';
        }
    },

    /**
     * Close all open modals
     */
    closeAll: function() {
        const modals = document.querySelectorAll('[id$="-modal"]'); // Assumes modals end with -modal
        modals.forEach(m => {
            m.classList.add('hidden');
            m.classList.remove('flex');
        });
        document.body.style.overflow = '';
    }
};

// Global Listeners
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        AdminModals.closeAll();
    }
});

// Auto-bind overlay clicks if data-close-on-overlay is present
document.addEventListener('click', (e) => {
    if (e.target.hasAttribute('data-modal-overlay')) {
        AdminModals.closeAll();
    }
});
