# 📝 Daily Notes Application

A full-stack web application for managing daily notes with user authentication and CRUD operations.

## 🌟 Features

### 🔐 Authentication
- **User Registration** - Create new accounts with username/password
- **Secure Login** - JWT-based authentication system  
- **Session Management** - Automatic token handling and logout
- **Protected Routes** - Middleware-based route protection

### 📋 Note Management
- **Create Notes** - Add new notes with title and content
- **View Notes** - Display all user notes in chronological order
- **Edit Notes** - Inline editing with real-time updates
- **Delete Notes** - Remove unwanted notes
- **Responsive Design** - Works on desktop and mobile

### ⚡ User Experience
- **Real-time Updates** - Instant UI updates after operations
- **Loading States** - Visual feedback during API calls
- **Error Handling** - Graceful error management
- **Keyboard Shortcuts** - Quick actions with hotkeys
- **Modern UI** - Clean, professional interface

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database with Mongoengine ODM
- **JWT** - JSON Web Tokens for authentication
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Werkzeug** - Password hashing and security

### Frontend  
- **Nuxt.js 3** - Vue.js framework with SSR
- **Vue 3** - Progressive JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Composables** - Reusable logic with Vue Composition API

### Testing
- **Pytest** - Python testing framework
- **Mongomock** - MongoDB mocking for tests
- **Test Coverage** - Comprehensive unit tests

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **MongoDB** (running locally or cloud)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ex1.1-unit-test-daily-notes
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (if not running)
brew services start mongodb-community  # macOS
# Or start MongoDB service on your system

# Run the backend
python app.py
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Configuration

Create configuration files as needed:

**Backend (`backend/config.py`)**
```python
class Config:
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret'
    MONGODB_SETTINGS = {
        'db': 'mario_notes',
        'host': 'localhost',
        'port': 27017
    }
```

## 📖 Usage

### 1. **Registration & Login**
- Visit `http://localhost:3000`
- Create a new account or login with existing credentials
- You'll be redirected to the dashboard upon successful authentication

### 2. **Creating Notes**
- Enter a title and content in the form fields
- Click "Add" or press Enter to create a note
- The note will appear in your notes list immediately

### 3. **Editing Notes**
- Click the "Edit" button on any note card
- Modify the title and content directly
- Save with "Save" button, Ctrl+Enter, or cancel with "Cancel"/Esc

### 4. **Deleting Notes**
- Click the "Delete" button on any note card
- The note will be removed immediately

### 5. **Keyboard Shortcuts**
- **Enter** - Create new note / Save edit
- **Ctrl+Enter** - Save edit from textarea
- **Esc** - Cancel editing

## 🔧 API Endpoints

### Authentication
```http
POST /api/register    # Register new user
POST /api/login       # User login
POST /api/logout      # User logout  
GET  /api/me          # Get current user info
```

### Notes
```http
GET    /api/notes           # Get all user notes
POST   /api/notes           # Create new note
PUT    /api/notes/:id       # Update existing note
DELETE /api/notes/:id       # Delete note
OPTIONS /api/notes          # CORS preflight
```

### Request/Response Examples

**Create Note**
```bash
curl -X POST http://localhost:5001/api/notes \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content"}'
```

**Response**
```json
{
  "msg": "Note created!",
  "id": "note-id"
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py
pytest tests/test_notes.py

# Run with coverage
pytest --cov=.
```

### Test Coverage
- **Authentication Tests** - Registration, login, logout, token validation
- **Notes CRUD Tests** - Create, read, update, delete operations
- **Error Handling Tests** - Invalid inputs, authentication errors
- **Database Tests** - MongoDB integration with mocking

## 📁 Project Structure

