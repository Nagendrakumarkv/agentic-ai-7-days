from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from ai_service import generate_project
from sandbox import SandboxManager

app = FastAPI()
sandbox = SandboxManager(os.path.join(os.path.dirname(__file__), "workspace"))

class GenerateRequest(BaseModel):
    prompt: str
    chat_history: list[dict] = []

@app.post("/api/generate")
def generate(req: GenerateRequest):
    try:
        files, raw_text = generate_project(req.prompt, req.chat_history)
        if not files:
            raise HTTPException(status_code=400, detail="Failed to parse files from the output. Ensure Gemini responded correctly.")
            
        sandbox.write_files(files)
        success = sandbox.restart_server()
        
        return {
            "success": success,
            "raw_text": raw_text,
            "files": files,
            "sandbox_url": "http://127.0.0.1:8001"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
