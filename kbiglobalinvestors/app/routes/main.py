"""Main application routes."""
from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the main contact page."""
    return render_template('index.html')


@bp.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submission."""
    data = request.get_json()
    
    # Here you would typically send an email or save to database
    # For now, we'll just return a success response
    
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    
    # TODO: Implement email sending or database storage
    
    return jsonify({
        'success': True,
        'message': f'Thank you for your message, {first_name}! We will get back to you shortly.'
    })
