"""Integração da VÍDEOCREATOR com o Worker remoto de vídeo.

O motor open-source roda no serviço Render Worker. A Engine não tenta mais
instalá-lo localmente; ela envia jobs para o Worker HTTP e acompanha o status.
"""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

WORKER_URL = os.getenv("VIDEO_WORKER_URL", "https://videocreator-worker.onrender.com").rstrip("/")


def _request(path: str, method: str = "GET", payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(f"{WORKER_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except (HTTPError, URLError, TimeoutError) as exc:
        return {"status": "failed", "message": f"Worker indisponível: {exc}"}


def engine_status() -> dict[str, Any]:
    health = _request("/api/health", timeout=15)
    online = health.get("success") is not False and health.get("status") not in {"failed", None}
    return {
        "id": "automated-video-generator",
        "name": "Automated Video Generator",
        "configured": bool(WORKER_URL) and online,
        "path": WORKER_URL,
        "package_detected": online,
        "capabilities": ["voice", "media", "captions", "render", "dry_run"],
        "setup_required": not online,
        "mode": "remote_worker",
    }


def run_video_engine(job_id: str, command: str, dry_run: bool = False) -> dict[str, Any]:
    """Cria um job real no Worker e devolve os identificadores para acompanhamento."""
    status = engine_status()
    if not status["configured"]:
        return {"status": "needs_setup", "message": "Worker de vídeo não está disponível.", "worker_url": WORKER_URL}

    title = f"VÍDEOCREATOR {job_id[:8]}"
    payload = {
        "title": title,
        "script": command,
        "orientation": "portrait",
        "language": "portuguese",
        "showText": True,
        "skipReview": True,
        "exportCaptions": True,
    }
    if dry_run:
        payload["skipReview"] = False

    result = _request("/api/jobs", method="POST", payload=payload, timeout=60)
    if result.get("status") == "failed":
        return result
    data = result.get("data", result)
    remote_id = data.get("jobId") or data.get("id")
    return {
        "status": "validated" if dry_run else "started",
        "remote_job_id": remote_id,
        "status_url": data.get("statusUrl") or data.get("statusPageUrl"),
        "worker_url": WORKER_URL,
        "message": "Job enviado ao Worker remoto.",
    }


def get_remote_job(remote_job_id: str) -> dict[str, Any]:
    return _request(f"/api/jobs/{remote_job_id}", timeout=30)
