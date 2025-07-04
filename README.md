# Course Feedback System 🎓

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://course-feedback-system.streamlit.app)

## 🚀 Live Demo
[Access the Live Streamlit App](https://course-feedback-system.streamlit.app)

## 📝 Project Overview
A modern Course Feedback System built with Python and Streamlit, enabling students, instructors, and administrators to interact through a comprehensive feedback platform.

## ✨ Features
- 🌟 5-Star Course Rating System
- 🔐 Secure User Authentication
- 📊 Detailed Feedback Submission
- 🎨 Responsive and Modern UI/UX
- 🔄 Automatic Database Migrations

## 🛠 Tech Stack
- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- Authentication: Custom Secure Mechanism

## 🚀 Quick Start

### Local Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/course-feedback-system.git
cd course-feedback-system
```

2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the Application
```bash
streamlit run src/frontend/app.py
```

### Deployment on Streamlit
1. Fork the repository
2. Connect your GitHub repository to Streamlit
3. Select the main branch
4. Deploy!

## 🌈 User Roles
- **Students**: Submit and rate course feedback
- **Instructors**: View and analyze course feedback
- **Administrators**: Manage courses and feedback system

## 🔒 Security Features
- Password hashing
- Role-based access control
- Input validation
- Secure database interactions

## 🛡 Database Management
- Automatic schema migrations
- Flexible database structure
- Backward compatibility

## 🚧 Future Roadmap
- Advanced analytics dashboard
- Machine learning insights
- Enhanced reporting features

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact
Your Name - [Your Email]

Project Link: [https://github.com/yourusername/course-feedback-system](https://github.com/yourusername/course-feedback-system)

## 🌟 Modern UI/UX Features
- Sleek, professional design with modern color scheme
- Responsive layout with intuitive navigation
- Role-based color coding
- Animated interactive elements
- Clean, minimalist interface

## 🔄 Database Migration
- Automatic schema update mechanism
- Backward compatibility with existing databases
- Seamless handling of database structure changes
- Prevents data loss during upgrades

## 📊 Feedback Enhancement
- 5-star rating system
- Detailed feedback submission
- Visual star rating display
- Flexible feedback mechanism
- Comprehensive feedback tracking

## Overview
A cutting-edge Course Feedback Platform designed to provide a seamless, engaging user experience for students, instructors, and administrators.

## 🚀 Key Features
- **Intelligent Database Management**
  - Automatic schema migrations
  - Robust error handling
  - Flexible database structure

- **Advanced Feedback System**
  - 5-star course rating
  - Detailed feedback submission
  - Instructor feedback analysis
  - Visual rating representation

- **Elegant User Authentication**
  - Modern login/registration interface
  - Secure password validation
  - Role-based access control

## 🔒 Security Enhancements
- Automatic database schema protection
- Password strength validation
- Secure authentication mechanism
- Role-based access control
- Comprehensive error handling

## 📊 Technical Highlights
- Modern UI/UX design
- Responsive Streamlit interface
- SQLite database backend
- Secure password hashing
- Detailed course and feedback tracking

## Prerequisites
- Python 3.8+
- pip

## Installation
1. Clone the repository
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
```bash
streamlit run src/frontend/app.py
```

## 🌈 User Roles
- **Students**: 
  - Submit course feedback
  - Rate courses (1-5 stars)
  - Provide detailed feedback
- **Instructors**: 
  - View and analyze course feedback
  - See detailed student ratings
- **Administrators**: 
  - Manage courses and feedback
  - Oversee feedback system

## Future Roadmap
- Advanced database migration tools
- Comprehensive feedback analytics
- Machine learning-powered insights
- Enhanced rating and feedback visualization

## Contributing
We welcome contributions! Please read our contribution guidelines before getting started.

## Features
- User Registration (Student, Instructor, Admin)
- User Authentication
- Students can:
  - View available courses
  - Submit feedback for courses
- Instructors can:
  - View feedback for courses
- Admins can:
  - Add new courses
  - Delete feedback by ID

## Database
- SQLite is used for data storage
- Database file: `feedback.db`
- Tables: 
  - users
  - courses
  - feedback

## Security
- Passwords are hashed using SHA-256
- Basic role-based access control implemented

## Troubleshooting
- If no courses are available, an admin can add courses through the admin panel
- Ensure you have the latest version of Streamlit installed

## Future Improvements
- Implement more robust password hashing
- Add more detailed input validation
- Enhance error handling
- Create more comprehensive reporting
- Add course assignment for instructors 