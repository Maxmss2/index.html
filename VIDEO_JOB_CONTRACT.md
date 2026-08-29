# VÍDEOCREATOR — Contrato Universal de Tarefas de Vídeo

## Objetivo

Definir uma linguagem única entre a interface mobile da VÍDEOCREATOR e qualquer motor de vídeo. O aplicativo não deve depender de um único fornecedor ou projeto open-source.

## Estados oficiais

1. `queued` — tarefa recebida e aguardando processamento.
2. `planning` — roteiro, cenas ou plano de produção sendo preparado.
3. `generating` — mídia, voz ou conteúdo sendo gerado.
4. `rendering` — composição e renderização do vídeo final.
5. `completed` — vídeo disponível.
6. `failed` — processamento interrompido com erro.

## Progresso

Todo motor integrado deve informar:

- `jobId`: identificador da tarefa;
- `status`: um dos estados oficiais;
- `progress`: número de 0 a 100;
- `message`: descrição simples da etapa atual;
- `resultUrl`: endereço do resultado quando concluído;
- `error`: mensagem segura quando houver falha.

## Regra Mobile-First

O celular é o painel de controle. Processamento pesado pode acontecer remotamente. A interface deve conseguir acompanhar o trabalho mesmo que o motor demore vários minutos.

## Adaptadores

Cada motor recebe um adaptador responsável por converter seus estados internos para este contrato. Assim podemos usar, testar ou substituir motores sem reconstruir a interface da VÍDEOCREATOR.

## Próximo marco

Conectar este contrato ao backend e à barra de progresso da interface, depois validar com um motor real hospedado remotamente.
