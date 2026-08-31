FROM ghcr.io/itspremkumar/automated-video-generator:latest

ENV HOST=0.0.0.0
ENV PORT=10000
ENV OPENVERSE_ENABLED=true
ENV TTS_PROVIDER=edge-tts

COPY worker/proxy.mjs /app/videocreator-proxy.mjs

EXPOSE 10000

CMD ["node", "/app/videocreator-proxy.mjs"]
