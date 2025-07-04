use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct User {
    pub id: i64,
    pub username: String,
    pub password: String,
    pub role: String,
}

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct Course {
    pub id: i64,
    pub name: String,
    pub instructor_id: Option<i64>,
}

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct Feedback {
    pub id: i64,
    pub course_id: i64,
    pub student_id: i64,
    pub content: String,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LoginRequest {
    pub username: String,
    pub password: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct FeedbackSubmission {
    pub course_id: i64,
    pub content: String,
} 