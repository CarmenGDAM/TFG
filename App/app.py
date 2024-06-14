import streamlit as st
from streamlit_modal import Modal
import tempfile
import nest_asyncio
import os
import logging
import sys
from typing import List, Optional
import fitz

nest_asyncio.apply()

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

from rag import RAG

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))



#Método para leer archivos PDF
def pdf_to_text(file):
    # Lee el contenido del archivo en memoria
    file_bytes = file.read()
    document = fitz.open(stream=file_bytes, filetype="pdf")    
    text = ""

    # Itera sobre cada página y extrae el texto
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    return text

with st.sidebar:
    st.page_link("http://localhost:8000/docs", label="API", icon="👾")


# Función para verificar si el archivo es PDF
def is_pdf(file):
    return file.name.lower().endswith('.pdf')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link("app.py", label="Home", icon="🏠", disabled=True)

with col2:
    st.page_link("pages/help.py", label="Help", icon="💬")

with col3:
    st.page_link("pages/info.py", label="Info", icon="💡")

with col4:
    st.page_link("http://localhost:8000/docs", label="API", icon="👾")

with col5:
    st.page_link("http://www.google.com", label="Google", icon="🔍")


st.title('DOCMAN')
st.markdown("Aplicación de gestión documental mediante IA (Document Management by AI), organiza y gestiona documentos eficientemente, proporcionando respuestas instantáneas a sus preguntas.")

# Inicializamos las variables
context_file=""
template = (
    "Eres un asistente virtual, que solo contestas con la información recibida en el contexto. Cualquier otra pregunta que no esté en el contexto ignoralá y responde:'No puedo ayudarte porque no tengo información sobre ese contexto.' \n"
    "A continuación se proporciona la información de contexto. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Usando sólamente esta información, sin aportar nueva información que no aparezca en el contexto, responde a la siguiente consulta: {query_str}\n"
)


#Page title and header
st.header("En qué puedo ayudarle")


# Crear un directorio temporal
temp_dir = tempfile.TemporaryDirectory()




uploaded_files = st.file_uploader("¿Desea subir un archivo?", accept_multiple_files=True, type="pdf", help = "Solamente admite archivos PDF.")

for uploaded_file in uploaded_files:
    if is_pdf(uploaded_file):

        # Guardar el archivo en el directorio temporal
        file_path = os.path.join(temp_dir.name, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convertir el archivo PDF a texto
        data = pdf_to_text(uploaded_file)
        context_file += data + "\n"
        #st.write("filename:", uploaded_file.name)

    else:
        st.warning("Por favor, cargue un archivo PDF.")

#st.write("", context_file)


english = st.toggle("Inglés", value=False, help="Traduce las respuestas al inglés")


if english:
    template = ("""
        You are a virtual assistant. You only respond with the information provided in the context. 
        Any other questions outside of the context should be ignored, and you should reply with: 
        'I can't help you because I don't have information on that context.' \n"
        The following context information is provided.
        \n---------------------\n"
        {context_str}
        \n---------------------\n
        Using only this information, without adding any new information that is not present in the context, 
        respond to the following query in English: {query_str}
    """)

#Instanciamos el RAG con el template
myRag = RAG(template)


response_file = "Además ten en cuenta la siguiente información, en caso de estar vacío, ignóralo:"+context_file



#Chatbot
messages = st.container()
prompt = st.chat_input("Qué deseas saber", max_chars=300)
if prompt:
    query = response_file + prompt
    response_vector = myRag.query(query)
    messages.chat_message("user").write(prompt)
    messages.chat_message("assistant").write(response_vector.response)
    response_file = response_vector.response

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button("Guardar respuesta", response_file, "Respuesta.txt", type = "primary", help="Descarga la respuesta en un fichero")

with col2:

    on_file_persist = st.button("Guardar fichero", type = "primary", help = "Guarda la información del fichero en al base de datos para que se tenga en cuenta en las proximas consultas.")
     
    if on_file_persist:

        if context_file != "":
            myRag.addDocuments(temp_dir)

            st.success("Los documentos se han guardado correctamente en la base de datos vectorial.")
        else:
            st.warning("No hay ningun archivo cargado.")

modal = Modal(key="window clear",title="Borrar")

with col3:
    #st.button("Borrar")
    if st.button("Borrar",  type = "primary", help="Borra la consulta y los documentos cargados.") :
       
        with modal.container():
            st.markdown('Desea borrar la consulta y los documentos cargados?')
            col1,col2 = st.columns(2)
            with col1:
                if st.button("Si"):
                    st.info("Se ha borrado la consulta y los documentos cargados.")
                    response_file =""
                    uploaded_files.clear()
                    temp_dir.cleanup()
                    context_file = ""
                    st.experimental_rerun()
            with col2:
                if st.button("No"):
                    modal.close()
            
                    