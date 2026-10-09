# Atualização: Integração Open-Meteo & Refatoração UI

## Novidades (Features)
- **Integração Real-time com Open-Meteo**: Agora a rampa consome a API da Open-Meteo para buscar a velocidade e rajada do vento (em km/h), além da cobertura de nuvens, em tempo real.
- **Auto-Refresh**: Os dados são atualizados automaticamente na tela a cada 10 segundos utilizando JavaScript nativo (Fetch API), eliminando a necessidade de atualizar a página do Django manualmente.
- **Validação Automática de Segurança**: A regra de negócios que decide se a rampa está 'Segura' ou 'Insegura' (baseada em ventos abaixo de 25 km/h e rajadas abaixo de 35 km/h) passou a rodar diretamente no cliente, proporcionando feedback instantâneo.

## Melhorias de Design & UI (Style)
- **Design Flat/Minimalista**: Remoção de efeitos pesados de sombreamento e de vidro fosco (glassmorphism), substituindo por fundos limpos e bordas coloridas indicativas do status de voo (Verde para Seguro, Laranja para Atenção, Vermelho para Risco).
- **Tipografia Moderna**: Importação da fonte `Roboto` do Google Fonts para aprimorar a legibilidade.
- **Grid Responsivo para os Dados de Leitura**: Os dados de clima (temperatura, vento, nuvens) agora estão organizados em pequenos cartões ("cards") dentro de um flex-grid, o que melhora consideravelmente a leitura em dispositivos móveis.

## Refatorações (Refactor)
- **Arquitetura Atômica**: Os templates gigantescos do Django foram fragmentados em componentes menores para facilitar a manutenção futura:
  - `inicio.html`: Serve como o template de página principal ("Page").
  - `card_situacao.html`: Atua como o componente ("Organismo") que exibe a cor e o status principal.
  - `dados_leitura.html`: Atua como o componente agrupado ("Molécula") contendo as leituras numéricas do momento.
- **Código Limpo no JavaScript**: O código do script `monitor_clima.js` foi reescrito usando `async / await` e um objeto literal de `CONFIG` no topo para constantes matemáticas, garantindo que o DOM não precise ser consultado (`getElementById`) repetidas vezes dentro do loop.

## Infraestrutura (Chore)
- **Modo DEBUG**: A chave `DEBUG` foi definida como `True` em `settings.py` para garantir que o Django sirva os arquivos estáticos de maneira correta no ambiente de desenvolvimento local.
