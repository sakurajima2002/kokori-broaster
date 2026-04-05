/**
 * Sidebar Handler for Kokori Staff Panel
 * - Mobile: toggle slide-in/out with overlay
 * - Desktop: collapse to icon-only mode, persisted in localStorage
 */

document.addEventListener('DOMContentLoaded', function () {
    const sidebar      = document.getElementById('sidebar');
    const overlay      = document.getElementById('sidebar-overlay');
    const openBtn      = document.getElementById('open-sidebar-btn');
    const closeBtn     = document.getElementById('close-sidebar-btn');
    const collapseBtn  = document.getElementById('collapse-sidebar-btn');
    const collapseIcon = document.getElementById('collapse-icon');
    const expandIcon   = document.getElementById('expand-icon');
    const layout       = document.getElementById('staff-layout');

    if (!sidebar || !overlay) return;

    // ─── Mobile Toggle ─────────────────────────────────────────────────

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

    if (openBtn)  openBtn.addEventListener('click', openMobileSidebar);
    if (closeBtn) closeBtn.addEventListener('click', closeMobileSidebar);
    overlay.addEventListener('click', closeMobileSidebar);

    // ─── Desktop Collapse ───────────────────────────────────────────────

    const COLLAPSED_KEY = 'kokori_sidebar_collapsed';

    function applyCollapsedState(collapsed) {
        if (collapsed) {
            // Shrink sidebar
            sidebar.classList.remove('lg:w-72');
            sidebar.classList.add('lg:w-[4.5rem]');

            // Hide text labels
            document.querySelectorAll('.sidebar-label').forEach(el => {
                el.classList.add('opacity-0', 'w-0', 'overflow-hidden');
                el.style.maxWidth = '0';
            });
            // Hide section labels
            document.querySelectorAll('.sidebar-section-label').forEach(el => {
                el.classList.add('opacity-0', 'h-0', 'py-0', 'my-0', 'overflow-hidden');
                el.style.maxHeight = '0';
            });

            // Center icons in links
            document.querySelectorAll('.sidebar-link').forEach(el => {
                el.classList.add('justify-center');
                el.classList.remove('space-x-3');
            });

            // Switch icons
            if (collapseIcon) collapseIcon.classList.add('hidden');
            if (expandIcon)   expandIcon.classList.remove('hidden');

        } else {
            // Expand sidebar
            sidebar.classList.add('lg:w-72');
            sidebar.classList.remove('lg:w-[4.5rem]');

            // Show text labels
            document.querySelectorAll('.sidebar-label').forEach(el => {
                el.classList.remove('opacity-0', 'w-0', 'overflow-hidden');
                el.style.maxWidth = '';
            });
            // Show section labels
            document.querySelectorAll('.sidebar-section-label').forEach(el => {
                el.classList.remove('opacity-0', 'h-0', 'py-0', 'my-0', 'overflow-hidden');
                el.style.maxHeight = '';
            });

            // Restore link alignment
            document.querySelectorAll('.sidebar-link').forEach(el => {
                el.classList.remove('justify-center');
                el.classList.add('space-x-3');
            });

            // Switch icons
            if (collapseIcon) collapseIcon.classList.remove('hidden');
            if (expandIcon)   expandIcon.classList.add('hidden');
        }
    }

    // Apply saved state on load
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

    // ─── Resize Handler ──────────────────────────────────────────────────

    window.addEventListener('resize', () => {
        if (window.innerWidth >= 1024) {
            // Ensure mobile state is clean
            overlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        } else {
            // Close mobile sidebar
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }
    });
});
