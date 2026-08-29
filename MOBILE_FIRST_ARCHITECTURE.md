# VÍDEOCREATOR — Arquitetura Mobile-First

## Decisão do projeto
A VÍDEOCREATOR será pensada para ser usada principalmente pelo celular. O telefone será o painel de comando e acompanhamento; a geração pesada de vídeo poderá acontecer em um backend remoto quando necessário.

## Fluxo desejado

Celular → API da VÍDEOCREATOR → Fila de tarefas → Motor de vídeo → Armazenamento do resultado → Celular

O usuário digita ou fala um comando, acompanha uma barra de progresso e recebe o vídeo final para visualizar e publicar.

## Por que não depender de instalação no celular
A renderização de vídeos, modelos de IA e ferramentas como FFmpeg podem exigir bastante processamento e armazenamento. Separar o aplicativo móvel do motor permite usar o celular como interface sem exigir um computador pessoal ligado para cada operação.

## Próximos marcos

1. Tornar a interface atual acessível pelo navegador do celular.
2. Criar um contrato de API independente do motor de vídeo.
3. Preparar execução remota do motor escolhido.
4. Exibir status real da tarefa e progresso no celular.
5. Entregar um link/arquivo de vídeo quando a tarefa terminar.

## Regra Frankenstein
Antes de criar uma funcionalidade do zero, procurar soluções open-source compatíveis e reutilizáveis, respeitando as licenças dos projetos.

## Critério de sucesso
A primeira versão funcional estará comprovada quando um usuário puder iniciar uma tarefa pelo celular, acompanhar o status e receber um vídeo gerado pelo sistema.
