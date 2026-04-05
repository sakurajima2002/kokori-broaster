/**
 * Kokori Artisan Admin - General Form Utilities
 * Universal handlers for image previews and dynamic formsets.
 */

const AdminForms = {
    /**
     * Initialize Image Preview for a file input
     * @param {string} inputId 
     * @param {string} previewImgId 
     * @param {string} placeholderId 
     * @param {string} fileNameId 
     */
    initImagePreview: function(inputId, previewImgId, placeholderId, fileNameId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewImgId);
        const placeholder = document.getElementById(placeholderId);
        const fileName = document.getElementById(fileNameId);

        if (!input || !preview) return;

        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    preview.src = event.target.result;
                    preview.classList.remove('hidden');
                    if (placeholder) placeholder.classList.add('hidden');
                    if (fileName) fileName.textContent = file.name;
                };
                reader.readAsDataURL(file);
            }
        });
    },

    /**
     * Initialize Dynamic Formset (Add/Remove rows)
     * @param {string} containerId 
     * @param {string} addBtnId 
     * @param {string} rowClass 
     * @param {string} totalFormsId 
     * @param {string} prefix 
     * @param {Function} onUpdate - Optional callback after adding/removing
     */
    initDynamicFormset: function(containerId, addBtnId, rowClass, totalFormsId, prefix, onUpdate) {
        const container = document.getElementById(containerId);
        const addButton = document.getElementById(addBtnId);
        const totalForms = document.getElementById(totalFormsId);

        if (!container || !addButton || !totalForms) return;

        // Add row
        addButton.addEventListener('click', function() {
            const forms = container.getElementsByClassName(rowClass);
            const count = forms.length;
            
            // Clone first row
            const newForm = forms[0].cloneNode(true);
            
            // Update indices
            const regex = new RegExp(`${prefix}-(\\d+)-`, 'g');
            newForm.innerHTML = newForm.innerHTML.replace(regex, `${prefix}-${count}-`);
            
            // Clear inputs
            newForm.querySelectorAll('input, select, textarea').forEach(i => {
                if (i.type !== 'hidden') i.value = '';
            });

            container.appendChild(newForm);
            totalForms.value = count + 1;
            
            if (onUpdate) onUpdate();
        });

        // Remove row
        container.addEventListener('click', function(e) {
            if (e.target.closest('.remove-row')) {
                const row = e.target.closest(`.${rowClass}`);
                const forms = container.getElementsByClassName(rowClass);
                
                if (forms.length > 1) {
                    row.remove();
                    
                    // Re-index all rows
                    const currentForms = Array.from(container.getElementsByClassName(rowClass));
                    totalForms.value = currentForms.length;
                    
                    currentForms.forEach((f, idx) => {
                        const regex = new RegExp(`${prefix}-(\\d+)-`, 'g');
                        f.innerHTML = f.innerHTML.replace(regex, `${prefix}-${idx}-`);
                    });
                }
                
                if (onUpdate) onUpdate();
            }
        });

        // Initial update
        if (onUpdate) {
            container.addEventListener('change', onUpdate);
            onUpdate();
        }
    }
};
