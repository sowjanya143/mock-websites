# Global Investment Partners - Flask Web Application

A professional investment firm website built with Flask, following clean code principles and best practices.

## Project Structure

```
kbiglobalinvestors/
├── app/
│   ├── __init__.py              # Application factory
│   ├── routes/
│   │   ├── __init__.py          # Routes package
│   │   └── main.py              # Main application routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Application styles
│   │   └── js/
│   │       └── main.js          # Client-side JavaScript
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Main contact page
│       └── components/
│           ├── header.html      # Header component
│           ├── footer.html      # Footer component
│           └── modals.html      # Modal dialogs
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## Features

- **Responsive Design**: Mobile-first, fully responsive layout
- **Contact Form**: Ajax-powered form submission
- **Legal Compliance**: Terms, privacy policy, and regional compliance information
- **Cookie Banner**: GDPR-compliant cookie consent management
- **Modular Architecture**: Clean separation of concerns
- **Configuration Management**: Environment-based configuration
- **RESTful API**: JSON API endpoint for form submissions

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\Users\hmalijan\Desktop\mock-website\kbiglobalinvestors
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables** (optional):
   Create a `.env` file in the project root:
   ```
   FLASK_CONFIG=development
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

## Running the Application

### Development Mode

```bash
python run.py
```

The application will start on `http://localhost:5000`

### Production Mode

```bash
# Set environment variable
set FLASK_CONFIG=production  # Windows
export FLASK_CONFIG=production  # macOS/Linux

# Run with Gunicorn (Linux/macOS)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

## Configuration

The application supports multiple configuration environments:

- **Development**: Debug mode enabled, detailed error messages
- **Production**: Debug disabled, optimized for deployment
- **Testing**: Configuration for running tests

Edit `config.py` to modify configuration settings.

## API Endpoints

### POST /api/contact
Submit contact form data

**Request Body**:
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+1 234 567 8900",
  "message": "Your message here"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Thank you for your message, John! We will get back to you shortly."
}
```

## Project Architecture

### Clean Code Principles Applied

1. **Separation of Concerns**: Routes, templates, static files, and configuration are separated
2. **Single Responsibility**: Each module has a clear, single purpose
3. **DRY (Don't Repeat Yourself)**: Reusable components and templates
4. **Configuration Management**: Environment-based settings
5. **Application Factory Pattern**: Flexible app initialization
6. **Blueprint Pattern**: Modular routing structure

### Design Patterns Used

- **Application Factory**: `create_app()` function for flexible initialization
- **Blueprint Pattern**: Modular route organization
- **Template Inheritance**: Base template with child templates
- **Component Pattern**: Reusable template components

## Future Enhancements

- [ ] Database integration for storing contact submissions
- [ ] Email service integration (SMTP/SendGrid)
- [ ] User authentication and admin panel
- [ ] Form validation with WTForms
- [ ] Unit and integration tests
- [ ] Logging and monitoring
- [ ] Rate limiting for API endpoints
- [ ] Internationalization (i18n)

## Contributing

When contributing to this project, please follow these guidelines:

1. Follow PEP 8 style guidelines for Python code
2. Use meaningful variable and function names
3. Add docstrings to all functions and classes
4. Keep functions small and focused
5. Write tests for new features
6. Update documentation as needed

## License

© 2024 Global Investment Partners. All rights reserved.

## Contact

For questions or support, please contact:
- Email: contact@gip-test.com
- Dublin Office: +353 (1) 555 4400
- Boston Office: +1 617 555 7141
