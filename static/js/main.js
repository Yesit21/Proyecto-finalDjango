// Gestión del sidebar móvil
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('app-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const openBtn = document.getElementById('sidebar-toggle');
    const closeBtn = document.getElementById('sidebar-close');

    if (sidebar && overlay && openBtn) {
        // Abrir sidebar
        openBtn.addEventListener('click', function() {
            sidebar.classList.remove('hidden');
            sidebar.classList.add('flex');
            overlay.classList.remove('hidden');
            document.documentElement.classList.add('overflow-hidden');
        });

        // Cerrar sidebar
        function closeSidebar() {
            if (window.matchMedia('(min-width: 768px)').matches) {
                return;
            }
            sidebar.classList.add('hidden');
            sidebar.classList.remove('flex');
            overlay.classList.add('hidden');
            document.documentElement.classList.remove('overflow-hidden');
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', closeSidebar);
        }

        overlay.addEventListener('click', closeSidebar);

        // Cerrar con tecla Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeSidebar();
            }
        });

        // Resetear estado en cambio de tamaño de pantalla
        window.matchMedia('(min-width: 768px)').addEventListener('change', function(e) {
            if (e.matches) {
                overlay.classList.add('hidden');
                if (sidebar) {
                    sidebar.classList.remove('hidden');
                    sidebar.classList.add('flex');
                }
                document.documentElement.classList.remove('overflow-hidden');
            }
        });
    }

    // Gestión del tema (dark/light)
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }

    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
});
