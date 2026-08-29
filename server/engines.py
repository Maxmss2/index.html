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

ENGINE_ROOT_RAW = os.getenv("AUTOMATED_VIDEO_GENERATOR_PATH", "").strip()
ENGINE_ROOT = Path(ENGINE_ROOT_RAW).expanduser() if ENGINE_ROOT_RAW else None


def engine_status() -> dict[str, Any]:
    configured = ENGINE_ROOT is not None and ENGINE_ROOT.exists()
    package_file = ENGINE_ROOT / "package.json" if configured and ENGINE_ROOT else None
    return {
        "id": "automated-video-generator",
        "name": "Automated Video Generator",
        "configured": configured,
        "path": str(ENGINE_ROOT) if configured else None,
        "package_detected": bool(package_file and package_file.exists()),
        "capabilities": ["voice", "media", "captions", "render", "dry_run"],
        "setup_required": not configured,
    }


def build_job_payload(job_id: str, command: str, dry_run: bool = False) -> list[dict[str, Any]]:
    """Converte o comando da VÍDEOCREATOR no formato oficial do motor externo."""
    return [{
        "id": job_id,
        "title": f"VÍDEOCREATOR {job_id[:8]}",
        "orientation": "portrait",
        "language": "portuguese",
        "script": command,
        "dryRun": dry_run,
    }]


def run_video_engine(job_id: str, command: str, dry_run: bool = False) -> dict[str, Any]:
    """Executa o pipeline oficial do motor instalado localmente.

    O modo dry-run é repassado no JSON oficial do motor e permite validar o
    pipeline sem renderizar o MP4. Não usa shell=True para evitar injeção de
    comandos.
    """
    status = engine_status()
    if not status["configured"] or ENGINE_ROOT is None:
        return {
            "status": "needs_setup",
            "message": "Motor de vídeo ainda não instalado neste computador/servidor.",
        }
    if not status["package_detected"]:
        return {
            "status": "failed",
            "message": "A pasta configurada não parece conter o Automated Video Generator (package.json ausente).",
        }

    input_dir = ENGINE_ROOT / "input" / "scripts"
    input_file = input_dir / "input-scripts.json"
    input_dir.mkdir(parents=True, exist_ok=True)
    input_file.write_text(
        json.dumps(build_job_payload(job_id, command, dry_run=dry_run), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    try:
        process = subprocess.run(
            ["npm", "run", "generate"],
            cwd=ENGINE_ROOT,
            capture_output=True,
            text=True,
            timeout=int(os.getenv("VIDEO_ENGINE_TIMEOUT", "3600")),
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "failed", "message": "Tempo limite do motor de vídeo excedido."}
    except FileNotFoundError:
        return {"status": "failed", "message": "Node.js/npm não está disponível no ambiente de execução."}

    if process.returncode != 0:
        return {
            "status": "failed",
            "returncode": process.returncode,
            "error": process.stderr[-2000:],
        }

    if dry_run:
        return {
            "status": "validated",
            "dry_run": True,
            "message": "Pipeline validado sem renderização final.",
            "log": process.stdout[-1000:],
        }

    output_dir = ENGINE_ROOT / "output" / job_id
    videos = [str(path) for path in output_dir.rglob("*.mp4")] if output_dir.exists() else []
    return {
        "status": "completed" if videos else "completed_no_video_found",
        "videos": videos,
        "log": process.stdout[-1000:],
    }
