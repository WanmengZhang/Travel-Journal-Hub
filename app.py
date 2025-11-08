"""
Travel Journal Hub - Flask Backend Application
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'travel_journal_hub')
}


def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def init_db():
    """Initialize database and create tables if they don't exist"""
    try:
        # Connect without database to create it
        temp_config = DB_CONFIG.copy()
        database_name = temp_config.pop('database')
        
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
        
        # Create journal_entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                travel_date DATE NOT NULL,
                content TEXT NOT NULL,
                image_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")
        return True
    except Error as e:
        print(f"Error initializing database: {e}")
        return False


@app.route('/')
def index():
    """Serve the main HTML page"""
    return app.send_static_file('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Travel Journal Hub API is running'})


@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all journal entries"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, location, travel_date, content, image_url, 
                   created_at, updated_at 
            FROM journal_entries 
            ORDER BY travel_date DESC, created_at DESC
        """)
        entries = cursor.fetchall()
        
        # Convert date and datetime objects to strings
        for entry in entries:
            if entry['travel_date']:
                entry['travel_date'] = entry['travel_date'].isoformat()
            if entry['created_at']:
                entry['created_at'] = entry['created_at'].isoformat()
            if entry['updated_at']:
                entry['updated_at'] = entry['updated_at'].isoformat()
        
        cursor.close()
        connection.close()
        return jsonify({'entries': entries})
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to retrieve entries'}), 500


@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Get a specific journal entry by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, location, travel_date, content, image_url, 
                   created_at, updated_at 
            FROM journal_entries 
            WHERE id = %s
        """, (entry_id,))
        entry = cursor.fetchone()
        
        if entry:
            # Convert date and datetime objects to strings
            if entry['travel_date']:
                entry['travel_date'] = entry['travel_date'].isoformat()
            if entry['created_at']:
                entry['created_at'] = entry['created_at'].isoformat()
            if entry['updated_at']:
                entry['updated_at'] = entry['updated_at'].isoformat()
            
            cursor.close()
            connection.close()
            return jsonify(entry)
        else:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Entry not found'}), 404
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to retrieve entry'}), 500


@app.route('/api/entries', methods=['POST'])
def create_entry():
    """Create a new journal entry"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'location', 'travel_date', 'content']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO journal_entries (title, location, travel_date, content, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['title'],
            data['location'],
            data['travel_date'],
            data['content'],
            data.get('image_url', '')
        ))
        connection.commit()
        entry_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            'message': 'Entry created successfully',
            'entry_id': entry_id
        }), 201
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to create entry'}), 500


@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an existing journal entry"""
    data = request.get_json()
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM journal_entries WHERE id = %s", (entry_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Entry not found'}), 404
        
        # Update entry
        cursor.execute("""
            UPDATE journal_entries 
            SET title = %s, location = %s, travel_date = %s, 
                content = %s, image_url = %s
            WHERE id = %s
        """, (
            data.get('title'),
            data.get('location'),
            data.get('travel_date'),
            data.get('content'),
            data.get('image_url', ''),
            entry_id
        ))
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Entry updated successfully'})
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to update entry'}), 500


@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a journal entry"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM journal_entries WHERE id = %s", (entry_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Entry not found'}), 404
        
        # Delete entry
        cursor.execute("DELETE FROM journal_entries WHERE id = %s", (entry_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Entry deleted successfully'})
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to delete entry'}), 500


if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run the app
    # Note: In production, use a WSGI server like gunicorn instead of the development server
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
