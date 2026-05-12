export const layoutManager = {
    init() {
        this.sidebar = document.getElementById('app-sidebar');
        this.overlay = document.getElementById('sidebar-overlay');
        this.openBtn = document.getElementById('sidebar-toggle');
        this.closeBtn = document.getElementById('sidebar-close');

        if (!this.sidebar || !this.overlay) {
            return;
        }

        this.openBtn?.addEventListener('click', () => this.openSidebar());
        this.closeBtn?.addEventListener('click', () => this.closeSidebar());
        this.overlay.addEventListener('click', () => this.closeSidebar());

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeSidebar();
            }
        });

        window.matchMedia('(min-width: 768px)').addEventListener('change', (e) => {
            if (e.matches) {
                this.resetMobileState();
            }
        });
    },

    openSidebar() {
        this.sidebar.classList.remove('hidden');
        this.sidebar.classList.add('flex');
        this.overlay.classList.remove('hidden');
        document.documentElement.classList.add('overflow-hidden');
    },

    closeSidebar() {
        if (window.matchMedia('(min-width: 768px)').matches) {
            return;
        }

        this.sidebar.classList.add('hidden');
        this.sidebar.classList.remove('flex');
        this.overlay.classList.add('hidden');
        document.documentElement.classList.remove('overflow-hidden');
    },

    resetMobileState() {
        this.overlay.classList.add('hidden');
        this.sidebar.classList.remove('hidden');
        this.sidebar.classList.add('flex');
        document.documentElement.classList.remove('overflow-hidden');
    },
};
