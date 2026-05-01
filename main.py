from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ---------------- MODELS ----------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    tasks = relationship("Task", back_populates="user")


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String, default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")


Base.metadata.create_all(bind=engine)


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- AUTH ----------------

@app.post("/signup")
def signup(username: str, password: str, role: str, db: Session = Depends(get_db)):
    if not username or not password or role not in ["admin", "member"]:
        raise HTTPException(status_code=400, detail="Invalid input")

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username exists")

    user = User(username=username, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg": "User created", "user_id": user.id}


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username, password=password).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid login")

    return {"user_id": user.id, "role": user.role}


# ---------------- PROJECT ----------------

@app.post("/project")
def create_project(name: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    if not name:
        raise HTTPException(status_code=400, detail="Project name required")

    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)

    return {"msg": "Project created", "project_id": project.id}


# ---------------- TASK ----------------

@app.post("/task")
def create_task(title: str, user_id: int, project_id: int, created_by: int, db: Session = Depends(get_db)):

    admin = db.query(User).filter(User.id == created_by).first()
    assigned_user = db.query(User).filter(User.id == user_id).first()
    project = db.query(Project).filter(Project.id == project_id).first()

    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    if not assigned_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not title:
        raise HTTPException(status_code=400, detail="Title required")

    task = Task(title=title, user_id=user_id, project_id=project_id)
    db.add(task)
    db.commit()
    db.refresh(task)

    return {"msg": "Task created", "task_id": task.id}


# ---------------- GET TASKS ----------------

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    result = []
    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "user": t.user.username if t.user else "",
            "project": t.project.name if t.project else ""
        })

    return result


# ---------------- UPDATE TASK ----------------

@app.put("/task/{task_id}")
def update_task(task_id: int, status: str, user_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if status not in ["pending", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    if user.role != "admin" and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    task.status = status
    db.commit()
    db.refresh(task)

    return {"msg": "Task updated", "status": task.status}


# ---------------- DELETE TASK ----------------

@app.delete("/task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"msg": "Task deleted"}


# ---------------- DASHBOARD ----------------

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    tasks = db.query(Task).all()

    total = len(tasks)
    done = len([t for t in tasks if t.status == "done"])
    pending = len([t for t in tasks if t.status == "pending"])

    return {
        "total_tasks": total,
        "completed_tasks": done,
        "pending_tasks": pending
    }


# ---------------- TEAM MANAGEMENT ----------------

@app.get("/project/{project_id}/team")
def get_project_team(project_id: int, db: Session = Depends(get_db)):

    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    users = set()
    for t in tasks:
        if t.user:
            users.add(t.user.username)

    return {
        "project_id": project_id,
        "team_members": list(users)
    }