# Arquitetura da VÍDEOCREATOR

A VÍDEOCREATOR é composta por uma interface simples e um motor de produção independente.

## Fluxo
1. Comando do usuário
2. Pesquisa e planejamento
3. Roteiro
4. Narração
5. Seleção de mídia licenciada ou fornecida pelo usuário
6. Legendas
7. Renderização
8. Revisão e publicação por integrações oficiais

## Princípios
- Nenhuma chave secreta é armazenada no frontend.
- Cada serviço externo é conectado por um adaptador configurável.
- O projeto não depende exclusivamente de um repositório open-source externo.
- Componentes de terceiros só serão reutilizados conforme suas licenças.

## Próxima implementação
Adicionar uma fila persistente e adaptadores para IA, voz, mídia e renderização local/servidor.
