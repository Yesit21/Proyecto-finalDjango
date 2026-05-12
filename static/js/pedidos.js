export const pedidosManager = {
    init() {
        this.updateCartTotal();
        this.attachRemoveButtons();
    },

    updateCartTotal() {
        const totalElement = document.querySelector('#cart-total');
        if (!totalElement) return;

        const subtotals = Array.from(document.querySelectorAll('.cart-subtotal')).map((node) => {
            return Number(node.textContent.replace('$', '').trim()) || 0;
        });

        const total = subtotals.reduce((sum, value) => sum + value, 0);
        totalElement.textContent = `$${total.toFixed(2)}`;
    },

    attachRemoveButtons() {
        const removeButtons = document.querySelectorAll('.cart-remove');
        removeButtons.forEach((button) => {
            button.addEventListener('click', () => {
                setTimeout(() => this.updateCartTotal(), 100);
            });
        });
    },
};
