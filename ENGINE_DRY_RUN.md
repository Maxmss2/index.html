# VÍDEOCREATOR — Validação do Motor (Dry-Run)

Este documento registra o contrato de validação entre a VÍDEOCREATOR e o Automated Video Generator.

## Objetivo

Antes de renderizar um MP4, validar que um comando da VÍDEOCREATOR pode ser convertido em uma solicitação compreendida pelo motor externo.

## Comando de referência do motor

Depois de instalar o Automated Video Generator conforme a documentação oficial, execute no diretório dele:

```bash
npm run agentic -- --topic "Curiosidades sobre o espaço" --orientation portrait --dry-run
```

O modo `--dry-run` planeja o pipeline sem baixar mídia ou renderizar o vídeo.

## Contrato VÍDEOCREATOR → Motor

Entrada da VÍDEOCREATOR:
- comando em linguagem natural;
- orientação preferencial;
- idioma;
- identificador da tarefa.

Saída esperada do planejamento:
- título;
- cenas planejadas;
- orientação;
- decisões de mídia;
- texto/narração por cena.

## Próximo teste

Após a validação do dry-run, executar uma geração curta e confirmar a existência do MP4 no diretório de saída do motor.

> Segurança: nunca envie chaves de API ou senhas para o repositório.
