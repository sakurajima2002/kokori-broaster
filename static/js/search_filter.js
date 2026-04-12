/**
 * Search Filter Module for Kokori Staff Panels
 * 
 * Handles real-time filtering of items (rows, list items, etc) based on 
 * data-attributes provided in the search input.
 */
document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('.generic-search-input');

    searchInputs.forEach(input => {
        const targetId = input.getAttribute('data-search-target');
        const itemSelector = input.getAttribute('data-search-item');
        const emptyStateId = input.getAttribute('data-search-empty');

        const container = document.getElementById(targetId);
        const emptyState = document.getElementById(emptyStateId);

        if (!container) return;

        input.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const items = container.querySelectorAll(itemSelector);
            let visibleCount = 0;

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.classList.remove('hidden');
                    visibleCount++;
                } else {
                    item.classList.add('hidden');
                }
            });

            // Toggle empty state and grid visibility
            if (visibleCount === 0) {
                container.classList.add('hidden');
                if (emptyState) emptyState.classList.remove('hidden');
            } else {
                container.classList.remove('hidden');
                if (emptyState) emptyState.classList.add('hidden');
            }
        });
    });
});
