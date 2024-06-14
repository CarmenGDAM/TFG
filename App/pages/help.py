import streamlit as st
from faq import response



# Definir las respuestas preestablecidas del chatbot
responses = {
    "hola": "¡Hola! ¿Cómo puedo ayudarte?",
    "adios": "¡Adiós! Que tengas un buen día.",
    "¿cómo estás?": "Estoy bien, gracias por preguntar. ¿Y tú?",
    "¿qué puedes hacer?": "Puedo responder preguntas básicas y ayudarte con información predefinida.",
    "para que sirve esta aplicacion?": "Esta aplicación es un chatbot que te resuelve dudas sobre un tema en concreto.",
    "sobre que puedo preguntar?": "Puedo responder preguntas sobre un tema de programación, etc.",
    "sabes algun chiste?": "SI. Se abre el telón, aparece un informático y dice: ¡qué habéis tocado que no se cierra el telón!",
    "jajaja": "🤪 iba a ser humorista pero me quedé en Chatbot.",
    "que malo": "¿Que malo? ¡Pues no! La verdad es, que no hay malos en el mundo!!!"
}

# Función para obtener una respuesta del chatbot
def add_response(question):
    question = question.lower()
    return responses.get(question, "Lo siento, no entiendo esa pregunta.")

with st.sidebar:
    st.page_link("http://localhost:8000/docs", label="API", icon="👾")

#Toolbar de navegación
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link("app.py", label="Home", icon="🏠")

with col2:
    st.page_link("pages/help.py", label="Help", icon="💬", disabled=True)

with col3:
    st.page_link("pages/info.py", label="Info", icon="💡")

with col4:
    st.page_link("http://localhost:8000/docs", label="API", icon="👾")

with col5:
    st.page_link("http://www.google.com", label="Google", icon="🔍")


#Page title and header
st.header("En qué puedo ayudarte")


messages = st.container(height=300)
if prompt := st.chat_input("Escribe tu pregunta"):
    messages.chat_message("user").write(prompt)
    messages.chat_message("assistant").write(response(prompt))
