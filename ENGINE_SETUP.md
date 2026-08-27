# VÍDEOCREATOR — Motor de vídeo open-source

A primeira integração real da estratégia Frankenstein usa o projeto **Automated Video Generator**, sob licença MIT, como motor externo de geração.

## Como a integração funciona

A VÍDEOCREATOR continua sendo o painel e o orquestrador. O motor externo faz o trabalho pesado:

`Comando → VÍDEOCREATOR → Automated Video Generator → MP4`

O adaptador está em `server/engines.py`. Para ativá-lo, o servidor precisa receber o caminho local onde o motor foi instalado através da variável:

`AUTOMATED_VIDEO_GENERATOR_PATH`

## Instalação do motor

Consulte sempre as instruções atuais do projeto original:
https://github.com/itsPremkumar/Automated-Video-Generator

Após instalar o motor, configure a variável `AUTOMATED_VIDEO_GENERATOR_PATH` apontando para a pasta do repositório. A VÍDEOCREATOR poderá então verificar o motor em `/engines` e iniciar tarefas com `POST /jobs/{job_id}/run`.

## Segurança

Chaves de APIs e contas de redes sociais não devem ser salvas no código ou enviadas para o repositório. Elas serão configuradas somente no ambiente de execução.

## Próximo marco

Executar um teste real de ponta a ponta e confirmar a geração do primeiro MP4 pela VÍDEOCREATOR.
