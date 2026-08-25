from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI(title='VIDEO CREATOR Engine')

class Command(BaseModel):
    command: str
    limit: int = 5

FACTS = [
    'Uma estrela de nêutrons possui uma densidade extraordinária.',
    'Em Vênus, um dia pode durar mais do que um ano.',
    'O Sol concentra aproximadamente 99,8% da massa do Sistema Solar.',
    'O espaço não transmite som como a atmosfera terrestre.',
    'Existem bilhões de galáxias no universo observável.'
]

@app.get('/health')
def health():
    return {'status': 'online', 'engine': 'videocreator', 'date': str(date.today())}

@app.post('/jobs')
def create_job(data: Command):
    amount = max(1, min(data.limit, 5))
    videos = []
    for i in range(amount):
        fact = FACTS[i % len(FACTS)]
        videos.append({
            'id': i + 1,
            'title': f'Curiosidade #{i+1}',
            'fact': fact,
            'script': f'Você sabia? {fact} Essa é uma curiosidade incrível. Para mais curiosidades, acompanhe o canal!',
            'status': 'script_ready'
        })
    return {'status': 'planned', 'command': data.command, 'videos': videos}
