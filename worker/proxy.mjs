import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { randomUUID } from 'node:crypto';

const PUBLIC_PORT = Number(process.env.PORT || 10000);
const UPSTREAM_PORT = 10001;
const ROOT = '/app';
const INPUT = path.join(ROOT, 'input', 'scripts', 'input-scripts.json');
const OUTPUT = path.join(ROOT, 'output');
const jobs = new Map();

function json(res, code, body) {
  const data = JSON.stringify(body);
  res.writeHead(code, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(data), 'access-control-allow-origin': '*' });
  res.end(data);
}

async function body(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

function findMp4(dir) {
  if (!fs.existsSync(dir)) return null;
  const stack = [dir];
  while (stack.length) {
    const current = stack.pop();
    for (const name of fs.readdirSync(current)) {
      const full = path.join(current, name);
      const stat = fs.statSync(full);
      if (stat.isDirectory()) stack.push(full);
      else if (name.toLowerCase().endsWith('.mp4')) return full;
    }
  }
  return null;
}

function startGeneration(job) {
  fs.mkdirSync(path.dirname(INPUT), { recursive: true });
  const payload = [{
    id: job.id,
    title: job.title,
    script: job.script,
    orientation: job.orientation,
    language: job.language,
    voice: job.voice,
    showText: true,
  }];
  fs.writeFileSync(INPUT, JSON.stringify(payload, null, 2));
  job.status = 'processing';
  job.message = 'Gerando narração, mídia, legendas e vídeo...';
  const child = spawn('npm', ['run', 'generate'], { cwd: ROOT, env: process.env, stdio: ['ignore', 'pipe', 'pipe'] });
  job.pid = child.pid;
  child.stdout.on('data', d => { job.log = (job.log || '') + d.toString().slice(-4000); });
  child.stderr.on('data', d => { job.errorLog = (job.errorLog || '') + d.toString().slice(-4000); });
  child.on('close', code => {
    const file = findMp4(path.join(OUTPUT, job.id));
    if (code === 0 && file) {
      job.status = 'completed';
      job.videoUrl = `/api/jobs/${job.id}/video`;
      job.output = file;
      job.message = 'Vídeo concluído.';
    } else {
      job.status = 'failed';
      job.message = code === 0 ? 'O motor terminou sem localizar o MP4.' : `Motor terminou com código ${code}.`;
    }
  });
}

function api(req, res) {
  if (req.method === 'GET' && req.url === '/api/health') return json(res, 200, { status: 'online', engine: 'Automated Video Generator', mode: 'remote-worker', no_api_key_tts: true });
  if (req.method === 'POST' && req.url === '/api/jobs') {
    return body(req).then(data => {
      if (!data.title || !data.script || data.script.length < 10) return json(res, 400, { error: 'title e script são obrigatórios; script mínimo de 10 caracteres.' });
      const id = randomUUID();
      const job = { id, title: String(data.title).slice(0, 180), script: String(data.script).slice(0, 5000), orientation: data.orientation === 'landscape' ? 'landscape' : 'portrait', language: data.language || 'portuguese', voice: data.voice, status: 'queued', message: 'Tarefa recebida.' };
      jobs.set(id, job);
      startGeneration(job);
      return json(res, 202, { success: true, data: { jobId: id, title: job.title, status: 'processing', statusUrl: `/api/jobs/${id}` } });
    }).catch(() => json(res, 400, { error: 'JSON inválido.' }));
  }
  const match = req.url?.match(/^\/api\/jobs\/([^/]+)(?:\/(video))?$/);
  if (match) {
    const job = jobs.get(match[1]);
    if (!job) return json(res, 404, { error: 'Job não encontrado neste Worker.' });
    if (match[2] === 'video') {
      if (!job.output || !fs.existsSync(job.output)) return json(res, 404, { error: 'Vídeo ainda não disponível.' });
      res.writeHead(200, { 'content-type': 'video/mp4', 'access-control-allow-origin': '*', 'content-length': fs.statSync(job.output).size });
      return fs.createReadStream(job.output).pipe(res);
    }
    return json(res, 200, { success: true, data: job });
  }
  return null;
}

const upstream = spawn('npm', ['run', 'dev', '--', '--host', '127.0.0.1', '--port', String(UPSTREAM_PORT)], { cwd: ROOT, env: process.env, stdio: 'inherit' });
upstream.on('exit', code => console.error(`upstream exited: ${code}`));

const server = http.createServer(async (req, res) => {
  if (req.url?.startsWith('/api/')) {
    const handled = api(req, res);
    if (handled) return;
    return;
  }
  try {
    const target = `http://127.0.0.1:${UPSTREAM_PORT}${req.url}`;
    const init = { method: req.method, headers: req.headers };
    if (!['GET', 'HEAD'].includes(req.method)) init.body = req;
    const response = await fetch(target, init);
    res.writeHead(response.status, Object.fromEntries(response.headers));
    if (response.body) response.body.pipeTo(new WritableStream({ write(chunk) { res.write(Buffer.from(chunk)); }, close() { res.end(); } })).catch(() => res.end());
    else res.end();
  } catch (e) { json(res, 502, { error: 'Upstream indisponível', detail: String(e) }); }
});

server.listen(PUBLIC_PORT, '0.0.0.0', () => console.log(`VÍDEOCREATOR worker API listening on 0.0.0.0:${PUBLIC_PORT}`));
