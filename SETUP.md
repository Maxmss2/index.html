# Colocando o VÍDEOCREATOR em produção

## O que já funciona
O painel web pode ser aberto no navegador e permite testar comandos, fila diária e geração local de roteiros de demonstração.

## Para automação real
1. Criar um projeto de API do YouTube e configurar OAuth para a conta do canal.
2. Escolher provedores para IA e narração conforme disponibilidade e cotas.
3. Configurar fontes de mídia com licenças adequadas.
4. Executar o backend/orquestrador em computador ou servidor.
5. Configurar o agendador diário e limites reais.

## Regra de custos
O orquestrador deve consultar limites disponíveis e parar quando atingir a cota. Não deve tentar contornar limites, usar contas falsas ou burlar termos dos provedores.

## Publicação
A publicação deve usar autorização explícita do proprietário e APIs oficiais. Recomenda-se revisão humana antes das primeiras publicações e validação dos fatos e direitos sobre mídia.
