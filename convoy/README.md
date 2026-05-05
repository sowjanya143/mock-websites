# Finex - Financial Platform Web Application

A Flask-based web application for the Finex financial management platform, following clean code principles and Flask best practices.

## Project Structure

```
convoy/
├── app.py                  # Flask application with route definitions
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/                # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   └── js/
│       └── script.js      # Client-side JavaScript
└── templates/             # HTML templates
    ├── index.html         # Home page
    ├── about.html         # About page
    ├── services.html      # Services page
    └── contact.html       # Contact page
```

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.7 or higher installed on your system.

### 2. Install Dependencies
Open a terminal in this directory and run:
```bash
pip install -r requirements.txt
```

Or install Flask directly:
```bash
pip install Flask
```

### 3. Run the Server
Start the Flask development server:
```bash
python app.py
```

### 4. Access the Website
Open your web browser and navigate to:
- http://localhost:5000
- http://127.0.0.1:5000

The server will be accessible from other devices on your network at:
- http://YOUR_LOCAL_IP:5000

## Available Routes
- `/` or `/index.html` - Home page
- `/about.html` - About page
- `/services.html` - Services page
- `/contact.html` - Contact page

Static assets are automatically served from the `/static/` directory.

## Development Mode
The server runs in debug mode by default, which means:
- Automatic reloading when files change
- Detailed error messages
- Interactive debugger

## Clean Code Principles Applied
- **Separation of Concerns**: Templates, static files, and application logic are separated
- **Flask Conventions**: Standard Flask directory structure (templates/, static/)
- **Maintainability**: Clear folder hierarchy makes the codebase easy to navigate
- **Scalability**: Structure supports easy addition of new pages and assets

## Production Deployment
For production use, consider:
- Setting `debug=False` in app.py
- Using a production WSGI server like Gunicorn or uWSGI
- Setting up proper environment variables
- Configuring a reverse proxy (nginx/Apache)
- Adding proper error handling and logging

## Stopping the Server
Press `Ctrl+C` in the terminal to stop the server.
