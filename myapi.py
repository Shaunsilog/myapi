from fastapi import FastAPI

app = FastAPI()

health= {
    1 : {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
}
@app.get("/")
def index(health_id:int):
    return health[health_id]
    
@app.get("/health")
def check_health():
    return {"status" : "ok"}

