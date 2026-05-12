export const chartsManager = {
    init() {
        this.renderChart('sales-chart', 'Ventas', 'line');
        this.renderChart('income-chart', 'Ingresos', 'bar');
        this.renderChart('orders-chart', 'Pedidos', 'pie');
        this.renderChart('products-chart', 'Platos vendidos', 'bar');
    },

    renderChart(elementId, label, defaultType) {
        const canvas = document.getElementById(elementId);
        if (!canvas) return;

        const payload = canvas.dataset.chart ? JSON.parse(canvas.dataset.chart) : null;
        if (!payload) return;

        const data = {
            labels: payload.labels || [],
            datasets: [{
                label,
                data: payload.data || [],
                backgroundColor: payload.backgroundColor || 'rgba(59, 130, 246, 0.5)',
                borderColor: payload.borderColor || 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                fill: true,
            }],
        };

        const type = payload.type || defaultType;
        new Chart(canvas, {
            type,
            data,
            options: {
                responsive: true,
                plugins: {
                    legend: {display: type !== 'line'},
                },
            },
        });
    },
};
