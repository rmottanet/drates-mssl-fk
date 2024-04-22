import os
import unittest
from unittest.mock import patch, MagicMock
from api.index import app
from api.service.redis_client import RedisClient

# Definir variáveis de ambiente para os testes
os.environ['REDIS_HOST'] = 'localhost'
os.environ['REDIS_PORT'] = '6379'
os.environ['REDIS_KEY'] = 'password'
os.environ['COINSNARK_TOKEN'] = 'correct_token'

class TestIndex(unittest.TestCase):
    @patch('api.index.RedisClient')
    def test_get_exrates_success(self, mock_redis_client):
        # Criar um mock para o RedisClient
        mock_redis_instance = MagicMock()
        # Simular dados retornados em bytes
        mock_redis_instance.get_exrates.return_value = {b'USD': b'1.234', b'EUR': b'2.345'}
        mock_redis_client.return_value = mock_redis_instance
    
        # Fazer uma solicitação GET para a rota /exrates com token correto
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer correct_token'}
            response = client.get('/exrates', headers=headers)
    
        # Verificar se a resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)
    
        # Verificar se os dados retornados correspondem aos dados simulados
        expected_data = {'USD': '1.234', 'EUR': '2.345'}
        self.assertEqual(response.json, expected_data)
    
    @patch('api.index.RedisClient')
    def test_get_exrates_unauthorized(self, mock_redis_client):
        # Criar um mock para o RedisClient
        mock_redis_instance = MagicMock()
        # Simular dados retornados em bytes
        mock_redis_instance.get_exrates.return_value = {b'USD': b'1.234', b'EUR': b'2.345'}
        mock_redis_client.return_value = mock_redis_instance
    
        # Fazer uma solicitação GET para a rota /exrates sem token
        with app.test_client() as client:
            response = client.get('/exrates')
    
        # Verificar se a resposta é 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)
    
    @patch('api.index.RedisClient')
    def test_get_exrates_invalid_token(self, mock_redis_client):
        # Criar um mock para o RedisClient
        mock_redis_instance = MagicMock()
        # Simular dados retornados em bytes
        mock_redis_instance.get_exrates.return_value = {b'USD': b'1.234', b'EUR': b'2.345'}
        mock_redis_client.return_value = mock_redis_instance
    
        # Fazer uma solicitação GET para a rota /exrates com token incorreto
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer invalid_token'}
            response = client.get('/exrates', headers=headers)
    
        # Verificar se a resposta é 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)
    
    @patch('api.index.RedisClient')
    def test_exrates_no_data(self, mock_redis_client):
        # Criar um mock para o RedisClient
        mock_redis_instance = MagicMock()
        # Simular dados retornados em bytes
        mock_redis_instance.get_exrates.return_value = None
        mock_redis_client.return_value = mock_redis_instance
    
        # Fazer uma solicitação GET para a rota /exrates com token correto
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer correct_token'}
            response = client.get('/exrates', headers=headers)
    
        # Verificar se a resposta é 404 (Not Found)
        self.assertEqual(response.status_code, 404)
    
        # Verificar se a mensagem de erro está correta
        expected_error = {'error': 'Data not found'}
        self.assertEqual(response.json, expected_error)
    

if __name__ == '__main__':
    unittest.main()
