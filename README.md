# Travel Journal Hub 🌍

A full-stack web application that lets users document, organize, and revisit travel experiences in a structured way. Travel Journal Hub offers a centralized platform to replace scattered notes or social media posts, catering to the growing need for digital memory-keeping.

## Features

- **Create Travel Entries**: Document your travel experiences with title, location, date, content, and optional images
- **View Entries**: Browse all your travel memories in a beautiful grid layout
- **Edit & Update**: Modify existing entries to add more details or correct information
- **Delete Entries**: Remove entries you no longer want to keep
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **RESTful API**: Clean API architecture for easy integration and extensibility

## Technology Stack

### Backend
- **Flask**: Python web framework handling server-side logic
- **MySQL**: Relational database for persistent data storage
- **Flask-CORS**: Enable cross-origin resource sharing
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with CSS variables and responsive design
- **JavaScript (ES6+)**: Client-side logic using the Fetch API
- **No frameworks**: Pure vanilla JavaScript for lightweight performance

## Architecture

The application follows a client-server architecture:

1. **Frontend (Client)**: HTML/CSS/JavaScript interface served as static files
2. **Backend (Server)**: Flask application managing business logic and data flow
3. **Database**: MySQL storing all journal entries persistently
4. **Communication**: RESTful API with JSON data format using JavaScript's Fetch API

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/WanmengZhang/Travel-Journal-Hub.git
cd Travel-Journal-Hub
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL Database

1. Start your MySQL server
2. Create a database (the app will auto-create it if it doesn't exist):

```sql
CREATE DATABASE travel_journal_hub;
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=travel_journal_hub
```

### Step 5: Run the Application

```bash
python app.py
```

The application will:
- Initialize the database and create tables automatically
- Start the Flask development server
- Be accessible at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```
GET /api/health
```
Returns API status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Travel Journal Hub API is running"
}
```

#### 2. Get All Entries
```
GET /api/entries
```
Retrieves all journal entries, sorted by travel date (newest first).

**Response:**
```json
{
  "entries": [
    {
      "id": 1,
      "title": "Amazing Weekend in Paris",
      "location": "Paris, France",
      "travel_date": "2024-03-15",
      "content": "Had an incredible time...",
      "image_url": "https://example.com/image.jpg",
      "created_at": "2024-03-20T10:30:00",
      "updated_at": "2024-03-20T10:30:00"
    }
  ]
}
```

#### 3. Get Single Entry
```
GET /api/entries/<entry_id>
```
Retrieves a specific journal entry by ID.

**Response:**
```json
{
  "id": 1,
  "title": "Amazing Weekend in Paris",
  "location": "Paris, France",
  "travel_date": "2024-03-15",
  "content": "Had an incredible time...",
  "image_url": "https://example.com/image.jpg",
  "created_at": "2024-03-20T10:30:00",
  "updated_at": "2024-03-20T10:30:00"
}
```

#### 4. Create Entry
```
POST /api/entries
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Amazing Weekend in Paris",
  "location": "Paris, France",
  "travel_date": "2024-03-15",
  "content": "Had an incredible time exploring the city...",
  "image_url": "https://example.com/image.jpg"
}
```

**Response:**
```json
{
  "message": "Entry created successfully",
  "entry_id": 1
}
```

#### 5. Update Entry
```
PUT /api/entries/<entry_id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "location": "Paris, France",
  "travel_date": "2024-03-15",
  "content": "Updated content...",
  "image_url": "https://example.com/updated.jpg"
}
```

**Response:**
```json
{
  "message": "Entry updated successfully"
}
```

#### 6. Delete Entry
```
DELETE /api/entries/<entry_id>
```

**Response:**
```json
{
  "message": "Entry deleted successfully"
}
```

## Database Schema

### Table: journal_entries

| Column | Type | Description |
|--------|------|-------------|
| id | INT (Primary Key, Auto Increment) | Unique entry identifier |
| title | VARCHAR(255) | Entry title |
| location | VARCHAR(255) | Travel location |
| travel_date | DATE | Date of travel |
| content | TEXT | Detailed description |
| image_url | VARCHAR(500) | Optional image URL |
| created_at | TIMESTAMP | Entry creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## Project Structure

```
Travel-Journal-Hub/
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
└── static/                # Frontend files
    ├── index.html         # Main HTML page
    ├── app.js             # JavaScript logic (Fetch API)
    └── styles.css         # CSS styling
```

## Development

### Running in Development Mode

The Flask app runs in debug mode by default, which provides:
- Auto-reloading on code changes
- Detailed error messages
- Interactive debugger

### Testing the API

You can test the API endpoints using tools like:
- Browser (for GET requests)
- curl
- Postman
- HTTPie

Example using curl:
```bash
# Create an entry
curl -X POST http://localhost:5000/api/entries \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Entry",
    "location": "New York, USA",
    "travel_date": "2024-03-15",
    "content": "Test content"
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Built with ❤️ for travel enthusiasts who want to preserve their memories digitally.