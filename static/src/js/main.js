import { themeManager } from './modules/theme.js';
import { alertManager } from './modules/alerts.js';

document.addEventListener('DOMContentLoaded', () => {
    themeManager.init();
    alertManager.init();
    
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
