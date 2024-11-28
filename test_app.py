import unittest
from app import app

class TestHomePage(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Cria um cliente de teste
        cls.app.testing = True  # Habilita o modo de teste
    
    def test_home_post_empty_ticker(self):
        # Envia um POST para a página inicial com um ticker vazio
        response = self.app.post('/', data={'ticker': ''})
        
        # Verifica se a mensagem de erro está na resposta
        self.assertIn('Por favor, insira um ticker válido', response.data.decode('utf-8'))

    def test_home_post_invalid_ticker(self):
        # Envia um POST para a página inicial com um ticker inválido
        response = self.app.post('/', data={'ticker': 'INVALIDTICKER'})
        
        # Verifica se a mensagem de erro está na resposta, considerando a codificação HTML (&#39; para aspas simples)
        self.assertIn("Ação &#39;INVALIDTICKER&#39; não encontrada. Por favor, verifique o ticker e tente novamente.", response.get_data(as_text=True))

    def test_home_post_valid_ticker(self):
        # Envia um POST para a página inicial com um ticker válido
        response = self.app.post('/', data={'ticker': 'AAPL'})  # Ticker de exemplo para a Apple
        
        # Verifica se o redirecionamento para a página de detalhes foi feito
        self.assertEqual(response.status_code, 302)  # Redirecionamento HTTP

    def test_home_get(self):
        # Envia um GET para a página inicial
        response = self.app.get('/')
        
        # Verifica se o código de status da resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Verifica se o conteúdo da página contém o formulário de pesquisa de ticker
        self.assertIn('Digite o ticker da ação:', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
