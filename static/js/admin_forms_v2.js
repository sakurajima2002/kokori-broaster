
const AdminForms = {
    
    initImagePreview: function (inputId, previewImgId, placeholderId, fileNameId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewImgId);
        const placeholder = document.getElementById(placeholderId);
        const fileName = document.getElementById(fileNameId);

        if (!input || !preview) return;

        input.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    preview.src = event.target.result;
                    preview.classList.remove('hidden');
                    if (placeholder) placeholder.classList.add('hidden');
                    if (fileName) fileName.textContent = file.name;
                };

                reader.readAsDataURL(file);
            }
        });
    },

    
    initDynamicFormset: function (containerId, addBtnId, rowClass, totalFormsId, prefix, onUpdate) {
        const container = document.getElementById(containerId);
        const addButton = document.getElementById(addBtnId);
        const totalForms = document.getElementById(totalFormsId);

        if (!container || !addButton || !totalForms) return;

        addButton.addEventListener('click', function () {
            const forms = container.getElementsByClassName(rowClass);
            const count = forms.length;

            const newForm = forms[0].cloneNode(true);

            const regex = new RegExp(`${prefix}-(\\d+)-`, 'g');
            newForm.innerHTML = newForm.innerHTML.replace(regex, `${prefix}-${count}-`);

            newForm.querySelectorAll('input, select, textarea').forEach(i => {
                // Clear values for new forms
                if (i.type !== 'hidden') {
                    i.value = '';
                } else if (!i.name.includes('TOTAL_FORMS') && !i.name.includes('INITIAL_FORMS') && !i.name.includes('MIN_NUM_FORMS') && !i.name.includes('MAX_NUM_FORMS')) {
                    // Clear hidden IDs for cloned forms so they are treated as NEW records
                    i.value = '';
                }
            });

            container.appendChild(newForm);
            totalForms.value = count + 1;

            if (onUpdate) onUpdate();
        });

        container.addEventListener('click', function (e) {
            if (e.target.closest('.remove-row')) {
                const row = e.target.closest(`.${rowClass}`);
                const forms = container.getElementsByClassName(rowClass);

                if (forms.length > 1) {
                    row.remove();

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

        if (onUpdate) {
            container.addEventListener('change', onUpdate);
            onUpdate();
        }
    }
};

export { AdminForms };