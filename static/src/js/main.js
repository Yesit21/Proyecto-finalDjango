import { themeManager } from './modules/theme.js';
import { alertManager } from './modules/alerts.js';
import { pedidosManager } from '../js/pedidos.js';
import { dashboardManager } from '../js/dashboard.js';
import { chartsManager } from '../js/charts.js';

document.addEventListener('DOMContentLoaded', () => {
    themeManager.init();
    alertManager.init();
    pedidosManager.init();
    dashboardManager.init();
    chartsManager.init();
});
