import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
# import subprocess
import requests
from flask_restx import Api, Resource, reqparse, abort
from werkzeug.datastructures import FileStorage
from text_extractor import TextExtractor



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'xlsx', 'docx'])

#Função para definir quais formatos de documentos são permitidos
def allowed_file(filename):
    file_allowed = ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return file_allowed

#Instaciar flask e flask_restx
app = Flask(__name__)
api = Api(app, version='1.0.0', title='API de Processamento de Arquivos', description='API para upload, extração de texto e processamento de arquivos.')
app.secret_key = "secret key"

#Define os campos esperados no parser
parser = reqparse.RequestParser()
parser.add_argument('file_to_process', type=FileStorage, location= 'files', required=False)

'''@app.route('/')
def index():
    response_data = {
        'message': 'Server is alive and kicking!',
    }
    return jsonify(response_data), 200'''
    
#Verifica se o upload do ficheiro foi efetuado corretamente
@api.route('/validate-filetype')
class CheckFile(Resource):
    @api.doc(parser=parser, description = 'Endpoint para realizar o upload de um arquivo.')
    @api.response(200, 'File successfully uploaded')
    @api.response(400, 'Validation Error')
    def post(self):
        # Verifica se o post tem um ficheiro
        if 'file_to_process' not in request.files:
            return {'message': 'No file in the request', 'file name': 'None', 'status_code': 400}, 400
        
        file = request.files['file_to_process']
    
        if file.filename == '':
            return {'message' : 'No file selected for uploading', 'file name': 'None', 'status_code ': 400}, 400
            
    
        if allowed_file(file.filename):
            filename = file.filename
            resp = jsonify({'message' : 'File successfully uploaded', 'file name': filename, 'status code': '200'})
            return resp
        else:
            return {'message' :'Allowed file types are txt, pdf, csv, xlsx, docx', 'file name': 'None', 'status code': 400}, 400

#Função para extrair o texto do ficheiro
@api.route('/extract-text')
class ExtractText(Resource):
    @api.doc(parser=parser, description= 'Endpoint para extrair o texto de um arquivo enviado.')
    @api.response(200, 'Text successfully extracted')
    @api.response(400, 'Validation Error')
    def post(self):
        if 'file_to_process' not in request.files:
        
            return {'message' : 'No file part in the request', 'file name': 'None', 'status_code': 400, 'Extracted text was': 'None'}, 400
        file = request.files['file_to_process']
        if file.filename == '':
            
            return {'message' : 'No file selected for uploading', 'file name': 'None', 'status code ': 400, 'Extracted text was': 'None'},400
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)

            # Determina o tipo de ficheiro com base na extensão
            file_type = filename.split('.')[-1].lower()

            # Utiliza o TextExtractor class to extract text from the file
            text_extractor = TextExtractor()
            text = text_extractor.extract_text_from_file(filename, file_type)

            os.remove(filename)
            response_data = {
                'message': 'Text successfully extracted',
                'text': text,
                'status code': 200
            }
            return jsonify(response_data) 
        
        else:
            return {'message' :'Allowed file types are txt, pdf, csv, xlsx, docx', 'file name': 'None', 'status code': '400'}, 400
    


@api.route('/process-file', methods=['POST', 'GET'])
class ProcessFile(Resource):
    @api.doc(parser=parser, description='Endpoint para processar o arquivo enviado, extrair o texto e enviar para o servidor MockAPI.')
    @api.response(200, 'Text successfully extracted')
    @api.response(400, 'Validation Error')
    def post(self):
        # Verifica se há arquivo na requisição
        if 'file_to_process' not in request.files:
            abort (400,message= 'No file part in the request')


        file = request.files['file_to_process']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            return resp

        if allowed_file(file.filename):
            # Salva o arquivo temporariamente
            filename = secure_filename(file.filename)
            file.save(filename)
            file_type = filename.split('.')[-1].lower()
            # Utiliza o TextExtractor para extrair o texto
        
            text_extractor= TextExtractor()
            extracted_text = text_extractor.extract_text_from_file(filename, file_type)
            os.remove(filename)
        
        
            # Enviar o texto para o servidor MockAPI
            data = {'extracted_text': extracted_text}
            #url = 'http://edoc-spacy-service.azurewebsites.net/ner'  # URL do mock criado para testar a comunicação entre REST Client.
            url = 'http://127.0.0.1:5001/ner'  # URL do mock criado para testar a comunicação entre REST Client.
            response = requests.post(url, json=data)

            if response.status_code == 200:
                classified_text = response.json()
                return jsonify(classified_text)
            else:
                return jsonify({'error': 'Error in the request to the other application'})
        else:
         abort(400, message='Allowed file types are txt, pdf, csv, xlsx, docx')
    

if __name__ == "__main__":
    # subprocess.Popen (["python", "mock_api.py"])
    print('Running api service...') 
    # app.run(debug=False, host="0.0.0.0")
    app.run(debug=True, host="0.0.0.0")

    