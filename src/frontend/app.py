import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

# Custom CSS for enhanced UI/UX
def set_custom_style():
    st.markdown("""
    <style>
    /* Global Styles */
    body {
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        background-color: #f4f6f9;
    }

    /* Main Container Styling */
    .main-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        padding: 30px;
        margin: 20px;
    }

    /* Header Styles */
    .title {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Button Styles */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }

    /* Input Styles */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }

    /* Feedback Card Styles */
    .feedback-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    /* Role-based Color Coding */
    .student-role { color: #27ae60; }
    .instructor-role { color: #e67e22; }
    .admin-role { color: #e74c3c; }

    /* Sidebar Styling */
    .css-1aumxhk {
        background-color: #2c3e50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

class CourseFeedbackApp:
    def __init__(self, db_path='feedback.db'):
        self.db_path = db_path
        self.init_database()
        self.migrate_database()
        self.init_default_courses()

    def init_database(self):
        """Initialize the SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    instructor_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(instructor_id) REFERENCES users(id)
                )
            ''')
            # Feedback table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY,
                    course_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(course_id) REFERENCES courses(id),
                    FOREIGN KEY(student_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

    def migrate_database(self):
        """Perform database schema migrations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Migration for courses table
            try:
                cursor.execute('SELECT description FROM courses LIMIT 1')
            except sqlite3.OperationalError:
                cursor.execute('ALTER TABLE courses ADD COLUMN description TEXT')
                conn.commit()

            # Migration for feedback table
            try:
                cursor.execute('SELECT rating FROM feedback LIMIT 1')
            except sqlite3.OperationalError:
                # Add rating column with a default value
                cursor.execute('''
                    ALTER TABLE feedback 
                    ADD COLUMN rating INTEGER CHECK(rating BETWEEN 1 AND 5) DEFAULT 3
                ''')
                conn.commit()

    def init_default_courses(self):
        """Initialize default courses if none exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if courses exist
            cursor.execute('SELECT COUNT(*) FROM courses')
            if cursor.fetchone()[0] == 0:
                # Insert some default courses with descriptions
                default_courses = [
                    ('Introduction to Computer Science', 'Foundational course covering basic programming concepts and computational thinking.'),
                    ('Data Structures and Algorithms', 'In-depth exploration of fundamental data structures and algorithm design.'),
                    ('Web Development Fundamentals', 'Comprehensive introduction to modern web development technologies.'),
                    ('Machine Learning Basics', 'Introductory course to machine learning principles and practical applications.')
                ]
                cursor.executemany(
                    'INSERT INTO courses (name, description, instructor_id) VALUES (?, ?, ?)', 
                    [(course[0], course[1], None) for course in default_courses]
                )
                conn.commit()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, role):
        """Register a new user with validation"""
        # Basic password validation
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                hashed_password = self.hash_password(password)
                cursor.execute(
                    'INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                    (username, hashed_password, role)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def authenticate_user(self, username, password):
        """Authenticate user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)
            cursor.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?', 
                (username, hashed_password)
            )
            return cursor.fetchone()

    def submit_feedback(self, course_id, student_id, content, rating=3):
        """Submit feedback for a course"""
        if not content.strip():
            raise ValueError("Feedback content cannot be empty")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO feedback (course_id, student_id, content, rating) VALUES (?, ?, ?, ?)', 
                (course_id, student_id, content, rating)
            )
            conn.commit()

    def get_courses(self):
        """Retrieve all courses with description"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Use COALESCE to provide a default description if NULL
            cursor.execute('''
                SELECT id, name, COALESCE(description, 'No description available') 
                FROM courses
            ''')
            return cursor.fetchall()

    def get_course_feedback(self, course_id):
        """Retrieve feedback for a specific course"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id, u.username, f.content, f.rating, f.created_at 
                FROM feedback f 
                JOIN users u ON f.student_id = u.id 
                WHERE f.course_id = ?
            ''', (course_id,))
            return cursor.fetchall()

    def delete_feedback(self, feedback_id):
        """Delete a specific feedback"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
            conn.commit()

def main():
    # Set custom styling
    set_custom_style()
    
    # Title with custom styling
    st.markdown('<h1 class="title">🎓 Course Feedback System</h1>', unsafe_allow_html=True)
    
    # Initialize app
    app = CourseFeedbackApp()

    # Session state management
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    # Login/Register Section
    if not st.session_state.logged_in:
        # Use columns for a more modern layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            login_mode = st.radio('Choose Action', ['Login', 'Register'])
            
            username = st.text_input('Username', key='login_username')
            password = st.text_input('Password', type='password', key='login_password')
            
            if login_mode == 'Register':
                role = st.selectbox('Role', ['student', 'instructor', 'admin'])
                
                if st.button('Register'):
                    try:
                        if app.register_user(username, password, role):
                            st.success('Registration Successful! 🎉')
                    except ValueError as e:
                        st.error(str(e))
            
            if st.button('Login'):
                user = app.authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        'id': user[0],
                        'username': user[1],
                        'role': user[3]
                    }
                    st.experimental_rerun()
                else:
                    st.error('Invalid credentials')
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Decorative section with course system description
            st.markdown("""
            <div class="main-container" style="background-color: #e8f4f8; text-align: center;">
            <h2>Welcome to Smart Feedback</h2>
            <p>A modern platform for course evaluation and improvement</p>
            <ul style="list-style-type: none; padding: 0;">
                <li>🌟 Transparent Feedback</li>
                <li>📊 Data-Driven Insights</li>
                <li>🔒 Secure Authentication</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    # Logged-in User Interface
    if st.session_state.logged_in:
        # Sidebar with user info
        st.sidebar.title(f"👤 {st.session_state.user['username']}")
        st.sidebar.markdown(f"**Role**: <span class='{st.session_state.user['role']}-role'>{st.session_state.user['role'].capitalize()}</span>", unsafe_allow_html=True)
        
        # Main content area
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Role-specific interfaces
        if st.session_state.user['role'] == 'student':
            st.header('Submit Course Feedback')
            courses = app.get_courses()
            
            if not courses:
                st.warning('No courses available. Please contact an administrator.')
            else:
                course_options = {name: id for id, name, _ in courses}
                
                selected_course_name = st.selectbox('Select Course', list(course_options.keys()))
                course_id = course_options[selected_course_name]
                
                # Display course description
                st.markdown(f"**Course Description**: {courses[course_id - 1][2]}")
                
                # Rating and feedback
                rating = st.slider('Rate the Course', 1, 5, 3)
                feedback_content = st.text_area('Your Detailed Feedback')
                
                if st.button('Submit Feedback'):
                    try:
                        app.submit_feedback(
                            course_id=course_id, 
                            student_id=st.session_state.user['id'], 
                            content=feedback_content,
                            rating=rating
                        )
                        st.success('Feedback Submitted Successfully! 🎉')
                    except ValueError as e:
                        st.error(str(e))

        # Instructor Interface
        elif st.session_state.user['role'] == 'instructor':
            st.header('Course Feedback')
            courses = app.get_courses()
            
            if not courses:
                st.warning('No courses available.')
            else:
                course_options = {name: id for id, name in courses}
                
                selected_course = st.selectbox('Select Course', list(course_options.keys()))
                
                if st.button('View Feedback'):
                    feedback_list = app.get_course_feedback(course_options[selected_course])
                    if feedback_list:
                        for feedback in feedback_list:
                            # Display feedback with rating
                            st.markdown(f"""
                            <div class="feedback-card">
                            **From {feedback[1]}**: {feedback[2]}
                            
                            **Rating**: {'⭐' * feedback[3]}
                            
                            *Submitted at: {feedback[4]}*
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info('No feedback received for this course')

        # Admin Interface
        elif st.session_state.user['role'] == 'admin':
            st.header('Admin Panel')
            
            # Add Course
            st.subheader('Add New Course')
            new_course_name = st.text_input('Course Name')
            if st.button('Create Course'):
                with sqlite3.connect(app.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO courses (name, instructor_id) VALUES (?, ?)', 
                                   (new_course_name, None))
                    conn.commit()
                st.success(f'Course "{new_course_name}" added successfully!')

            # Delete Feedback
            st.subheader('Delete Feedback')
            feedback_id = st.number_input('Enter Feedback ID to Delete', min_value=1)
            
            if st.button('Delete Feedback'):
                app.delete_feedback(feedback_id)
                st.success(f'Feedback {feedback_id} deleted successfully')

        st.markdown('</div>', unsafe_allow_html=True)

        # Logout button
        if st.sidebar.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.experimental_rerun()

if __name__ == '__main__':
    main() 
