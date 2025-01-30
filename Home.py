import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="😵‍💫",
    layout="wide"
)


#image_path = "C:\\Users\\aguiar.gustavo\\Documents\\repos\\Teste_gus\\NTT_Data-Logo.wine.png"
image = Image.open("NTT_Data-Logo.wine.png")
st.sidebar.image(image, width=180)


st.title("Visao - Empresa - Curry Company")
st.sidebar.markdown("# Curry Company")
st.sidebar.markdown("## Fast Delivery in India")
st.sidebar.markdown("""---""")


st.write("# Curry Company Growth Dashboard")


st.markdown("""### Como utilizar o Dashboard?
            - Visão Empresa:
                - Visão Gerencial: Métricas gerais de comportamento
                - Visão Tática: Indicadores semanais de crescimento
                - Visão Geográfica: Inisights de Geolocalização.

            - Visão Entregador:
                -Acompanhamento dos Indicadores semanais de crescimento.

            - Visão Restaurantes:
                - Indicadores semanais de crescimento dos restaurantes.

            Ask for Help
            - Time de Data Science Luiza Labs
                Aguiar.Gustavo
             """)
