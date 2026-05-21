# 📚 Library Management System

A full-featured **Library Management System** built using Python and Django. This project provides an efficient platform for librarians and students to manage books, track issues/returns, and handle user authentication seamlessly.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-3.0+-darkgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Features

- ✅ **User Registration & Login** - Secure authentication system for students and librarians
- ✅ **Authentication & Session Management** - Protected routes with role-based access
- ✅ **Book Management** - Add, update, delete, and view books in the library
- ✅ **Book Issuing System** - Issue books to students with tracking
- ✅ **Book Return System** - Track returned books and manage due dates
- ✅ **Student Profiles** - Manage student information and issued books
- ✅ **Protected Routes** - Login-required pages for security
- ✅ **Django Admin Panel** - Built-in admin interface for super-user management

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.8+ |
| **Framework** | Django 3.0+ |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite (default) / PostgreSQL (optional) |
| **Admin Panel** | Django Admin |

---

## 📁 Project Structure

```
library_management/
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
│
├── library_management/            # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                      # User authentication app
│   ├── models.py                  # User models
│   ├── views.py                   # Login, registration views
│   ├── forms.py                   # Authentication forms
│   ├── urls.py                    # App URL routing
│   └── templates/
│
├── books/                         # Book management app
│   ├── models.py                  # Book model
│   ├── views.py                   # Book views
│   ├── urls.py                    # App URL routing
│   └── templates/
│
├── transactions/                  # Issue & return system
│   ├── models.py                  # Transaction models
│   ├── views.py                   # Transaction views
│   ├── urls.py                    # App URL routing
│   └── templates/
│
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── dashboard.html             # Dashboard
│   ├── accounts/                  # Authentication templates
│   ├── books/                     # Book templates
│   └── transactions/              # Transaction templates
│
└── static/                        # CSS & JavaScript files
    ├── css/
    └── js/
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Tanish4196/Project-Demo-.git
cd Project-Demo-
```

### Step 2: Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create a Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin credentials
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## 📖 Usage

### For Students
1. **Register** - Create a new account on the registration page
2. **Login** - Login with your credentials
3. **Browse Books** - View available books in the library
4. **Issue Books** - Request to issue a book (librarian approval may be needed)
5. **Track Issues** - View your currently issued books and due dates
6. **Return Books** - Return issued books through the return system

### For Librarians/Admins
1. **Admin Panel** - Access Django admin at `/admin/`
2. **Manage Books** - Add, update, or delete books from inventory
3. **Approve Issues** - Review and approve book issue requests
4. **Track Transactions** - Monitor all book issues and returns
5. **Manage Students** - View and manage student profiles

---

## 🔐 Security Features

- Password hashing with Django's default security system
- CSRF protection on all forms
- SQL injection prevention through Django ORM
- Session-based authentication
- Login-required decorators on sensitive routes

---

## 📋 Requirements

See `requirements.txt` for all dependencies:
```
Django>=3.0
psycopg2-binary (for PostgreSQL support)
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Tanish Sharma**

- 🔗 **GitHub**: [@Tanish4196](https://github.com/Tanish4196)
- 📧 **Email**: sharmatanish44511@gmail.com

---

## 🙏 Acknowledgments

- Django Documentation & Community
- Stack Overflow for solutions and guidance
- All contributors and users

---

## 📞 Support

If you encounter any issues or have questions, please:
- Open an issue on GitHub
- Contact via email: sharmatanish44511@gmail.com

---

**Made with ❤️ by Tanish Sharma**
