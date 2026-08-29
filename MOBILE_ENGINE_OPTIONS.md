# VÍDEOCREATOR — Estratégia Mobile-First: Motores de Vídeo

## Decisão atual
A VÍDEOCREATOR será uma central mobile-first. O usuário controla a criação pelo celular e o processamento poderá acontecer:

1. Remotamente em um motor de vídeo hospedado; ou
2. Diretamente no dispositivo quando o tipo de vídeo permitir.

## Motor 1 — Automated Video Generator
**Papel:** pipeline completo de texto para vídeo.

Pontos fortes:
- roteiro/texto para vídeo;
- voz, mídia, legendas e MP4;
- API/portal e execução em container;
- adequado para processamento remoto.

Uso na VÍDEOCREATOR: motor principal para geração automatizada.

## Motor 2 — LeClap (candidato em avaliação)
**Papel:** composição e edição determinística.

Pontos fortes:
- renderização no navegador via WebAssembly;
- possibilidade de renderização no dispositivo com React Native;
- templates JSON reutilizáveis;
- útil para vinhetas, legendas, transições, barras de progresso e edição.

Uso potencial na VÍDEOCREATOR: editor/compositor complementar, não substituto do motor principal nesta fase.

## Arquitetura-alvo

Celular → VÍDEOCREATOR → Orquestrador
                         ├── Automated Video Generator → criação automatizada
                         └── LeClap (futuro) → composição/edição mobile

## Próximo marco para 60%
Criar um contrato único de "job" para que a interface móvel possa acompanhar estados como queued, processing, validated, completed e failed independentemente do motor escolhido.
