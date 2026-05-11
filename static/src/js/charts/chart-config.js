import Chart from 'chart.js/auto';

export const chartConfig = {
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'bottom'
            }
        }
    },

    createBarChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: { ...this.defaultOptions, ...options }
        });
    },

    createLineChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: { ...this.defaultOptions, ...options }
        });
    },

    createPieChart(ctx, data, options = {}) {
        return new Chart(ctx, {
            type: 'pie',
            data: data,
            options: { ...this.defaultOptions, ...options }
        });
    }
};
