from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    erro = None  # Inicializa a variável de erro como None
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if not ticker:  # Verifica se o ticker está vazio
            erro = 'Por favor, insira um ticker válido'  # Mensagem de erro se estiver vazio
        else:
            acao = yf.Ticker(ticker)
            try:
                historico = acao.history(period="1d")
                if historico.empty:
                    erro = f"Ação '{ticker}' não encontrada. Por favor, verifique o ticker e tente novamente."
                else:
                    return redirect(url_for('detalhes_acao', ticker=ticker))
            except Exception as e:
                erro = f"Ocorreu um erro ao buscar a ação '{ticker}': {str(e)}. Por favor, tente novamente."
    return render_template('home.html', erro=erro)

@app.route('/detalhes/<ticker>')
def detalhes_acao(ticker):
    acao = yf.Ticker(ticker)
    try:
        info = acao.info
        detalhes = {
            'nome_empresa': info.get('shortName', 'N/A'),
            'preco_inicio': None,
            'preco_fechamento': None,
            'preco_maximo': None,
            'preco_minimo': None,
            'volume': None,
        }
        historico_dia = acao.history(period='1d')
        if not historico_dia.empty:
            detalhes['preco_inicio'] = round(historico_dia['Open'].iloc[0], 2)
            detalhes['preco_fechamento'] = round(historico_dia['Close'].iloc[0], 2)
            detalhes['preco_maximo'] = round(historico_dia['High'].iloc[0], 2)
            detalhes['preco_minimo'] = round(historico_dia['Low'].iloc[0], 2)
            detalhes['volume'] = int(historico_dia['Volume'].iloc[0])
        else:
            detalhes['nome_empresa'] = 'N/A'
        return render_template('detalhes_acao.html', detalhes=detalhes, ticker=ticker)
    except Exception as e:
        erro = f"Erro ao buscar os detalhes da ação '{ticker}': {str(e)}."
        return render_template('detalhes_acao.html', erro=erro, ticker=ticker)

@app.route('/historico/<ticker>')
def historico(ticker):
    acao = yf.Ticker(ticker)
    try:
        historico = acao.history(period='1y')
        if historico.empty:
            return render_template('historico_acao.html', grafico_html=None, ticker=ticker, erro='Não foram encontrados dados.')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historico.index, y=historico['Close'], mode='lines', name='Preço de Fechamento'))
        fig.update_layout(
            title=f'Histórico de Preços - {ticker}', 
            xaxis_title='Data', 
            yaxis_title='Preço de Fechamento (R$)',
            width=1200, height=600, margin=dict(t=50, b=50, l=50, r=50)
        )
        grafico_html = fig.to_html(full_html=False)
        return render_template('historico_acao.html', grafico_html=grafico_html, ticker=ticker)
    except Exception as e:
        erro = f"Erro ao buscar o histórico da ação '{ticker}': {str(e)}."
        return render_template('historico_acao.html', grafico_html=None, ticker=ticker, erro=erro)

@app.route('/previsao/<ticker>')
def previsao(ticker):
    acao = yf.Ticker(ticker)
    try:
        historico = acao.history(period='1y')
        close_prices = historico['Close']
        
        if len(close_prices) < 2:
            return render_template('previsao_acao.html', previsoes=None, ticker=ticker, erro='Não há dados suficientes para previsão.')
        
        # Treinando o modelo ARIMA
        modelo = ARIMA(close_prices, order=(5, 1, 0))  # Ajuste de ordem (p,d,q)
        modelo_fit = modelo.fit()

        # Previsão para os próximos 10 dias
        previsoes = modelo_fit.forecast(steps=10)
        
        # Gerando as datas para previsão
        datas_previsao = [datetime.today().date() + timedelta(days=i) for i in range(1, 11)]
        previsoes_dict = dict(zip(datas_previsao, [round(p, 2) for p in previsoes]))
        
        return render_template('previsao_acao.html', previsoes=previsoes_dict, ticker=ticker)
    
    except Exception as e:
        erro = f"Erro ao buscar a previsão da ação '{ticker}': {str(e)}."
        return render_template('previsao_acao.html', previsoes=None, ticker=ticker, erro=erro)

if __name__ == '__main__':
    app.run(debug=True)
