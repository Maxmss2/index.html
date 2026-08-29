"""VÍDEOCREATOR Engine - núcleo independente para automação de vídeos."""
from datetime import datetime, timezone
from pathlib import Path
import json
from uuid import uuid4
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from engines import engine_status, run_video_engine

app = FastAPI(title="VÍDEOCREATOR Engine", version="0.5.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

jobs: dict[str, dict] = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / "progress.json"

class Command(BaseModel):
    command: str = Field(min_length=3, max_length=4000)
    limit: int = Field(default=1, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "online", "engine": "VÍDEOCREATOR Engine", "version": "0.5.0"}

@app.get("/progress")
def project_progress():
    """Retorna o progresso real registrado do desenvolvimento do projeto."""
    if not PROGRESS_FILE.exists():
        raise HTTPException(status_code=404, detail="Progresso do projeto não configurado")
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))

@app.get("/engines")
def list_engines():
    """Mostra os motores open-source que a VÍDEOCREATOR consegue orquestrar."""
    return {"engines": [engine_status()]}

@app.post("/jobs")
def create_job(data: Command):
    job_id = str(uuid4())
    videos = []
    for i in range(data.limit):
        videos.append({
            "id": f"{job_id}-{i+1}",
            "title": f"Produção {i+1}",
            "script": data.command,
            "status": "queued",
            "stages": {
                "research": "pending", "script": "pending", "voice": "pending",
                "media": "pending", "captions": "pending", "render": "pending", "publish": "pending"
            }
        })
    jobs[job_id] = {"id": job_id, "command": data.command, "status": "queued", "created_at": datetime.now(timezone.utc).isoformat(), "videos": videos}
    return {"job_id": job_id, "status": "queued", "videos": videos}

def execute_job(job_id: str, dry_run: bool = False):
    job = jobs[job_id]
    job["status"] = "validating" if dry_run else "processing"
    job["dry_run"] = dry_run
    for video in job["videos"]:
        video["status"] = "validating" if dry_run else "processing"
        video["stages"]["voice"] = "processing"
        video["stages"]["media"] = "processing"
        result = run_video_engine(video["id"], video["script"], dry_run=dry_run)
        video["engine_result"] = result
        video["status"] = result["status"]
        if result["status"] == "completed":
            for stage in ("voice", "media", "captions", "render"):
                video["stages"][stage] = "completed"
        elif result["status"] == "validated":
            for stage in ("voice", "media", "captions"):
                video["stages"][stage] = "validated"
            video["stages"]["render"] = "skipped_dry_run"
        elif result["status"] == "needs_setup":
            video["status"] = "waiting_for_engine"
    success_states = {"completed"} if not dry_run else {"validated"}
    job["status"] = "validated" if all(v["status"] in success_states for v in job["videos"]) else "waiting_or_failed"

@app.post("/jobs/{job_id}/run")
def run_job(job_id: str, background_tasks: BackgroundTasks, dry_run: bool = False):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    if not engine_status()["configured"]:
        return {"job_id": job_id, "status": "needs_setup", "engine": engine_status()}
    background_tasks.add_task(execute_job, job_id, dry_run)
    return {
        "job_id": job_id,
        "status": "validation_started" if dry_run else "started",
        "mode": "dry_run" if dry_run else "render",
        "engine": "automated-video-generator",
    }

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    return job

@app.get("/architecture")
def architecture():
    return {
        "pipeline": ["research", "script", "voice", "media", "captions", "render", "publish"],
        "note": "A VÍDEOCREATOR orquestra motores open-source por adaptadores intercambiáveis.",
        "validation": "O modo dry-run valida o pipeline do motor antes da renderização final.",
    }
