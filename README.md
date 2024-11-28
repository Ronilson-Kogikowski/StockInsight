Descrição do Projeto
StockInsight
Um sistema de análise financeira simples, desenvolvido com Flask, que permite visualizar detalhes, históricos e previsões de ações utilizando dados em tempo real da biblioteca yfinance.

Funcionalidades
Pesquisar informações básicas sobre ações (nome, preço atual, etc.).
Exibir detalhes da ação, como preço de abertura, fechamento, máximo, mínimo e volume diário.
Visualizar o histórico de preços de fechamento em um gráfico interativo.
Gerar previsões de preços para os próximos 10 dias com o modelo ARIMA.
Tecnologias Utilizadas
Flask: Para criação do backend e gerenciamento de rotas.
yfinance: Para busca de dados financeiros em tempo real.
ARIMA: Para previsão de preços com base em séries temporais.
Plotly: Para renderização de gráficos interativos.
HTML e CSS: Para construção de uma interface amigável.
Como Executar o Projeto
Clone este repositório:
bash
Copiar código
git clone https://github.com/SEU_USUARIO/StockInsight.git
cd StockInsight
Crie um ambiente virtual e instale as dependências:
bash
Copiar código
python -m venv venv
source venv/bin/activate  # (ou venv\Scripts\activate no Windows)
pip install -r requirements.txt
Inicie o servidor Flask:
bash
Copiar código
python app.py
Acesse o projeto em http://127.0.0.1:5000.
