# Introdução
# API de Processamento de Arquivos

Esta API foi desenvolvida utilizando Flask e Flask-RestX para realizar operações de upload, extração de texto e processamento de arquivos. A API permite enviar arquivos em diversos formatos, como txt, pdf, csv, xlsx e docx, e realizar as seguintes operações:

- **Validação de Tipo de Arquivo**: Verifica se o arquivo enviado está em um formato permitido.
- **Extração de Texto**: Extrai o texto de um arquivo enviado.
- **Processamento de Arquivo**: Extrai o texto de um arquivo enviado e o envia para um servidor MockAPI para processamento e classificação do texto através da funcionalidade NER, onde através categorias pré-definidas, identifica locais, nomes, datas, organizações. Devolve uma lista com as entities identificadas.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados:

- Python 3.x
- Flask
- Flask-RestX
- Werkzeug
- textract
- requests
- spacy
- pytesseract
- pdf2image
- openpyxl


## Como executar a API

1. Clone este repositório em sua máquina local:

Clone o repositório em sua máquina local
§ git clone https://LRedGlue-Production@dev.azure.com/LRedGlue-Production/Datasense-eDoc%20REST%20API/_git/Datasense-eDoc%20REST%20API

2.	Software dependencies

$ pipenv install -r requirements.txt

3. Execução 

§ python ds_backend_fserver.py 
§ python mock_api.py

A API estará disponível em ´http://localhost:5000' e o servidor mock em 'http://localhost:5001' 

## Endpoints da API
A API possui os seguintes endpoints:

POST /validate-filetype: Realiza a validação do tipo de arquivo enviado e verifica através do métodos allowed_file se o ficheiro está entre os formatos aceites pela API.
POST /extract-text: Extrai o texto de um arquivo enviado.
POST /process-file: Extrai o texto de um arquivo enviado e envia para o servidor MockAPI, e retorna o texto extraído e um dicionário com o texto classificado em labels pela funcionalidade NER.
Consulte a documentação da API para obter mais detalhes sobre os parâmetros esperados e as respostas retornadas em cada endpoint.

## Documentação da API
Foi desenvolvida uma documentação através do Swaggwe UI e pode ser acedida em http://localhost:5000 

## MockAPI
Este projeto também inclui um servidor MockAPI que é utilizado para processar o texto extraído dos arquivos enviados. O servidor MockAPI está configurado para ser executado na porta 5001.

Certifique-se de executar o servidor MockAPI antes de utilizar o endpoint /process-file da API principal.

## Contribuição
Contribuições são bem-vindas! Se você encontrar algum problema, tiver alguma sugestão ou quiser adicionar algum recurso, sinta-se à vontade para criar um problema ou enviar uma solicitação pull.