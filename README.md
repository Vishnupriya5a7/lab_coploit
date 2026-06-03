# Mark's Python Web App - Interactive Form & API

A Flask-based web application with an interactive HTML form and RESTful API endpoints for handling submissions and generating pseudo-random tokens. Built with GitHub Copilot assistance as a learning project.

## 🎯 Overview

This project demonstrates:
- Building a Python web application using Flask
- Creating interactive HTML forms with modern styling
- Developing RESTful API endpoints
- Generating secure pseudo-random tokens
- Writing comprehensive test cases
- Using GitHub Copilot as an AI pair programmer

## 📋 Features

### Frontend
- **Interactive HTML Form** - Modern, responsive form design with real-time validation
- **Form Fields**:
  - Full Name (required)
  - Email Address (optional)
  - Reason for Submission (required)
  - Additional Comments (optional)
- **User Feedback** - Success/error messages with auto-hide functionality
- **Token Display** - Shows the generated token after successful submission

### Backend API
- **POST /api/submit** - Submit form data and receive a unique token
- **GET /api/token** - Generate a standalone token with custom length
- **GET /api/submissions** - Retrieve all submitted data
- **GET /api/health** - Health check endpoint

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lab_coploit
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open in browser**
   - Navigate to `http://localhost:5000`
   - You should see the interactive form

3. **Test the API**
   - Form submission: Submit the form to generate a token
   - Health check: `http://localhost:5000/api/health`
   - Get token: `http://localhost:5000/api/token`
   - Get submissions: `http://localhost:5000/api/submissions`

## 📚 API Documentation

### 1. Submit Form (POST /api/submit)

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "reason": "bug_report",
  "comments": "Found a critical bug"
}
```

**Response (Success):**
```json
{
  "success": true,
  "token": "aB1cD2eF3gH4iJ5k",
  "message": "Form submitted successfully!",
  "data": {
    "token": "aB1cD2eF3gH4iJ5k",
    "name": "John Doe",
    "email": "john@example.com",
    "reason": "bug_report",
    "comments": "Found a critical bug",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Missing required fields: name, reason"
}
```

### 2. Generate Token (GET /api/token)

**Query Parameters:**
- `length` (optional, default: 16) - Token length (4-128 characters)

**Request:**
```
GET /api/token?length=32
```

**Response:**
```json
{
  "success": true,
  "token": "aB1cD2eF3gH4iJ5kLmNoPqRsT1uVwXyZ",
  "length": 32
}
```

### 3. Get All Submissions (GET /api/submissions)

**Request:**
```
GET /api/submissions
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "submissions": [
    {
      "token": "aB1cD2eF3gH4iJ5k",
      "name": "John Doe",
      "email": "john@example.com",
      "reason": "bug_report",
      "comments": "Found a critical bug",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "token": "xY9zAbCdEfGhIjKl",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "reason": "feature_request",
      "comments": "Request new feature",
      "timestamp": "2024-01-15T10:35:00"
    }
  ]
}
```

### 4. Health Check (GET /api/health)

**Request:**
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Mark's Python Web App",
  "timestamp": "2024-01-15T10:40:00"
}
```

## 🧪 Testing

### Run All Tests
```bash
python -m unittest test_app.py -v
```

### Run Specific Test Class
```bash
python -m unittest test_app.TestFlaskApp.test_submit_form_valid_data -v
```

### Test Coverage
The test suite includes:
- ✅ Token generation (uniqueness, length, character validation)
- ✅ Home page rendering
- ✅ Form submission with valid data
- ✅ Form submission with missing fields
- ✅ Error handling and validation
- ✅ Data storage verification
- ✅ API endpoint functionality
- ✅ Health check endpoint
- ✅ HTTP error handling (404, 405)

## 📁 Project Structure

```
lab_coploit/
├── app.py                 # Main Flask application
├── templates/
│   └── form.html         # Interactive HTML form
├── requirements.txt      # Python dependencies
├── test_app.py           # Unit tests
└── README.md             # This file
```

## 🔧 Code Explanation

### Token Generation (`generate_token()`)
- Uses Python's `secrets` module for cryptographically secure random generation
- Combines uppercase letters, lowercase letters, and digits
- Default length: 16 characters
- Customizable length via function parameter

### Form Handling (`submit_form()`)
- Validates required fields (name, reason)
- Generates unique token for each submission
- Returns JSON response with token and submission data
- Includes error handling and logging

### Frontend JavaScript
- Async form submission without page reload
- Real-time validation and error messages
- Loading indicator during submission
- Token display in formatted box
- Auto-hiding status messages

## 🎓 Learning Outcomes

After completing this project, you will understand:

1. **Flask Basics**
   - Routing and URL parameters
   - Request handling (GET, POST)
   - JSON responses

2. **Web Form Development**
   - HTML form creation
   - Client-side validation with JavaScript
   - Styling with CSS

3. **API Development**
   - RESTful API design
   - Request/response handling
   - Error handling and validation

4. **Python Best Practices**
   - Code documentation with docstrings
   - Error handling and logging
   - Unit testing

5. **GitHub Copilot Usage**
   - Code generation
   - Comment and docstring creation
   - Test case generation
   - Code explanation

## 💡 GitHub Copilot Tips

This project was created using GitHub Copilot. Here are some tips:

1. **Code Generation**: Describe what you want, and Copilot suggests implementations
2. **Comments First**: Write comments describing functionality, then let Copilot generate code
3. **Test Generation**: Ask Copilot to generate test cases for your functions
4. **Refactoring**: Use Copilot suggestions for cleaner, more efficient code
5. **Documentation**: Let Copilot help create comprehensive docstrings

## 🔐 Security Considerations

- Uses `secrets` module for cryptographically secure random generation
- Validates and sanitizes all user inputs
- CORS headers can be added for cross-origin requests
- In production, consider:
  - Database instead of in-memory storage
  - Authentication/authorization
  - HTTPS/SSL
  - Rate limiting
  - Input validation enhancements

## 🚀 Future Enhancements

- Add database persistence (SQLite, PostgreSQL)
- Implement user authentication
- Add pagination for submissions
- Create admin dashboard
- Add file upload support
- Implement rate limiting
- Add API key authentication
- Create deployment configuration (Docker, Heroku)

## 📝 License

This project is created for educational purposes.

## 👤 Author

**Mark** - ABC Project Fresher
- Created with GitHub Copilot AI assistance
- Mentored by John

---

**Happy Coding! 🚀**

For questions or issues, please refer to the code comments or test cases for usage examples.