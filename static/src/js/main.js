import { themeManager } from './modules/theme.js';
import { alertManager } from './modules/alerts.js';

document.addEventListener('DOMContentLoaded', () => {
    themeManager.init();
    alertManager.init();
});
