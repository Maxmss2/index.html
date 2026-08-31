"""VÍDEOCREATOR Engine - orquestrador remoto de geração de vídeos."""
from datetime import datetime, timezone
from pathlib import Path
import json
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from engines import engine_status, run_video_engine, get_remote_job

app = FastAPI(title="VÍDEOCREATOR Engine", version="0.6.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

jobs: dict[str, dict] = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / "progress.json"

class Command(BaseModel):
    command: str = Field(min_length=10, max_length=5000)
    limit: int = Field(default=1, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "online", "engine": "VÍDEOCREATOR Engine", "version": "0.6.0", "worker": engine_status()}

@app.get("/progress")
def project_progress():
    if not PROGRESS_FILE.exists():
        raise HTTPException(status_code=404, detail="Progresso do projeto não configurado")
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))

@app.get("/engines")
def list_engines():
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
            "stages": {"research": "pending", "script": "pending", "voice": "pending", "media": "pending", "captions": "pending", "render": "pending", "publish": "pending"},
        })
    jobs[job_id] = {"id": job_id, "command": data.command, "status": "queued", "created_at": datetime.now(timezone.utc).isoformat(), "videos": videos}
    return {"job_id": job_id, "status": "queued", "videos": videos}

@app.post("/jobs/{job_id}/run")
def run_job(job_id: str, dry_run: bool = False):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    results = []
    for video in job["videos"]:
        result = run_video_engine(video["id"], video["script"], dry_run=dry_run)
        video["engine_result"] = result
        video["status"] = result.get("status", "failed")
        video["remote_job_id"] = result.get("remote_job_id")
        if result.get("status") in {"started", "validated"}:
            video["stages"]["voice"] = "queued"
            video["stages"]["media"] = "queued"
            video["stages"]["captions"] = "queued"
            video["stages"]["render"] = "queued"
        results.append(result)
    job["status"] = "started" if any(r.get("status") == "started" for r in results) else results[0].get("status", "failed")
    return {"job_id": job_id, "status": job["status"], "mode": "dry_run" if dry_run else "render", "results": results}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    for video in job["videos"]:
        remote_id = video.get("remote_job_id")
        if remote_id:
            remote = get_remote_job(remote_id)
            data = remote.get("data", remote)
            remote_status = data.get("status")
            if remote_status:
                video["remote_status"] = data
                if remote_status == "completed":
                    video["status"] = "completed"
                    for stage in ("voice", "media", "captions", "render"):
                        video["stages"][stage] = "completed"
                elif remote_status == "failed":
                    video["status"] = "failed"
    if job["videos"] and all(v["status"] == "completed" for v in job["videos"]):
        job["status"] = "completed"
    elif any(v["status"] == "failed" for v in job["videos"]):
        job["status"] = "failed"
    return job

@app.get("/architecture")
def architecture():
    return {"pipeline": ["research", "script", "voice", "media", "captions", "render", "publish"], "worker": "remote Render service", "validation": "dry-run disponível antes da renderização"}
