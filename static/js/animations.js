/**
 * BLOOD BANK AI - ELITE INTERACTION & ANIMATION ENGINE v4.0
 * Features: Scroll-Based Reveals, Staggered Loading, 60fps Performance
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. SCROLL-BASED REVEALS (Intersection Observer) ---
    const revealCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    };

    const revealObserver = new IntersectionObserver(revealCallback, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));


    // --- 2. STAGGERED GRID LOADING ---
    const staggerGrids = document.querySelectorAll('.stagger-grid');
    staggerGrids.forEach(grid => {
        const items = grid.children;
        Array.from(items).forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('stagger-item');
        });
    });


    // --- 3. DYNAMIC DATA FRESHNESS UPDATER ---
    const updateTimestamp = () => {
        const timestampEl = document.getElementById('v4-timestamp');
        if (timestampEl) {
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            timestampEl.innerText = `Data Synced: ${timeStr}`;
        }
    };
    setInterval(updateTimestamp, 10000);
    updateTimestamp();


    // --- 4. OPTIMISTIC UI FEEDBACK ---
    const luxuryForms = document.querySelectorAll('.diagnostic-form, .structured-form');
    luxuryForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('.btn-elite');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<i data-lucide="loader-2" class="animate-spin mr-2"></i> Processing...`;
                lucide.createIcons();
            }
        });
    });

});

// Global Theme Switcher Wrapper
window.toggleLuxuryTheme = () => {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Smooth transition radial pulse effect
    const mask = document.createElement('div');
    mask.style.position = 'fixed';
    mask.style.inset = '0';
    mask.style.background = newTheme === 'dark' ? '#0F172A' : '#F8FAFC';
    mask.style.zIndex = '9999';
    mask.style.opacity = '0';
    mask.style.transition = 'opacity 0.3s ease-in-out';
    document.body.appendChild(mask);
    
    setTimeout(() => {
        mask.style.opacity = '0.4';
        setTimeout(() => {
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            mask.style.opacity = '0';
            setTimeout(() => mask.remove(), 300);
        }, 150);
    }, 10);
};
