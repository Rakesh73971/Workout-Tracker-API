# Workout Tracker API 🏋️‍♂️

A **Workout & Fitness Tracking REST API** built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This project helps users track workouts, exercises, exercise logs, and body measurements with secure user-based access and pagination support.

---

## 🚀 Features

* User authentication & ownership-based data access
* Workout creation and management
* Exercise master data (categories, muscle groups, equipment)
* Workout–Exercise mapping with sets, reps, weight, and duration
* Exercise logging for daily performance tracking
* Body measurement tracking over time
* Pagination for large datasets
* Cascading deletes for user-owned data

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation & Serialization:** Pydantic
* **Authentication:** JWT (Token-based)
* **Migrations:** Alembic (recommended)

---

## 📦 Database Models

### User

Stores user profile and physical attributes.

* id, name, email, password
* age, gender, height, weight
* created_at

### Workout

Represents a workout session created by a user.

* title, workout_date, total_duration, notes
* owner_id → User

### Exercise

Master table for exercises.

* name, description, category
* muscle_group, equipment

### WorkoutExercise

Mapping table between workouts and exercises.

* workout_id → Workout
* exercise_id → Exercise
* sets, reps, weight, duration

### ExerciseLog

Tracks individual exercise performance history.

* exercise_id → Exercise
* sets, reps, weight, duration
* owner_id → User

### BodyMeasurement

Stores body metrics over time.

* weight, chest, waist, arms, thighs
* owner_id → User

---

## 📄 API Schemas (Pydantic)

* Request & response validation using **Pydantic models**
* Separate schemas for:

  * Create
  * Update
  * Response
* Pagination schemas included for:

  * Exercises
  * Workouts
  * Workout Exercises
  * Exercise Logs
  * Body Measurements

---

## 🔐 Authentication Flow

1. User registers and logs in
2. JWT token is generated
3. Token must be passed in `Authorization` header
4. All protected routes validate token and user ownership

```
Authorization: Bearer <access_token>
```

---

## 📑 Pagination Format

All paginated endpoints follow this response format:

```json
{
  "data": [],
  "total": 100,
  "page": 1,
  "totalPages": 10
}
```
---

## ▶️ Running the Project

1. Clone the repository
2. Create virtual environment & install dependencies
3. Set up `.env` with database URL and secret key
4. Run migrations
5. Start the server

```
uvicorn app.main:app --reload
```

## 👨‍💻 Author

**Rakesh**
Backend Developer | FastAPI | Django | SQL
B.Tech CSE (AIML)


