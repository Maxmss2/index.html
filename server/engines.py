"""Adaptadores de motores externos para a VÍDEOCREATOR.

A VÍDEOCREATOR não reimplementa o renderizador de vídeo: ela orquestra motores
open-source instalados localmente. O primeiro adaptador suporta o repositório
Automated Video Generator (MIT) por meio do seu pipeline oficial.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

ENGINE_ROOT = Path(os.getenv("AUTOMATED_VIDEO_GENERATOR_PATH", "")).expanduser()


def engine_status() -> dict[str, Any]:
    configured = bool(str(ENGINE_ROOT)) and ENGINE_ROOT.exists()
    return {
        "id": "automated-video-generator",
        "name": "Automated Video Generator",
        "configured": configured,
        "path": str(ENGINE_ROOT) if configured else None,
        "capabilities": ["voice", "media", "captions", "render"],
        "setup_required": not configured,
    }


def build_job_payload(job_id: str, command: str) -> list[dict[str, Any]]:
    """Converte o comando da VÍDEOCREATOR no formato de entrada do motor externo."""
    return [{
        "id": job_id,
        "title": f"VÍDEOCREATOR {job_id[:8]}",
        "orientation": "portrait",
        "language": "portuguese",
        "script": command,
    }]


def run_video_engine(job_id: str, command: str) -> dict[str, Any]:
    """Executa o pipeline oficial do motor instalado localmente.

    Não usa shell=True para evitar injeção de comandos. O motor deve estar
    instalado separadamente e apontado por AUTOMATED_VIDEO_GENERATOR_PATH.
    """
    status = engine_status()
    if not status["configured"]:
        return {
            "status": "needs_setup",
            "message": "Motor de vídeo ainda não instalado neste computador/servidor.",
        }

    input_dir = ENGINE_ROOT / "input" / "scripts"
    input_file = input_dir / "input-scripts.json"
    input_dir.mkdir(parents=True, exist_ok=True)
    input_file.write_text(json.dumps(build_job_payload(job_id, command), ensure_ascii=False, indent=2), encoding="utf-8")

    process = subprocess.run(
        ["npm", "run", "generate"],
        cwd=ENGINE_ROOT,
        capture_output=True,
        text=True,
        timeout=int(os.getenv("VIDEO_ENGINE_TIMEOUT", "3600")),
        check=False,
    )

    output_dir = ENGINE_ROOT / "output" / job_id
    videos = [str(path) for path in output_dir.glob("*.mp4")] if output_dir.exists() else []
    if process.returncode != 0:
        return {
            "status": "failed",
            "returncode": process.returncode,
            "error": process.stderr[-2000:],
        }
    return {
        "status": "completed",
        "videos": videos,
        "log": process.stdout[-1000:],
    }
