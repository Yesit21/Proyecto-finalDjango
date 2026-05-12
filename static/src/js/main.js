import { themeManager } from './modules/theme.js';
import { alertManager } from './modules/alerts.js';
import { layoutManager } from './modules/layout.js';

document.addEventListener('DOMContentLoaded', () => {
    themeManager.init();
    alertManager.init();
    layoutManager.init();

    // Inicializar otros módulos solo si existen
    if (typeof pedidosManager !== 'undefined') {
        pedidosManager.init();
    }
    if (typeof dashboardManager !== 'undefined') {
        dashboardManager.init();
    }
    if (typeof chartsManager !== 'undefined') {
        chartsManager.init();
    }
});
