from flask import Flask, render_template

app = Flask(__name__)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
