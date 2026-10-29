import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#==================================
#    Función Moda
#==================================

def Mode(data):
    data = np.sort(data)
    f = np.zeros(len(data),dtype=int)

    i = 0
    
    while i < len(data):
        j = i
        while (j < len(data) and data[i] == data[j]):
            f[i]+=1
            j+=1
        i=j       

    max_freq = int(np.max(f))

    if(max_freq == 1):
        modas = np.array([])
    else:
        modas = np.unique(data[f == max_freq])

    return modas, max_freq


#==================================
#    Configuración de aplicación
#==================================

st.set_page_config(
    page_title="Laboratorio de Estadística",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Laboratorio de Estadística Descriptiva")

st.write("Introduce un conjunto de datos para calcular sus medidas" \
" de tendencia central y dispersión, así como para visualizar su distribución.")

#==================================
#           Entrada de datos
#==================================

st.subheader("1. Introduce tus datos")


with st.form("formulario_datos"):
    st.write(
        "Escribe los números separados por comas, "
        "espacios o saltos de línea."
    )
    entrada = st.text_area(
    "Conjunto de datos",
    value="65, 70, 72, 75, 76, 78, 80, 82, "
    "84, 85, 87, 90, 92, 95, 130",
    height=100
    )
    enviar = st.form_submit_button(
        "Procesar datos",
        use_container_width=True
    )

archivo = st.file_uploader(
    "O carga un archivo CSV",
    type=["csv"]
)



datos = None


try:
    if archivo is not None:
        df = pd.read_csv(archivo)

        columnas_num = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if not columnas_num:
            st.error("El archivo no contiene columnas numéricas.")
            st.stop()

        columna = st.selectbox(
            "Selecciona la columna numérica que deseas analizar",
            columnas_num)
        
        datos =df[columna].dropna().to_numpy(dtype=float)

    else:

        texto = entrada.replace(",", " ")
        valores = texto.split()

        datos = np.array(
            [float(valor) for valor in valores],
            dtype = float
        )

    if datos.size == 0:

        st.warning("Introduce al menos un dato.")
        st.stop()

    if not np.all(np.isfinite(datos)):
        
        st.error("Todos los datos deben ser números finitos.")
        st.stop()

except ValueError:

    st.error("Revisa los datos: utiliza números separados "
             "por comas, espacios o saltos de línea.")

    st.stop()

except Exception as error:

    st.error(f"Se produjo un error inesperado: {error}")
    st.stop()

#==================================
#     Configuración estadística
#==================================


st.subheader("2. Configuración estadística")

tipo_varianza = st.radio(
    "¿Cómo deseas calcular la varianza?",
    ["Poblacional", "Muestral"],
    horizontal=True
)


st.subheader("3. Resultados Estadísticos")

if tipo_varianza == "Poblacional":
    media = datos.mean()
    moda, max_freq = Mode(datos)
    mediana = np.median(datos)
    varianza = datos.var(ddof=0)
    desviacion_estandar = np.sqrt(varianza)
    xmin = datos.min()
    xmax = datos.max()
    rango = xmax - xmin
    q1 = np.percentile(datos,25)
    q2 = mediana
    q3 = np.percentile(datos,75)
    RIQ = q3 - q1

else:
    media = datos.mean()
    moda, max_freq = Mode(datos)
    mediana = np.median(datos)
    varianza = datos.var(ddof=1)
    desviacion_estandar = np.sqrt(varianza)
    xmin = datos.min()
    xmax = datos.max()
    rango = xmax - xmin
    q1 = np.percentile(datos,25)
    q2 = mediana
    q3 = np.percentile(datos,75)
    RIQ = q3 - q1


data1 = pd.DataFrame(
    {
        "Medidas de variabilidad": [
            r"Varianza ($\sigma^{2})$",
            r"Desviación Estándar ($\sigma$)",
            r"$x_{min}$",
            r"$x_{max}$",
            r"Rango ($R$)",
            r"Primer Cuartil ($Q_{1}$)",
            r"Segundo cuartil ($Q_{2}$)",
            r"Tercer Cuartil ($Q_{3}$)",
            r"Rango Intercuartílico ($RIQ$)"
        ],
        "Valor": [
            varianza,
            desviacion_estandar,
            xmin,
            xmax,
            rango,
            q1,
            q2,
            q3,
            RIQ
        ]
    }
)
st.table(data=data1,border=True, width="stretch", height="content", hide_index=None, hide_header=None, alt=None)


data2 = pd.DataFrame(
    {
        "Medidas de tendencia central": [
            r"Número total de datos",
            r"Media($\bar{x})$",
            r"Mediana($Me$)"
        ],
        "Valor": [
            int(len(datos)),
            media,
            mediana
        ]
    }
)

#==================================
#     Relleno de tablas
#==================================


st.table(data=data2,border=True, width="stretch", height="content", hide_index=None, hide_header=None, alt=None)



#==================================
#    Determinación de la moda
#==================================


if len(moda) == 0.0:
    st.write("No hay moda en el conjunto de datos.")
else:
    st.write("Moda(s):", moda, "con frecuencia:", max_freq)




#==================================
#  Histograma y Diagrama de Caja
#==================================

#Creación de Columnas

col1, col2 = st.columns(2)

with col1:

    st.subheader("Histograma")

    fig1 = plt.figure(figsize=(12, 5))

    plt.subplot(1,2,1)
    plt.hist(datos, bins='auto', color="#b6142a8b", alpha=0.7, rwidth=0.85,edgecolor='black')
    plt.scatter(
        media, 0,                      # Coordenadas (x=media, y=0)
        color="#2268d1",                   # Color del punto
        marker='^',
        s=100,                         # Tamaño del punto
        zorder=5,                      # Asegura que se dibuje por encima de los ejes
        clip_on=False,                 # Evita que el borde del gráfico corte el punto
        label=f'Media: {media:.2f}'
    )
    plt.axvline(mediana, color='green', linestyle='-.', linewidth=1, label=f'Mediana: {mediana:.2f}')
    plt.axvline(media+desviacion_estandar, color='black', linestyle='--', linewidth=1, label=r'$\bar{x}+\sigma$'f': {media+desviacion_estandar:.2f}')
    plt.axvline(media-desviacion_estandar, color='black', linestyle='--', linewidth=1, label=r'$\bar{x}-\sigma$'f': {media-desviacion_estandar:.2f}')

    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    # Ajuste estrecho del lienzo
    fig1.tight_layout()
    



with col2:

    st.subheader("Diagrama de Caja y Bigote")
    fig2 = plt.figure(figsize=(12,5))

    plt.subplot(1, 2, 2)
    plt.boxplot(datos, vert=False, patch_artist=True)
    plt.title("Diagrama de Caja y Bigotes")
    plt.xlabel("Valores")
    plt.grid()

    fig2.tight_layout()
    


tab1, tab2 = st.tabs(["📊 Histograma", "📦 Diagrama de Caja"])
with tab1:
    st.pyplot(fig1, use_container_width=True)
with tab2:
    st.pyplot(fig2, use_container_width=True)

st.markdown(
    """
    <hr style="margin-top: 50px;">

    <div style="
        text-align: center;
        color: #808495;
        font-size: 14px;
        padding: 10px;
    ">
        <p>
            © 2026 | Laboratorio de Estadística Descriptiva
        </p>
        <p>
             MCAF Ozzy Orozco
        </p>
        <p>
            Bioestadística y Ciencia de Datos
        </p>
    </div>
    """,
    unsafe_allow_html=True
)