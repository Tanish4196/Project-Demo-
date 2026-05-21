📚 Library Management System

A full-featured Library Management System built using Python and Django. This project allows librarians/admins to manage books, issue/return books, and handle user authentication efficiently.

🚀 Features
👤 User Registration & Login System
🔐 Authentication & Session Management
📚 Add, Update, Delete Books
🔍 View Available Books
📖 Issue Books to Students
↩️ Return Books System
📊 Track Issued Books
🧑 Student Profile Management
🔒 Protected Routes (Login Required)
🛠️ Tech Stack
Backend: Python
Framework: Django
Database: SQLite (default) / PostgreSQL (optional)
Frontend: HTML, CSS
Admin Panel: Django Admin


📁 Project Structure
library_management/
│
├── manage.py
├── requirements.txt
│
├── library_management/        # Main project settings
│
├── accounts/                  # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│
├── books/                     # Book management app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── transactions/             # Issue & return system
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── templates/                # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── accounts/
│   ├── books/
│   ├── transactions/
│
└── static/                   # CSS/JS files

👨‍💻 Author

Tanish Sharma

GitHub: https://github.com/Tanish4196
Email: sharmatanish44511@gmail.com