```
ex1.1-unit-test-daily-notes/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models (User, Note)
│   ├── requirements.txt    # Python dependencies
│   ├── routes/
│   │   ├── auth.py         # Authentication routes
│   │   └── notes.py        # Notes CRUD routes
│   └── tests/
│       ├── conftest.py     # Test configuration
│       ├── test_auth.py    # Authentication tests
│       └── test_notes.py   # Notes functionality tests
├── frontend/
│   ├── app.vue             # Root Vue component
│   ├── nuxt.config.ts      # Nuxt.js configuration
│   ├── package.json        # Node.js dependencies
│   ├── components/
│   │   ├── Footer.vue      # Footer component
│   │   ├── Navbar.vue      # Navigation component
│   │   └── NoteCard.vue    # Note display/edit component
│   ├── composables/
│   │   └── useAuth.js      # Authentication composable
│   ├── layouts/
│   │   └── default.vue     # Default layout
│   ├── middleware/
│   │   └── auth.js         # Route protection middleware
│   ├── pages/
│   │   ├── index.vue       # Home page (redirects to login)
│   │   ├── login.vue       # Login page
│   │   ├── register.vue    # Registration page
│   │   └── dashboard.vue   # Main dashboard
│   ├── plugins/
│   │   └── auth.client.js  # Client-side auth plugin
│   └── assets/
│       └── css/
│           └── main.css    # Global styles
└── README.md              # This file
```

## 🔒 Security Features

- **Password Hashing** - Werkzeug PBKDF2 encryption
- **JWT Tokens** - Secure stateless authentication
- **CORS Configuration** - Controlled cross-origin requests
- **Input Validation** - Server-side data validation
- **Route Protection** - Authenticated-only endpoints

## 🐛 Troubleshooting

### Common Issues

**Port 5001 already in use**
```bash
# Find and kill the process
lsof -ti:5001
kill $(lsof -ti:5001)
```

**MongoDB connection failed**
```bash
# Start MongoDB service
brew services start mongodb-community  # macOS
sudo systemctl start mongod             # Linux
```

**JWT token errors**
- Clear browser localStorage
- Logout and login again
- Check token expiration

**CORS errors**
- Ensure backend is running on port 5001
- Check CORS configuration in `app.py`
- Verify frontend is on port 3000

## 📝 Development Notes

### Adding New Features
1. **Backend** - Add routes in `routes/`, update models in `models.py`
2. **Frontend** - Create components in `components/`, add pages in `pages/`
3. **Tests** - Add corresponding tests in `tests/`

### Database Schema
```javascript
// User Document
{
  _id: ObjectId,
  username: String,
  password: String (hashed)
}

// Note Document  
{
  _id: ObjectId,
  title: String,
  content: String,
  user: ObjectId (reference),
  created_at: DateTime
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

## 🇹🇭 คำแนะนำภาษาไทย

### การติดตั้ง
1. **คลอนโปรเจค** และเข้าไปในโฟลเดอร์
2. **ตั้งค่า Backend** - สร้าง virtual environment และติดตั้ง dependencies
3. **ตั้งค่า Frontend** - ติดตั้ง Node modules และรันเซิร์ฟเวอร์
4. **เปิด MongoDB** - ให้แน่ใจว่า MongoDB กำลังทำงาน

### การใช้งาน
- **สมัครสมาชิก/เข้าสู่ระบบ** ที่หน้าแรก
- **เพิ่มโน้ต** โดยใส่หัวข้อและเนื้อหา
- **แก้ไขโน้ต** โดยคลิก "Edit" และแก้ไขได้ทันที
- **ลบโน้ต** โดยคลิก "Delete"

### การทดสอบ
```bash
cd backend
pytest -v  # รันเทสต์ทั้งหมด
```

### ปัญหาที่พบบ่อย
- **Port ซ้ำ** - หยุดโปรเซสเก่าก่อนรันใหม่
- **MongoDB ไม่เชื่อมต่อ** - ตรวจสอบว่าเซอร์วิสทำงานอยู่
- **Token หมดอายุ** - ออกจากระบบและเข้าใหม่