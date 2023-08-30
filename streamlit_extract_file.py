import streamlit as st
from text_extractor import TextExtractor
import os


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


    



if check_password():
   st.header("Welcome to Extract File :smile:")
   arquivo = st.file_uploader('Insira seu arquivo:', type=['csv', 'xlsx', 'pdf', 'txt', 'docx'])
    
   if arquivo is not None:
        with open(os.path.join("temp", arquivo.name), "wb") as f:
            f.write(arquivo.getbuffer())

        filename = os.path.join("temp", arquivo.name)
        file_type = arquivo.type.split('/')[-1]

        if file_type in ['csv', 'xlsx', 'pdf', 'txt', 'docx']:
            extracted_text = TextExtractor.extract_text_from_file(filename, file_type)

            st.header("O texto extraído foi:")
            st.code(extracted_text)

            os.remove(filename)
        else:
            st.error("Tipo de arquivo não suportado.")
            st.stop()







            
        st.header("O texto extraído foi:")
        st.code(extracted_text)
        
        os.remove(filename)