import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'

@app.route('/')
def index():
    """Serve the home page"""
    return render_template('index.html')

@app.route('/index.html')
def index_alt():
    """Alternative route for index.html"""
    return render_template('index.html')

@app.route('/about.html')
def about():
    """Serve the about page"""
    return render_template('about.html')

@app.route('/services.html')
def services():
    """Serve the services page"""
    return render_template('services.html')

@app.route('/contact.html')
def contact():
    """Serve the contact page"""
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port, use_reloader=False)
