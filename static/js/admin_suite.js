/**
 * Kokori Artisan Admin - General Suite Utilities
 * General UI interactions, toast management, and dashboard-wide behavior.
 */

const AdminSuite = {
    /**
     * Auto-dismiss toast notifications after a delay
     * @param {number} delay 
     */
    initToastAutoDismiss: function(delay = 5000) {
        document.addEventListener('DOMContentLoaded', () => {
            const toasts = document.querySelectorAll('.toast-notification');
            toasts.forEach(t => {
                setTimeout(() => {
                    t.style.opacity = '0';
                    t.style.transform = 'translateX(50px) scale(0.9)';
                    setTimeout(() => t.remove(), 500);
                }, delay);
            });
        });
    },

    /**
     * Initialize generic UI behaviors
     */
    init: function() {
        this.initToastAutoDismiss();
        console.log('Artisan Admin Suite Initialized');
    }
};

// Initialize
AdminSuite.init();
