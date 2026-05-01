from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy in-memory storage (for simplicity)
users = []
projects = []
tasks = []

# ================= SIGNUP =================
@app.post("/signup")
def signup(username: str, password: str, role: str):
    user_id = len(users) + 1
    users.append({
        "id": user_id,
        "username": username,
        "password": password,
        "role": role
    })
    return {"message": "User created", "user_id": user_id}

# ================= LOGIN =================
@app.post("/login")
def login(username: str, password: str):
    for u in users:
        if u["username"] == username and u["password"] == password:
            return {"user_id": u["id"], "role": u["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ================= CREATE PROJECT =================
@app.post("/project")
def create_project(name: str, admin_id: int):
    project_id = len(projects) + 1
    projects.append({
        "id": project_id,
        "name": name,
        "admin_id": admin_id
    })
    return {"project_id": project_id}

# ================= CREATE TASK =================
@app.post("/task")
def create_task(title: str, user_id: int, project_id: int, admin_id: int):
    task_id = len(tasks) + 1
    tasks.append({
        "id": task_id,
        "title": title,
        "status": "pending",
        "user_id": user_id,
        "project_id": project_id
    })
    return {"task_id": task_id}

# ================= GET TASKS =================
@app.get("/tasks")
def get_tasks():
    return tasks

# ================= DASHBOARD =================
@app.get("/dashboard")
def dashboard():
    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "done"])
    pending = total - done

    return {
        "total_tasks": total,
        "completed_tasks": done,
        "pending_tasks": pending
    }

# ================= TEAM =================
@app.get("/project/{project_id}/team")
def team(project_id: int):
    members = set()
    for t in tasks:
        if t["project_id"] == project_id:
            members.add(f"user{t['user_id']}")

    return {
        "project_id": project_id,
        "team_members": list(members)
    }