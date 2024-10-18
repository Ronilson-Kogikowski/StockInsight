from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detalhes', methods=['GET', 'POST'])
def detalhes():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            return redirect(url_for('detalhes_acao', ticker=ticker))
    return redirect(url_for('home'))

@app.route('/detalhes/<ticker>')
def detalhes_acao(ticker):
    acao = yf.Ticker(ticker)
    info = acao.info

    # Obtendo os detalhes da ação
    detalhes = {
        'nome_empresa': info.get('shortName', 'N/A'),
        'preco_inicio': None,
        'preco_fechamento': None,
        'preco_maximo': None,
        'preco_minimo': None,
        'volume': None,
    }

    # Obtendo o histórico para 1 dia
    historico_dia = acao.history(period='1d')
    
    # Verifica se há dados disponíveis
    if not historico_dia.empty:
        detalhes['preco_inicio'] = historico_dia['Open'][0]
        detalhes['preco_fechamento'] = historico_dia['Close'][0]
        detalhes['preco_maximo'] = historico_dia['High'][0]
        detalhes['preco_minimo'] = historico_dia['Low'][0]
        detalhes['volume'] = historico_dia['Volume'][0]
    else:
        detalhes['nome_empresa'] = 'N/A'
    
    return render_template('detalhes_acao.html', detalhes=detalhes, ticker=ticker)

@app.route('/historico/<ticker>')
def historico(ticker):
    acao = yf.Ticker(ticker)
    historico = acao.history(period='1y')

    if historico.empty:
        return render_template('historico_acao.html', grafico_html=None, ticker=ticker, erro='Não foram encontrados dados para o ticker fornecido.')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historico.index, y=historico['Close'], mode='lines', name='Preço de Fechamento'))
    
    # Ajuste o tamanho do gráfico aqui
    fig.update_layout(
        title=f'Histórico de Preços - {ticker}', 
        xaxis_title='Data', 
        yaxis_title='Preço de Fechamento (R$)',
        width=1200,  # Largura do gráfico
        height=600   # Altura do gráfico
    )

    grafico_html = fig.to_html(full_html=False)
    return render_template('historico_acao.html', grafico_html=grafico_html, ticker=ticker)

@app.route('/previsao/<ticker>')
def previsao(ticker):
    acao = yf.Ticker(ticker)
    historico = acao.history(period='1y')
    close_prices = historico['Close'].values

    if len(close_prices) == 0:
        return render_template('previsao_acao.html', previsoes=None, ticker=ticker, erro='Não há dados suficientes para realizar a previsão.')

    dias = np.arange(len(close_prices)).reshape(-1, 1)
    modelo = LinearRegression()
    modelo.fit(dias, close_prices)

    dias_futuros = np.arange(len(close_prices), len(close_prices) + 10).reshape(-1, 1)
    previsoes = modelo.predict(dias_futuros)

    datas_previsao = [datetime.today().date() + timedelta(days=i) for i in range(1, 11)]
    previsoes_dict = dict(zip(datas_previsao, previsoes))

    return render_template('previsao_acao.html', previsoes=previsoes_dict, ticker=ticker)

if __name__ == '__main__':
    app.run(debug=True)
