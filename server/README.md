# Backend do VÍDEOCREATOR

Esta pasta define a implantação do orquestrador real.

## Fluxo
Pesquisa -> validação de fatos -> roteiro -> narração -> mídia licenciada/original -> renderização -> revisão -> publicação via API oficial -> análise.

## Segurança
Chaves e tokens devem ficar em variáveis de ambiente ou em um gerenciador de segredos. Nunca devem ser enviados ao GitHub.

## Integrações
- YouTube Data API para publicação com OAuth do proprietário do canal.
- Fontes de pesquisa públicas e APIs com termos compatíveis.
- Provedores de voz e IA escolhidos pelo usuário.
- FFmpeg ou outro renderizador executado em servidor próprio.

O frontend atual funciona como painel e demonstração local. Para executar a automação real 24h/dia é necessário hospedar este backend em um computador ou servidor e configurar as credenciais das APIs.