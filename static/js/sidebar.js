export function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const openBtn = document.getElementById('open-sidebar-btn');
    const closeBtn = document.getElementById('close-sidebar-btn');
    const collapseBtn = document.getElementById('collapse-sidebar-btn');
    const collapseIcon = document.getElementById('collapse-icon');
    const expandIcon = document.getElementById('expand-icon');

    if (!sidebar || !overlay) return;

    function openMobileSidebar() {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }

    function closeMobileSidebar() {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }

    if (openBtn) openBtn.addEventListener('click', openMobileSidebar);
    if (closeBtn) closeBtn.addEventListener('click', closeMobileSidebar);
    overlay.addEventListener('click', closeMobileSidebar);

    const COLLAPSED_KEY = 'kokori_sidebar_collapsed';

    function applyCollapsedState(collapsed) {
        sidebar.classList.toggle('sidebar-collapsed-lg', collapsed);

        if (collapseIcon) collapseIcon.classList.toggle('hidden', collapsed);
        if (expandIcon) expandIcon.classList.toggle('hidden', !collapsed);
    }

    const savedCollapsed = localStorage.getItem(COLLAPSED_KEY) === 'true';
    applyCollapsedState(savedCollapsed);

    if (collapseBtn) {
        collapseBtn.addEventListener('click', () => {
            const isCollapsed = localStorage.getItem(COLLAPSED_KEY) === 'true';
            const next = !isCollapsed;
            localStorage.setItem(COLLAPSED_KEY, next);
            applyCollapsedState(next);
        });
    }

    window.addEventListener('resize', () => {
        if (window.innerWidth >= 1024) {
            overlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        } else {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }
    });
}

document.addEventListener('DOMContentLoaded', initSidebar);
