import streamlit as st
import re



def is_valid_email(email):
    # Define la expresión regular para un correo electrónico
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Utiliza la función match para verificar si el correo cumple con el patrón
    if re.match(email_regex, email):
        return True
    else:
        return False

with st.sidebar:
    st.page_link("http://localhost:8000/docs", label="API", icon="👾")



tab1, tab2, tab3 = st.tabs(["Información", "Soporte", "Sugerencias"])

with tab1:
    st.header("Docman")
    st.markdown("""
                Bienvenido a **DocMan**, una solución avanzada para la gestión de documentos basada en inteligencia artificial generativa. 
                DocMan está diseñado para facilitar la organización, búsqueda y análisis de grandes volúmenes de documentos PDF de manera 
                eficiente y precisa.
            """)
    
    st.header("¿Qué es DocMan?")
    st.markdown("""
                Descubre cómo DocMan puede transformar la manera en que gestionas y utilizas tus documentos. Simplifica la búsqueda de información y mejora tu productividad con nuestra 
                solución inteligente de gestión documental. DocMan permite a los usuarios cargar sus documentos PDF, realizar consultas mediante un chat interactivo y obtener respuestas 
                precisas basadas en la información contenida en esos documentos. Así como hacer consultas sobre la información almacenada en la base de datos.
                """)

    st.header("Beneficios de Usar DocMan")
    st.markdown("""
                1. **Sube tus archivos**: Puedes subir archivos PDF que quieras organizar y gestionar.
                2. **Procesamiento de archivos**: El sistema procesará los archivos subidos para extraer su contenido.
                3. **Almacenamiento**: Los documentos se almacenarán en una base de datos vectorial para futuras búsquedas.
                4. **Consulta**: Puedes hacer preguntas sobre los documentos almacenados y recibir respuestas instantáneas.
                5. **Guardar y eliminar**: Tienes opciones para guardar respuestas o eliminar archivos cargados.
                """)

    st.image("https://img.freepik.com/vector-premium/informacion-centro-datos-estilo-dibujos-animados-sistema-base-datos-vectorial-isometrica_100456-9243.jpg?w=900", width=500)
  

with tab2:
    st.header('Incidencia')
    st.markdown('Nos gustaría saber que problema ha sucedido')

    user = st.text_input('Usuario:')
    user_email = st.text_input('Correo electrónico:')
    type = st.selectbox(
        'Tipo de incidencia',
        ('Software', 'Hardware', 'Atencion al cliente', 'Otros'), help="Software: Carga de Datos, Hardware: Falta de memoria, Atención al cliente: Problemas usuarios, Otros: Cuestiones generales.")
    
    incidence = st.text_area('Escribe tu incidencia aquí:')

    
    if st.button('Enviar', type = "primary"):
        if user and user_email and type and incidence:
            if is_valid_email(user_email):
                try:
                    #send_email(subject, body, to)
                    st.success('Disculpa las molestias. En breve nos pondremos en contacto contigo.')
                except Exception as e:
                    st.error('Hubo un error al enviar tu incidencia. Inténtalo de nuevo más tarde.')
            else:
                st.error('Por favor, introduce un correo electrónico valido.')
        else:
            st.error('Por favor, completa todos los campos.')


with tab3:
   
    st.header('Sugerencias')
    st.markdown('Nos gustaría conocer tu opinión')

    name = st.text_input('Usuario')
    email = st.text_input('Email')
    suggestion = st.text_area('Escribe tu sugerencia aquí:')

    on_submit = st.toggle("Deseo suscribirme a la versión Premium")

    if on_submit:
        if is_valid_email(email):
            st.success('Gracias por suscribirse! Recibirá un correo electrónico con las intrucciones que debe seguir.')
        else:
            st.warning('Por favor, Introduzca su correo electrónico.')


    if st.button('Comentar', type = "primary"):
        if name and email and suggestion:
            if is_valid_email(email):
                try:
                    #send_email(subject, body, to)
                    st.success('¡Gracias por tu sugerencia!')
                    if on_submit:
                        st.balloons()
                        
                except Exception as e:
                    st.error('Hubo un error al enviar tu sugerencia. Inténtalo de nuevo más tarde.')
            else:
                st.error('Por favor, introduce un correo electrónico valido.')
        else:
            st.error('Por favor, completa todos los campos.')

        
