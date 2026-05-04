/**
 * Dismiss Popup Function
 * Hides the popup overlay and sends a dismissal notification to the server
 */
function dismissPopup() {
    const popupOverlay = document.getElementById('popupOverlay');
    if (popupOverlay) {
        popupOverlay.style.display = 'none';

        // Send AJAX POST to mark popup as dismissed server-side
        fetch('/api/dismiss-popup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        }).catch(error => {
            console.error('Error dismissing popup:', error);
        });
    }
}

/**
 * Document Ready - Initialize Popup Auto-Dismiss
 * Checks if popup exists and auto-dismisses based on data attributes
 */
document.addEventListener('DOMContentLoaded', function() {
    const popupOverlay = document.getElementById('popupOverlay');

    if (popupOverlay) {
        const autoDismiss = popupOverlay.getAttribute('data-auto-dismiss') === 'true';
        const dismissDelay = parseInt(popupOverlay.getAttribute('data-dismiss-delay'), 10) || 5000;

        if (autoDismiss) {
            setTimeout(function() {
                dismissPopup();
            }, dismissDelay);
        }
    }
});
