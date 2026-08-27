# Integrações Frankenstein

A VÍDEOCREATOR não pretende reinventar o motor de vídeo. Esta pasta registra adaptadores para projetos open-source avaliados.

## Primeiro motor candidato

**Automated Video Generator** — https://github.com/itsPremkumar/Automated-Video-Generator

Licença: MIT (confirmar e preservar avisos ao distribuir código derivado).

A estratégia inicial é integrar o projeto como um serviço/motor externo através de sua interface de geração, evitando copiar o repositório inteiro. Isso preserva a independência da API FastAPI da VÍDEOCREATOR e permite substituir componentes no futuro.

## Componentes candidatos

- Geração completa de vídeo: Automated Video Generator
- Legendas e composição avançada: OpenCut (MIT)
- Orquestração de múltiplos pipelines: OpenMontage, avaliado como referência e não como dependência obrigatória

## Regra do projeto

Antes de criar um componente novo, pesquisar soluções open-source maduras. Avaliar licença, manutenção, dependências, segurança e facilidade de integração antes de reutilizar código.