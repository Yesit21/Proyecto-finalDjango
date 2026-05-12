export const dashboardManager = {
    init() {
        this.animateKpis();
    },

    animateKpis() {
        const kpiElements = document.querySelectorAll('.kpi-value');
        kpiElements.forEach((element) => {
            const value = Number(element.dataset.value || '0');
            let current = 0;
            const step = Math.ceil(value / 30) || 1;
            const interval = setInterval(() => {
                current += step;
                if (current >= value) {
                    element.textContent = value.toLocaleString();
                    clearInterval(interval);
                } else {
                    element.textContent = current.toLocaleString();
                }
            }, 15);
        });
    },
};
