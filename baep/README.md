# ZXQP Partners Website

A professional investment management firm website built with Flask.

## Project Structure

```
baep/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── templates/             # HTML templates
│   └── index.html         # Main about us page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       └── script.js      # JavaScript functionality
└── index.html             # Original HTML (can be removed)
```

## Features

- Responsive design with mobile menu
- Professional corporate styling
- Award recognition section with custom SVG icons
- Clean separation of concerns (HTML, CSS, JS)
- Flask routing for scalability

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
   ```bash
   cd baep
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Production Deployment

For production deployment, consider:

1. Set a secure `SECRET_KEY` in `app.py`
2. Set `debug=False` in `app.py`
3. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

## Development

- The main application logic is in `app.py`
- HTML templates are in `templates/`
- Static files (CSS, JS) are in `static/`
- Modify `style.css` for styling changes
- Modify `script.js` for JavaScript functionality

## Technologies Used

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Icons**: Custom SVG graphics

## License

© 2026 Global Finance Consortium. All rights reserved.
