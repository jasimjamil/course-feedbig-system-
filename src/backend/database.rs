use sqlx::{SqlitePool, Error as SqlxError};
use argon2::{
    password_hash::{
        rand_core::OsRng,
        PasswordHash, PasswordHasher, PasswordVerifier, SaltString
    },
    Argon2
};

use crate::models::{User, Feedback, Course};

pub struct DatabaseService {
    pool: SqlitePool,
}

impl DatabaseService {
    pub async fn new(database_url: &str) -> Result<Self, sqlx::Error> {
        let pool = SqlitePool::connect(database_url).await?;
        Ok(Self { pool })
    }

    // User Authentication Methods
    pub async fn register_user(&self, username: &str, password: &str, role: &str) -> Result<i64, sqlx::Error> {
        // Generate salt and hash password
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password_hash = argon2.hash_password(password.as_bytes(), &salt)
            .map_err(|_| SqlxError::Configuration("Password hashing failed".into()))?
            .to_string();

        // Insert user into database
        let id = sqlx::query!(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            username, password_hash, role
        )
        .execute(&self.pool)
        .await?
        .last_insert_rowid();

        Ok(id)
    }

    pub async fn authenticate_user(&self, username: &str, password: &str) -> Result<User, sqlx::Error> {
        // Fetch user by username
        let user = sqlx::query_as!(User, 
            "SELECT * FROM users WHERE username = ?", 
            username
        )
        .fetch_one(&self.pool)
        .await?;

        // Verify password
        let parsed_hash = PasswordHash::new(&user.password)
            .map_err(|_| SqlxError::Configuration("Invalid password hash".into()))?;
        
        Argon2::default()
            .verify_password(password.as_bytes(), &parsed_hash)
            .map_err(|_| SqlxError::Configuration("Authentication failed".into()))?;

        Ok(user)
    }

    // Feedback Methods
    pub async fn submit_feedback(&self, course_id: i64, student_id: i64, content: &str) -> Result<i64, sqlx::Error> {
        let id = sqlx::query!(
            "INSERT INTO feedback (course_id, student_id, content) VALUES (?, ?, ?)",
            course_id, student_id, content
        )
        .execute(&self.pool)
        .await?
        .last_insert_rowid();

        Ok(id)
    }

    pub async fn get_course_feedback(&self, course_id: i64) -> Result<Vec<Feedback>, sqlx::Error> {
        let feedback = sqlx::query_as!(Feedback,
            "SELECT * FROM feedback WHERE course_id = ?",
            course_id
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(feedback)
    }

    pub async fn delete_feedback(&self, feedback_id: i64) -> Result<bool, sqlx::Error> {
        let result = sqlx::query!(
            "DELETE FROM feedback WHERE id = ?",
            feedback_id
        )
        .execute(&self.pool)
        .await?;

        Ok(result.rows_affected() > 0)
    }

    // Course Methods
    pub async fn get_courses_for_instructor(&self, instructor_id: i64) -> Result<Vec<Course>, sqlx::Error> {
        let courses = sqlx::query_as!(Course,
            "SELECT * FROM courses WHERE instructor_id = ?",
            instructor_id
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(courses)
    }
} 