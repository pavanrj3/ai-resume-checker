from fastapi import FastAPI
from modules import ResumeRequest   # or rename modules.py → models.py
from analyzer import analyze_resume

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Resume API Running"}

@app.post("/analyze")
def analyze(data: ResumeRequest):
    result = analyze_resume(data.resume)
    return {"result": result}