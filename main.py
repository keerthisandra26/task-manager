from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = []
projects = []
tasks = []

# ---------------- USER ----------------

@app.post("/signup")
def signup(username: str, password: str, role: str):
    user_id = len(users) + 1
    users.append({
        "id": user_id,
        "username": username,
        "password": password,
        "role": role
    })
    return {"user_id": user_id, "role": role}


@app.post("/login")
def login(username: str, password: str):
    for u in users:
        if u["username"] == username and u["password"] == password:
            return {"user_id": u["id"], "role": u["role"]}
    raise HTTPException(status_code=400, detail="Invalid credentials")


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    global users
    users = [u for u in users if u["id"] != user_id]
    return {"message": "User deleted"}


# ---------------- PROJECT ----------------

@app.post("/project")
def create_project(name: str, admin_id: int):
    project_id = len(projects) + 1
    projects.append({
        "id": project_id,
        "name": name,
        "admin_id": admin_id
    })
    return {"project_id": project_id}


# ---------------- TASK ----------------

@app.post("/task")
def create_task(title: str, user_id: int, project_id: int, admin_id: int):
    task_id = len(tasks) + 1
    tasks.append({
        "id": task_id,
        "title": title,
        "user_id": user_id,
        "project_id": project_id,
        "status": "pending"
    })
    return {"task_id": task_id}


@app.put("/task/{task_id}")
def update_task(task_id: int, status: str):
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            return {"message": "Task updated"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"message": "Task deleted"}


@app.get("/tasks")
def get_tasks():
    return tasks


# ---------------- DASHBOARD ----------------

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


# ---------------- TEAM ----------------

@app.get("/project/{project_id}/team")
def team(project_id: int):
    member_ids = [t["user_id"] for t in tasks if t["project_id"] == project_id]

    names = []
    for u in users:
        if u["id"] in member_ids:
            names.append(u["username"])

    return {"team_members": names}