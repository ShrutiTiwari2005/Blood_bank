/**
 * BLOOD BANK INTELLIGENCE - ELITE TOAST ENGINE v4.0
 * Lightweight, surgical medical notifications.
 */

window.v4Toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'v4-toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'success', duration = 4000) {
        this.init();
        
        const toast = document.createElement('div');
        toast.className = `v4-toast v4-toast-${type}`;
        
        const iconName = type === 'success' ? 'check-circle' : 
                         type === 'error' ? 'alert-octagon' : 'alert-triangle';
        
        toast.innerHTML = `
            <i data-lucide="${iconName}" size="20"></i>
            <span class="text-xs font-bold text-slate-700">${message}</span>
        `;
        
        this.container.appendChild(toast);
        lucide.createIcons();

        // Auto-remove logic
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px) scale(0.95)';
            setTimeout(() => toast.remove(), 400);
        }, duration);
    },

    success(m) { this.show(m, 'success'); },
    error(m) { this.show(m, 'error'); },
    warning(m) { this.show(m, 'warning'); }
};
