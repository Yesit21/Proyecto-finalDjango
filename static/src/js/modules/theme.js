export const themeManager = {
    init() {
        this.loadTheme();
        this.setupToggle();
    },

    loadTheme() {
        // Cargar tema desde localStorage
        const theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    },

    setupToggle() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggleTheme());
        }
    },

    toggleTheme() {
        // Alternar la clase 'dark' en el elemento html
        const isDark = document.documentElement.classList.toggle('dark');
        
        // Guardar en localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        
        console.log('Tema cambiado a:', isDark ? 'oscuro' : 'claro');
    }
};
