/**
 * Kokori Artisan Admin - Accounts Controller
 * Manages user-related interactions in the staff panel.
 */

const AdminAccounts = {
    /**
     * Prepares and opens the staff toggle confirmation modal
     * @param {string} url - Action URL for the form
     * @param {string} email - User email for display
     * @param {boolean} isStaff - Current staff status
     */
    openStaffToggleModal: function(url, email, isStaff) {
        const modal = document.getElementById('staff-toggle-modal');
        if (!modal) return;

        // Update information
        const form = modal.querySelector('#staff-toggle-form');
        const emailSpan = modal.querySelector('#staff-toggle-email');
        const title = modal.querySelector('#staff-toggle-title');
        const subtitle = modal.querySelector('#staff-toggle-subtitle');
        const iconContainer = modal.querySelector('#staff-toggle-icon');
        const submitBtn = modal.querySelector('#staff-toggle-submit');

        if (form) form.action = url;
        if (emailSpan) emailSpan.textContent = email;

        if (isStaff) {
            title.textContent = '¿Remover de Staff?';
            subtitle.textContent = 'Este usuario perderá el acceso al panel administrativo pero mantendrá su cuenta.';
            iconContainer.className = 'h-20 w-20 bg-red-50 rounded-[2rem] flex items-center justify-center text-red-500 mb-6 border-4 border-white shadow-xl';
            iconContainer.innerHTML = '<svg class="h-9 w-9" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>';
            submitBtn.textContent = 'Sí, Remover Staff';
            submitBtn.className = 'flex-1 px-6 py-4 bg-red-600 text-white text-xs font-black uppercase tracking-widest rounded-2xl shadow-xl shadow-red-100 hover:bg-red-700 active:scale-95 transition-all';
        } else {
            title.textContent = '¿Promover a Staff?';
            subtitle.textContent = 'Este usuario tendrá acceso a herramientas administrativas según los roles que le asignes.';
            iconContainer.className = 'h-20 w-20 bg-purple-50 rounded-[2rem] flex items-center justify-center text-purple-600 mb-6 border-4 border-white shadow-xl';
            iconContainer.innerHTML = '<svg class="h-9 w-9" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>';
            submitBtn.textContent = 'Sí, Promover a Staff';
            submitBtn.className = 'flex-1 px-6 py-4 bg-purple-600 text-white text-xs font-black uppercase tracking-widest rounded-2xl shadow-xl shadow-purple-100 hover:bg-purple-700 active:scale-95 transition-all';
        }

        AdminModals.open('staff-toggle-modal');
    }
};
