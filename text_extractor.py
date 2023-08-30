from pdf2image import convert_from_path
import pytesseract
import textract
import openpyxl
import csv
import datetime
import re


class TextExtractor:
    @staticmethod
    def extract_text_from_pdf(filepath):
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        doc = convert_from_path(filepath)
        text = ''
        for page_data in doc:
            text += pytesseract.image_to_string(page_data).encode('utf-8').decode('utf-8')
        return text

    
    @staticmethod
    def extract_text_from_xlsx(filepath):
        wb = openpyxl.load_workbook(filepath)
        sheet = wb.active

        extracted_text = ""
        
        for row in sheet.iter_rows(values_only=True):
            row_text = ""
            for cell_value in row:
                if cell_value is not None:
                    formatted_cell_value= TextExtractor.format_cell(cell_value)
                    row_text += formatted_cell_value + "\t"
                else:
                    row_text += "\t"
            extracted_text += row_text.strip()+ "\n"
        return extracted_text
        
    
    @staticmethod
    def format_cell(cell_value):
        if isinstance(cell_value, datetime.datetime):
            # Verifica se a célula possui data e hora completa (com hora, minuto, segundo)
            if cell_value.hour != 0 or cell_value.minute != 0 or cell_value.second != 0:
                return cell_value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return cell_value.strftime('%Y-%m-%d')
        
        # Filtra caracteres alfanuméricos e acentuações usando expressão regular 
        filtered_text = re.sub(r'[^a-zA-Z0-9áéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ\s]', '', str(cell_value))
        return filtered_text
    


    @staticmethod
    def extract_text_from_csv(filepath):
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            extracted_text = ""
            for row in csv_reader:
                for cell in row:
                    extracted_text += cell + "\n"
 
        return extracted_text

    @staticmethod
    def extract_text_from_file(filepath, file_type):
        if file_type == 'pdf':
            return TextExtractor.extract_text_from_pdf(filepath)
        elif file_type == 'xlsx':
            return TextExtractor.extract_text_from_xlsx(filepath)
        elif file_type == 'csv':
            return TextExtractor.extract_text_from_csv(filepath)
        else:
            # Utilizar o textract para extrair texto de outros formatos (Word e texto)
            text = textract.process(filepath).decode('utf-8')
            return text