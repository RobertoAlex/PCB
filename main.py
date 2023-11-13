import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="ManoTech",
    page_icon="🤖",
    layout="wide"
)

# Función para la página de bienvenida
def pagina_bienvenida():
    # Crea 3 columnas
    left_col, mid_col, right_col = st.columns(3)

    # Muestra la imagen en la columna central
    mid_col.image("Uni.png", width=200)
    st.title("Visor de venas")
    st.write("Este proyecto busca demostrar el poder que se puede generar con un poco de conocimiento en programacion al igual que en electronica")
    st.header("Ayudame a llenar este pedo")
    st.write("Ayudame a llenar este pedo")
    st.write("Ayudame a llenar este pedo")
        # URL del video de YouTube
    video_url = "https://youtu.be/lvIDTmyw6RU?si=I0cxedUcPvUTHEkY"

    # Mostrar el video de YouTube en la interfaz
    st.video(video_url)
    st.header("Presiona los siguientes botones para obtener mas informacion al respecto")
    # Botón
    if st.button("1.- ¡Arriesgar la salud de los trabajadores!"):
        st.write("""En algunos trabajas en diversos campos como en desarrollo de cultivos celulares es muy importante la biosegurad de los trabajadores y es muy importantes para los patrones la seguridad de sus empleados por tal motivo es mejor que algunas maquinas hagan el trabajo de los hombres""")
    if st.button("2.- ¡Automatizacion de procesos que requieran alta precision!"):
        st.write("""Algunas maquinas necesitan un alto grado de presicion y que mejor que la computadora o la maquina pueda copiar exactamente el movimiento de una persona y se pueda programar correctamente el moviemnto a realizar para una optima ejecucio de la tarea o trabajo que este buscando desempeñar""")
    if st.button("3.- ¡Puede servir para mejorar las capacitaciones de los trabajadores "):
        st.write("""Mejorando los procesos podemos almacenar los objetivos conseguidos con rastreos de manos los cuales pueden servir para que los trabajadore tengan un mejor entendimiendo de que y como se debe hacer la actividad y en base a esto minimizar los riesgos y maximizar el exito en las actividades""")
    if st.button("4.- ¡Mejorar la calidad de vida de los trabajadores "):
        st.write("""Cuando cuidamos a los trabajadores y los ayudamos con mejores capacitaciones y mejores herramientas no solo mejorams la calidad de vida de los trabajadores si no que aumentamos su productividad lo cual en terminos economicos siempre resulta un beneficio economico para todos.""")
    if st.button("5.- ¡Optimizacion de Procesos mecanicos "):
        st.write("""Este proyecto tiene una gran ventaja el cual es la escalabilidad y automatizacion de proceso ya que una simple mano parece no ser una buena idea sin embargo el proceso de copiar y reproducir el moviemiento de 1 mano humana no solo tiene este potencial este trabajao se puede usar para 10 manos o 100 o 1000 al mismo tiempo lo cual podria disminuir los tiempos de algunas actividades""")

# Función para la página de información (Opción 2)
def Datos_del_proyecto():
    st.title("Información sobre la contruccion del proyecto Mano Tech")
    st.write("A continuacion podra Observar el diagrama esquematico del Proyecto al igual que algunos videos que muestran las fases de la contruccion de este muy bonito e interesante proyecto")
    st.title("Diagrama esquimatico")
    st.image("Esquematico.jpeg")
    st.title("Materiales para el circuito:")
    # Crear un DataFrame de pandas con un solo valor
    datos = {"Componente": ["Servomotores", "Cables Dupont", "Fuente de alimentación externa", "Arduino Uno", "Otro Componente"],
    "Cantidad": [5, 16, 1, 1, 10]}
    df = pd.DataFrame(datos)
    # Mostrar la tabla
    st.table(df)
    st.title("Diagrama de conecciones")
    st.write("A continuacion mostraremos el diagrama esquematico en forma de diagrama de Tinkercad mas sencillo de distinguir lo que serian las conecciones")
    st.image("Imagen3.png")

# Función para la página de contacto (Opción 3)
def pagina_contacto():
    st.title("Contáctenos")
    st.write("Si tienes preguntas o comentarios, no dudes en ponerte en contacto con nosotros.")

    # Crea 2 columnas
    Cuatro_col, Cinco_col= st.columns(2)

    with Cuatro_col:
        st.image("4.png", width=180)
        st.markdown("**Nombre:** Luis Mauricio")
        st.markdown("**Apellido:** Lopez Jaramillo")
        link = '<a href="https://www.linkedin.com/in/luis-mauricio-lopez-jaramillo-108b09290/" target="_blank">Linkedin</a>'
        st.markdown(link, unsafe_allow_html=True)

    with Cinco_col:
        st.image("5.png", width=180)
        st.markdown("**Nombre:** Sergio Arturo")
        st.markdown("**Apellido:** Meza Huerta")
        link = '<a href="https://www.linkedin.com/in/luis-mauricio-lopez-jaramillo-108b09290/" target="_blank">Linkedin</a>'
        st.markdown(link, unsafe_allow_html=True)

# Título del menú
st.sidebar.markdown("Bienvenido al Menu")

# Elementos del menú
opciones = ["Bienvenida", "Datos del proyecto", "Contacto"]
eleccion = st.sidebar.selectbox("Selecciona una opción:", opciones)

# Contenido de la página según la elección
if eleccion == "Bienvenida":
    pagina_bienvenida()
elif eleccion == "Datos del proyecto":
    Datos_del_proyecto()
elif eleccion == "Contacto":
    pagina_contacto()
