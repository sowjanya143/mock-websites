// Cookie Banner Management
function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    document.getElementById('cookieBanner').classList.add('hidden');
}

function declineCookies() {
    localStorage.setItem('cookieConsent', 'declined');
    document.getElementById('cookieBanner').classList.add('hidden');
}

function openCookieSettings() {
    localStorage.removeItem('cookieConsent');
    document.getElementById('cookieBanner').classList.remove('hidden');
}

// Check cookie consent on page load
window.addEventListener('load', function() {
    const cookieConsent = localStorage.getItem('cookieConsent');
    if (cookieConsent) {
        document.getElementById('cookieBanner').classList.add('hidden');
    }
});

// Modal Functions
function openPrivacyModal() {
    document.getElementById('privacyModal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function acceptTerms() {
    localStorage.setItem('termsAccepted', 'true');
    closeModal('termsModal');
}

window.addEventListener('load', function() {
    const termsAccepted = localStorage.getItem('termsAccepted');
    if (!termsAccepted) {
        document.getElementById('termsModal').classList.add('active');
    }
});

// Accordion Functions
function toggleAccordion(header) {
    const item = header.parentElement;
    const content = item.querySelector('.accordion-content');
    const toggle = header.querySelector('.accordion-toggle');

    const isActive = content.classList.contains('active');

    // Close all other items
    document.querySelectorAll('.accordion-content.active').forEach(el => {
        el.classList.remove('active');
        el.previousElementSibling.classList.remove('active');
        el.previousElementSibling.querySelector('.accordion-toggle').classList.remove('active');
    });

    // Toggle current item
    if (!isActive) {
        content.classList.add('active');
        header.classList.add('active');
        toggle.classList.add('active');
    }
}

function agreeToTerms(section) {
    localStorage.setItem(`agree_${section}`, 'true');
    alert(`You have agreed to the ${section} terms.`);
}

// Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                message: document.getElementById('message').value
            };
            
            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(data.message);
                    contactForm.reset();
                } else {
                    alert('There was an error submitting your message. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('There was an error submitting your message. Please try again.');
            }
        });
    }
});

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const termsModal = document.getElementById('termsModal');
    const privacyModal = document.getElementById('privacyModal');

    if (event.target === termsModal) {
        closeModal('termsModal');
    }
    if (event.target === privacyModal) {
        closeModal('privacyModal');
    }
});
