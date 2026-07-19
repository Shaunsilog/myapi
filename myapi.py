from fastapi import FastAPI, Request
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

@app.post("/tasks")
async def create_task(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title or not title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {"id": new_id, "title": title.strip(), "done": False}
    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    if not body:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})
    for task in tasks:
        if task["id"] == task_id:
            if "title" in body:
                if not body["title"] or not body["title"].strip():
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = body["title"].strip()
            if "done" in body:
                if not isinstance(body["done"], bool):
                    return JSONResponse(status_code=400, content={"error": "Done must be true or false"})
                task["done"] = body["done"]
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return JSONResponse(status_code=204, content=None)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
