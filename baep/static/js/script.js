/**
 * ZXQP Partners - Main JavaScript
 * Handles mobile menu, navigation alerts, and smooth scrolling
 */

// Toggle mobile menu
function toggleMenu() {
    const nav = document.getElementById('mainNav');
    nav.classList.toggle('active');
}

// Simulate link clicks with alerts (for demo purposes)
function showAlert(page) {
    alert('Navigating to: ' + page);
    return false;
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const nav = document.getElementById('mainNav');
        const toggle = document.querySelector('.menu-toggle');
        
        if (nav && toggle && !nav.contains(event.target) && !toggle.contains(event.target)) {
            nav.classList.remove('active');
        }
    });
});
