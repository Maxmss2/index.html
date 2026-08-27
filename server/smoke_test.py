"""Teste básico sem serviços externos para validar o núcleo da VÍDEOCREATOR."""
import sys
from pathlib import Path

# Permite executar diretamente a partir da raiz do repositório.
SERVER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVER_DIR))

from engines import build_job_payload, engine_status
from main import health, architecture


def main() -> None:
    status = health()
    assert status["status"] == "online"
    assert "VÍDEOCREATOR" in status["engine"]

    pipeline = architecture()["pipeline"]
    assert "render" in pipeline
    assert "publish" in pipeline

    payload = build_job_payload("teste-123", "Crie um vídeo curto sobre tecnologia.")
    assert len(payload) == 1
    assert payload[0]["orientation"] == "portrait"
    assert payload[0]["language"] == "portuguese"

    engine = engine_status()
    assert engine["id"] == "automated-video-generator"
    assert "render" in engine["capabilities"]

    print("OK - Núcleo da VÍDEOCREATOR passou no teste básico.")


if __name__ == "__main__":
    main()
