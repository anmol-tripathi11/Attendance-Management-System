📚 Attendance Management System
A comprehensive, modern web application for digital attendance tracking in educational institutions. Features three-tier access for administrators, teachers, and students with real-time reporting and analytics.

✨ Features
👨‍💼 Admin Dashboard
Add, edit, and delete teacher accounts

View system-wide statistics and analytics

Manage teacher-subject-department assignments

Monitor overall system performance

👩‍🏫 Teacher Dashboard
Mark attendance for assigned subjects and departments

Add, edit, and manage student records

View attendance history and student performance

Generate subject-wise attendance reports

👩‍🎓 Student Dashboard
View personal attendance records

Check subject-wise attendance percentages

Monitor overall attendance statistics

Access historical attendance data

🚀 Quick Start
Prerequisites
Python 3.8 or higher

Modern web browser (Chrome, Firefox, Safari, Edge)

Installation
Run the backend server

bash
python backend.py
The server will start at http://localhost:5000

Open the frontend

Open index.html in your browser, OR

Navigate to http://localhost:5000

Default Login Credentials
Role	User ID	Password
Admin	ADMIN_001	admin123
Teacher	TCH_001	teacher123
Student	STU_001	student123
🏗️ Architecture
Frontend
Pure HTML, CSS, JavaScript – No frameworks or build tools required

Responsive Design – Works on desktop and mobile devices

Modern UI – Clean, intuitive interface with smooth animations

Real-time Updates – Live connection status and notifications

Backend
Flask – Lightweight Python web framework

JSON Database – Simple file-based storage (no SQL required)

CORS Enabled – Secure cross-origin resource sharing

RESTful API – Well-structured endpoints for all operations

Data Structure
text
database.json
├── users
│   ├── admin
│   ├── teachers
│   └── students
├── teacher_assignments
├── student_data
├── attendance_records
├── available_departments
└── available_subjects
📊 API Endpoints
Authentication
POST /api/login – User authentication

POST /api/logout – Session termination

Admin Endpoints
POST /api/admin/add-teacher – Add new teacher

GET /api/admin/teachers – List all teachers

GET /api/admin/available-data – Get departments and subjects

GET /api/system/stats – System statistics

Teacher Endpoints
POST /api/teacher/add-student – Add new student

POST /api/teacher/mark-attendance – Mark daily attendance

GET /api/teacher/students – View assigned students

GET /api/teacher/view-attendance – Attendance history

Student Endpoints
GET /api/student/attendance – Personal attendance records

GET /api/student/subject-attendance – Subject-wise statistics

🎨 UI Components
Role Selection Screen
Three distinct cards for Admin, Teacher, and Student roles with:

Role-specific icons and descriptions

Feature highlights for each role

Smooth hover animations

Login Modal
Role-specific login forms

Password visibility toggle

Connection status indicator

Demo credentials display

Dashboard Layout
User profile header with logout

Action cards for main functions

Dynamic content area

Real-time notifications

📱 Responsive Design
The application is fully responsive and adapts to:

Desktop (≥ 1024px) – Full dashboard layout

Tablet (768px - 1023px) – Adjusted grid layouts

Mobile (< 768px) – Single column, touch-optimized

🔧 Technical Highlights
No Dependencies
Zero npm packages – Pure vanilla JavaScript

No build process – Direct file execution

No database setup – JSON-based persistence

Real-time Features
Connection monitoring – Live backend status

Instant notifications – Success/error messages

Live data updates – No page refresh needed

Security Features
Session management – User authentication

Role-based access – Permission control

Input validation – Form security

CORS protection – API security headers

📁 Project Structure
text
attendance-management-system/
│
├── index.html              # Main frontend file
├── backend.py              # Flask backend server
├── database.json           # JSON database file
├── README.md              # This file
🚀 Deployment
Local Deployment
Ensure Python is installed

Run python backend.py

Access via http://localhost:5000

Cloud Deployment
The application can be easily deployed to:

Heroku (with Procfile)

PythonAnywhere

Replit

Railway

Any Python-compatible hosting service

🐛 Troubleshooting
Common Issues
Backend not connecting:

Check if Python is running: python --version

Verify port 5000 is free

Ensure all required files are in the same directory

Database issues:

Check database.json file permissions

Verify JSON format is valid

Restart the backend server

Browser console errors:

Clear browser cache

Check browser console for specific errors

Verify CORS headers in backend response

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
