/**
 * Kokori Artisan Admin Bundle
 * Consolidates Modals, Suite Utilities, Account Management, and Product Logic.
 * Optimized with Event Delegation to avoid ReferenceErrors.
 */

// --- MODAL MANAGEMENT ---
export const AdminModals = {
    open: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            if (modal.classList.contains('flex-col') || modal.classList.contains('items-center')) {
                modal.classList.add('flex');
            }
            document.body.style.overflow = 'hidden';
            
            const firstInput = modal.querySelector('input, textarea');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    },

    close: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            document.body.style.overflow = '';
        }
    },

    closeAll: function() {
        const modals = document.querySelectorAll('[id$="-modal"]');
        modals.forEach(m => this.close(m.id));
        document.body.style.overflow = '';
    }
};

// --- SUITE UTILITIES ---
export const AdminSuite = {
    initToastAutoDismiss: function(delay = 5000) {
        const toasts = document.querySelectorAll('.toast-notification');
        toasts.forEach(t => {
            setTimeout(() => {
                t.style.opacity = '0';
                t.style.transform = 'translateX(50px) scale(0.9)';
                setTimeout(() => t.remove(), 500);
            }, delay);
        });
    },

    init: function() {
        this.initToastAutoDismiss();
    }
};

// --- ACCOUNT MANAGEMENT ---
export const AdminAccounts = {
    openStaffToggleModal: function(url, email, isStaff) {
        const modal = document.getElementById('staff-toggle-modal');
        if (!modal) return;

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

// --- PRODUCT MANAGEMENT ---
export const AdminProducts = {
    config: {
        categoryFormId: 'category-form',
        categoryModalId: 'category-modal',
        categoryTitleId: 'modal-title',
        categorySubtitleId: 'modal-subtitle',
        categorySubmitTextId: 'modal-submit-text',
        categoryNameId: 'modal-name',
        categoryDescId: 'modal-description',
        deleteCategoryModalId: 'delete-category-modal',
        deleteCategoryFormId: 'delete-category-form',
        deleteCategoryNameId: 'delete-category-name'
    },

    openCategoryCreate: function(createUrl) {
        const c = this.config;
        const form = document.getElementById(c.categoryFormId);
        if (form) {
            form.action = createUrl;
            document.getElementById(c.categoryTitleId).textContent = 'Nueva Categoría';
            document.getElementById(c.categorySubtitleId).textContent = 'Agrega una nueva clasificación para tus productos.';
            document.getElementById(c.categorySubmitTextId).textContent = 'Guardar Categoría';
            document.getElementById(c.categoryNameId).value = '';
            document.getElementById(c.categoryDescId).value = '';
            AdminModals.open(c.categoryModalId);
        }
    },

    openCategoryEdit: function(updateUrl, name, description) {
        const c = this.config;
        const form = document.getElementById(c.categoryFormId);
        if (form) {
            form.action = updateUrl;
            document.getElementById(c.categoryTitleId).textContent = 'Editar Categoría';
            document.getElementById(c.categorySubtitleId).textContent = 'Modifica los datos de esta categoría.';
            document.getElementById(c.categorySubmitTextId).textContent = 'Guardar Cambios';
            document.getElementById(c.categoryNameId).value = name;
            document.getElementById(c.categoryDescId).value = description;
            AdminModals.open(c.categoryModalId);
        }
    },

    openCategoryDelete: function(deleteUrl, name) {
        const c = this.config;
        const form = document.getElementById(c.deleteCategoryFormId);
        if (form) {
            form.action = deleteUrl;
            document.getElementById(c.deleteCategoryNameId).textContent = `"${name}"`;
            AdminModals.open(c.deleteCategoryModalId);
        }
    },

    updateIsCombo: function(containerId, toggleId, rowClass) {
        const container = document.getElementById(containerId);
        const toggle = document.getElementById(toggleId);
        if (!container || !toggle) return;
        const rows = container.getElementsByClassName(rowClass);
        let hasChild = false;
        for (let r of rows) {
            const sel = r.querySelector('select');
            if (sel && sel.value) { hasChild = true; break; }
        }
        toggle.checked = hasChild;
    },

    confirmProductDeletion: function(name, url) {
        const nameEl = document.getElementById('delete-item-name');
        const formEl = document.getElementById('delete-form');
        if (nameEl && formEl) {
            nameEl.innerText = `"${name.toUpperCase()}"`;
            formEl.action = url;
            AdminModals.open('delete-modal');
        }
    },

    // Combo-specific logic with refined animations
    openComboModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            setTimeout(() => {
                modal.classList.remove('opacity-0');
                const content = modal.querySelector('.scale-95');
                if (content) {
                    content.classList.remove('scale-95');
                    content.classList.add('scale-100');
                }
            }, 10);
            document.body.style.overflow = 'hidden';
        }
    },

    closeComboModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('opacity-0');
            const content = modal.querySelector('.scale-100');
            if (content) {
                content.classList.remove('scale-100');
                content.classList.add('scale-95');
            }
            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = '';
            }, 300);
        }
    }
};

