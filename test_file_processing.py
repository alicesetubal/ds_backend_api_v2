import unittest
import requests
import time

class APITestCase(unittest.TestCase):
    base_url = 'http://localhost:5000'
    mock_api_url = 'http://localhost:5001'
    
    def setUp(self):
        
        self.test_results = {}  # Variável para armazenar os resultados dos testes 
         
    def test_response_time(self):
        
        with open('path/file', 'rb') as file:
            start_time = time.time()
            response = requests.post(f"{self.base_url}/validate-filetype", files={'file_to_process': file})
            end_time = time.time()

        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)  # Verifica se o tempo de resposta é menor que 1 segundo
        self.test_results['response_time'] = end_time - start_time
    
    def test_upload_success_rate(self):
        with open('path/file', 'rb') as file:
            response = requests.post(f"{self.base_url}/validate-filetype", files={'file_to_process': file})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['message'], 'File successfully uploaded')
        self.test_results['upload_success_rate'] = 1 if response.status_code == 200 else 0
        
    def test_upload_failure(self):
        # Criar um arquivo vazio para simular um upload incorreto
        open('path/file', 'w').close()
        with open('path/file', 'rb') as file:
            response = requests.post(f"{self.base_url}/validate-filetype", files={'file_to_process': file})

        self.assertEqual(response.status_code, 400)
        self.test_results['upload_failure'] = 1 if response.status_code == 400 else 0
        
    def tearDown(self):
        test_name = self._testMethodName
        test_status = self._outcome.result
        
        self.test_results[test_name] = test_status
       
    
if __name__ == '__main__':
    #print("Resultados dos testes:")
    #print(APITestCase().test_results)
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(APITestCase)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Aqui você pode acessar os resultados dos testes
    test_results = test_result.test_results
    print("Resultados dos testes:")
    print(test_results)