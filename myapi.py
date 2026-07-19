from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Write report", "done": False},
]

health= {
    1 : {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
}
@app.get("/")
def index():
    return health

@app.get("/health")
def check_health():
    return {"status" : "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