// --- ROLE MANAGEMENT ---
export const AdminRoles = {
    config: {
        deleteRoleModalId: 'delete-role-modal',
        deleteRoleFormId: 'delete-role-form',
        deleteRoleNameId: 'delete-role-name'
    },

    openRoleDelete: function(deleteUrl, name) {
        const c = this.config;
        const form = document.getElementById(c.deleteRoleFormId);
        if (form) {
            form.action = deleteUrl;
            const nameEl = document.getElementById(c.deleteRoleNameId);
            if (nameEl) nameEl.textContent = `"${name}"`;
            AdminModals.open(c.deleteRoleModalId);
        }
    }
};

// --- GLOBAL ATTACHMENTS FOR LEGACY ONCLICK ---
window.AdminModals = AdminModals;
window.AdminSuite = AdminSuite;
window.AdminAccounts = AdminAccounts;
window.AdminProducts = AdminProducts;
window.AdminRoles = AdminRoles;

// --- DELEGATED LISTENERS ---
document.addEventListener('click', (e) => {
    // 1. Modal Close (any element with data-modal-close or its parents)
    const closeBtn = e.target.closest('[data-modal-close]');
    if (closeBtn) {
        const modalId = closeBtn.getAttribute('data-modal-close');
        // Specially handle combo modals if they need unique animations
        if (modalId && modalId.startsWith('staff-combo-')) {
            AdminProducts.closeComboModal(modalId);
        } else if (modalId) {
            AdminModals.close(modalId);
        } else {
            AdminModals.closeAll();
        }
        return;
    }

    // 2. Overlay Click
    if (e.target.hasAttribute('data-modal-overlay')) {
        AdminModals.closeAll();
        return;
    }

    // 3. Account Staff Toggle
    const staffToggleBtn = e.target.closest('[data-action="staff-toggle"]');
    if (staffToggleBtn) {
        const { url, email, isStaff } = staffToggleBtn.dataset;
        AdminAccounts.openStaffToggleModal(url, email, isStaff === 'true');
        return;
    }

    // 4. Product actions (Delete / Combo)
    const productDeleteBtn = e.target.closest('[data-action="product-delete"]');
    if (productDeleteBtn) {
        const { url, name } = productDeleteBtn.dataset;
        AdminProducts.confirmProductDeletion(name, url);
        return;
    }

    const comboOpenBtn = e.target.closest('[data-action="open-combo"]');
    if (comboOpenBtn) {
        const { modalId } = comboOpenBtn.dataset;
        AdminProducts.openComboModal(modalId);
        return;
    }

    // 5. Category CRUD
    const catActionBtn = e.target.closest('[data-action^="category-"]');
    if (catActionBtn) {
        const action = catActionBtn.dataset.action;
        const d = catActionBtn.dataset;

        if (action === 'category-create') {
            AdminProducts.openCategoryCreate(d.url);
        } else if (action === 'category-edit') {
            AdminProducts.openCategoryEdit(d.url, d.name, d.description);
        } else if (action === 'category-delete') {
            AdminProducts.openCategoryDelete(d.url, d.name);
        }
        return;
    }

    // 6. Role CRUD
    const roleElem = e.target.closest ? e.target.closest('[data-action^="role-"]') : null;
    if (roleElem) {
        const action = roleElem.dataset.action;
        const d = roleElem.dataset;

        if (action === 'role-delete') {
            const rolesHandler = window.AdminRoles || AdminRoles;
            if (rolesHandler && rolesHandler.openRoleDelete) {
                rolesHandler.openRoleDelete(d.url, d.name);
            }
        }
        return;
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') AdminModals.closeAll();
});

// Auto-init
document.addEventListener('DOMContentLoaded', () => {
    AdminSuite.init();
});
