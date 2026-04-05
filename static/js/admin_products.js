/**
 * Kokori Artisan Admin - Inventory Logic
 * Specialized handlers for Products, Categories, and Combo detection.
 */

const AdminProducts = {
    /**
     * Category Modal Configuration
     */
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

    /**
     * Open Category Creation Modal
     * @param {string} createUrl 
     */
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

    /**
     * Open Category Edit Modal
     * @param {string} updateUrl 
     * @param {string} name 
     * @param {string} description 
     */
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

    /**
     * Open Category Delete Modal
     * @param {string} deleteUrl 
     * @param {string} name 
     */
    openCategoryDelete: function(deleteUrl, name) {
        const c = this.config;
        const form = document.getElementById(c.deleteCategoryFormId);
        
        if (form) {
            form.action = deleteUrl;
            document.getElementById(c.deleteCategoryNameId).textContent = `"${name}"`;
            AdminModals.open(c.deleteCategoryModalId);
        }
    },

    /**
     * Update Is Combo Toggle
     * @param {string} containerId 
     * @param {string} toggleId 
     * @param {string} rowClass 
     */
    updateIsCombo: function(containerId, toggleId, rowClass) {
        const container = document.getElementById(containerId);
        const toggle = document.getElementById(toggleId);
        
        if (!container || !toggle) return;
        
        const rows = container.getElementsByClassName(rowClass);
        let hasChild = false;
        
        for (let r of rows) {
            const sel = r.querySelector('select');
            if (sel && sel.value) {
                hasChild = true;
                break;
            }
        }
        
        toggle.checked = hasChild;
    },

    /**
     * Product Deletion Confirmation
     * @param {string} name 
     * @param {string} url 
     */
    confirmProductDeletion: function(name, url) {
        const nameEl = document.getElementById('delete-item-name');
        const formEl = document.getElementById('delete-form');
        
        if (nameEl && formEl) {
            nameEl.innerText = `"${name.toUpperCase()}"`;
            formEl.action = url;
            AdminModals.open('delete-modal');
        }
    }
};
