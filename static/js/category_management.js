export function initCategoryManagement(urls) {
    window.CATEGORY_URLS = urls;
}

export function handleCategoryErrors() {
    if (window.AdminModals) {
        window.AdminModals.open('category-modal');
    }
}