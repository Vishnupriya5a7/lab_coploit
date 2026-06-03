"""
Flask Web Application with Interactive Form and API Endpoint
Author: Mark (with GitHub Copilot assistance)
Purpose: Serve interactive HTML form and generate pseudo-random tokens for identifying reasons
"""

from flask import Flask, render_template, request, jsonify
import secrets
import string
from datetime import datetime
import logging

# Initialize Flask application
app = Flask(__name__)

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for submitted data (for demonstration)
# In production, this would be a database
submissions = []


def generate_token(length=16):
    """
    Generate a pseudo-random token for identifying reasons.
    
    Args:
        length (int): Length of the token (default: 16 characters)
    
    Returns:
        str: A randomly generated alphanumeric token
    
    Example:
        >>> token = generate_token()
        >>> len(token)
        16
    """
    # Create a character set combining uppercase, lowercase, and digits
    characters = string.ascii_letters + string.digits
    # Generate random token using secure random choice
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


@app.route('/', methods=['GET'])
def home():
    """
    Render the home page with interactive HTML form.
    
    Returns:
        Rendered HTML template with the form
    """
    logger.info("Home page accessed")
    return render_template('form.html')


@app.route('/api/submit', methods=['POST'])
def submit_form():
    """
    API endpoint to handle form submissions.
    Generates a unique token and stores the submission data.
    
    Returns:
        JSON response with:
        - success (bool): Whether submission was successful
        - token (str): Generated pseudo-random token
        - message (str): Status message
        - data (dict): Submitted form data
    """
    try:
        # Extract JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'reason' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing required fields: name, reason'
            }), 400
        
        # Generate unique token for this submission
        token = generate_token()
        
        # Create submission record
        submission = {
            'token': token,
            'name': data.get('name', '').strip(),
            'email': data.get('email', '').strip(),
            'reason': data.get('reason', '').strip(),
            'comments': data.get('comments', '').strip(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store submission in memory
        submissions.append(submission)
        
        logger.info(f"New submission recorded with token: {token}")
        
        # Return success response
        return jsonify({
            'success': True,
            'token': token,
            'message': 'Form submitted successfully!',
            'data': submission
        }), 200
    
    except Exception as e:
        # Log and return error response
        logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing submission: {str(e)}'
        }), 500


@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """
    API endpoint to retrieve all submissions (for demonstration).
    
    Returns:
        JSON response with list of all submissions and count
    """
    return jsonify({
        'success': True,
        'count': len(submissions),
        'submissions': submissions
    }), 200


@app.route('/api/token', methods=['GET'])
def get_token():
    """
    API endpoint to generate and return a token (standalone token generation).
    
    Query Parameters:
        length (int): Token length (optional, default: 16)
    
    Returns:
        JSON response with generated token
    """
    try:
        # Get token length from query parameters (default: 16)
        length = request.args.get('length', 16, type=int)
        
        # Validate length parameter
        if length < 4 or length > 128:
            return jsonify({
                'success': False,
                'message': 'Token length must be between 4 and 128'
            }), 400
        
        # Generate token
        token = generate_token(length)
        
        return jsonify({
            'success': True,
            'token': token,
            'length': length
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating token: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        JSON response indicating API status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Mark\'s Python Web App',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors gracefully."""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully."""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask development server
    # Set debug=True for development (auto-reload and interactive debugger)
    app.run(debug=True, host='0.0.0.0', port=5000)
