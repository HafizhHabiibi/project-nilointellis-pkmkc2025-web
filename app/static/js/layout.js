// Hamburger Menu Toggle
const hamburgerBtn = document.getElementById('hamburgerBtn');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const body = document.body;

hamburgerBtn.addEventListener('click', function() {
    sidebar.classList.toggle('sidebar-open');
    sidebarOverlay.classList.toggle('overlay-active');
    hamburgerBtn.classList.toggle('hamburger-active');

    // Prevent body scroll when sidebar is open on mobile
    if (window.innerWidth <= 768) {
        body.classList.toggle('no-scroll');
    }
});

// Close sidebar when clicking overlay
sidebarOverlay.addEventListener('click', function() {
    closeSidebar();
});

// Close sidebar when clicking on link (mobile/tablet)
const sidebarLinks = document.querySelectorAll('.sidebar a');
sidebarLinks.forEach(link => {
    link.addEventListener('click', function() {
        if (window.innerWidth <= 992) {
            closeSidebar();
        }
    });
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
        closeSidebar();
    }
});

// Function to close sidebar
function closeSidebar() {
    sidebar.classList.remove('sidebar-open');
    sidebarOverlay.classList.remove('overlay-active');
    hamburgerBtn.classList.remove('hamburger-active');
    body.classList.remove('no-scroll');
}

// Close sidebar on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('sidebar-open')) {
        closeSidebar();
    }
});

// Logout Modal Enhancement
const logoutModal = document.getElementById('logoutModal');

// Add smooth animation when modal shows
if (logoutModal) {
    logoutModal.addEventListener('show.bs.modal', function() {
        document.body.style.overflow = 'hidden';
    });

    logoutModal.addEventListener('hidden.bs.modal', function() {
        document.body.style.overflow = 'auto';
    });

    // Add click sound effect (optional)
    const logoutBtn = document.querySelector('[data-bs-target="#logoutModal"]');
    const confirmBtn = document.querySelector('.logout-confirm-btn');
    const cancelBtn = document.querySelector('.logout-cancel-btn');

    // Add hover effects
    if (confirmBtn) {
        confirmBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });

        confirmBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });

        cancelBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    }
}