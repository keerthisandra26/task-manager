# Task Manager (Full-Stack Web App)

##  Overview

This project is a **Task Manager Web Application** built using **FastAPI (backend)** and **HTML, CSS, JavaScript (frontend)**.
It allows users to create projects, assign tasks, and track progress with **role-based access control (Admin / Member)**.

The goal of this project is to demonstrate **full-stack development skills**, including API development, database management, and UI interaction.

---

##  Features

###  Authentication

* Users can **Sign up and Login**
* Each user has a role:

  * **Admin** → can create projects and assign tasks
  * **Member** → can update their assigned tasks

---

###  Project Management

* Admin can:

  * Create new projects
* Projects act as containers for tasks

---

###  Task Management

* Admin can:

  * Create tasks
  * Assign tasks to users
* Users can:

  * Update task status (done / pending)
* Tasks belong to:

  * A specific **project**
  * A specific **user**

---

### Dashboard

Displays:

* Total number of tasks
* Completed tasks
* Pending tasks

This helps in tracking overall progress.

---

### Team Management

* Shows all users working under a project
* Helps identify team members involved in a project

---

##  Tech Stack

### Backend

* **FastAPI** – API framework
* **SQLAlchemy** – ORM for database operations
* **SQLite** – Lightweight database

### Frontend

* HTML
* CSS (for styling UI)
* JavaScript (Fetch API for backend communication)

---

##  Database Structure

### User Table

* id
* username
* password
* role

### Project Table

* id
* name

### Task Table

* id
* title
* status
* user_id (assigned user)
* project_id (linked project)

 Relationships:

* One user → many tasks
* One project → many tasks

---

## API Endpoints

### Authentication

* `POST /signup` → Create user
* `POST /login` → Login user

---

### Project

* `POST /project` → Create project (Admin only)

---

### Task

* `POST /task` → Create task
* `GET /tasks` → Get all tasks
* `PUT /task/{id}` → Update task
* `DELETE /task/{id}` → Delete task

---

### Additional Features

* `GET /dashboard` → Get task summary
* `GET /project/{id}/team` → Get project members

---

##  How to Run the Project

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run backend server

```bash
uvicorn main:app --reload
```

### Step 3: Open frontend

* Open `index.html` in browser
* OR use Live Server

---

##  Deployment

The application is deployed using **Railway**.

 The app is fully functional and accessible online.

---

##  Limitations / Future Improvements

* No password hashing (can be improved )
* Basic UI (can be upgraded using React)
* No authentication tokens

---

##  Author

**S.KEERTHI**

B.Tech CSE (AIML)  
Email: keerthisandra26@gmail.com  

---
