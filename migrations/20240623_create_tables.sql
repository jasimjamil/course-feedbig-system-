-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'instructor', 'admin'))
);

-- Courses table
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    instructor_id INTEGER,
    FOREIGN KEY(instructor_id) REFERENCES users(id)
);

-- Feedback table
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(student_id) REFERENCES users(id)
);

-- Create initial admin user
INSERT INTO users (username, password, role) VALUES ('admin', '$argon2id$v=19$m=4096,t=3,p=1$c2FsdHNhbHQ$...', 'admin'); 