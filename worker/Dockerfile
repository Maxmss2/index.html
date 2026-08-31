FROM ghcr.io/itspremkumar/automated-video-generator:latest

ENV HOST=0.0.0.0
ENV PORT=10000
ENV OPENVERSE_ENABLED=true
ENV TTS_PROVIDER=edge-tts

EXPOSE 10000

CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port 10000"]
