#Bibliotecas


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

#Livrarias
from streamlit_folium import folium_static
from PIL import Image
from datetime import datetime, timedelta
from haversine import haversine

st.set_page_config(page_title="Visão Entregadores", page_icon="🛵", layout="wide")


#ler arquivo
df = pd.read_csv("C:\\Users\\aguiar.gustavo\\Documents\\repos\\ftc_programacao_python\\dataset\\train.csv")

#Criando Copia
df1 = df.copy()

#Filtrar NaN das linhas

linhas_selec = (df1["Road_traffic_density"]!="NaN ") & (df1["Type_of_order"]!="NaN ") & (df1["Type_of_vehicle"]!="NaN ") & (df1["City"]!="NaN ") & (df1["Weatherconditions"]!="NaN ") & (df1["multiple_deliveries"]!="NaN ") & (df1["Delivery_person_Age"]!="NaN ") & (df1["Festival"]!="NaN ")

df1 = df1.loc[linhas_selec,:]

#Ajustar string das colunas com espaço a mais

df1["ID"] = df1["ID"].str.strip()
df1["Delivery_person_Age"] = df1["Delivery_person_Age"].str.strip()
df1["Road_traffic_density"] = df1["Road_traffic_density"].str.strip()
df1["Type_of_order"] = df1["Type_of_order"].str.strip()
df1["Type_of_vehicle"] = df1["Type_of_vehicle"].str.strip()
df1["Festival"] = df1["Festival"].str.strip()
df1["City"] = df1["City"].str.strip()
df1["Festival"] = df1["Festival"].str.strip()


#reset no index para melhor utilização
df1 = df1.reset_index(drop=True)

#ajuste no tipo de objeto que é a coluna
df1["Order_Date"] = pd.to_datetime(df1["Order_Date"], format="%d-%m-%Y")
df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
df1["Time_taken(min)"] = df1.loc[:,"Time_taken(min)"].str.split(" ").str[1]
df1["Time_taken(min)"] = df1["Time_taken(min)"].astype(int)

# =======================================================
#Barra Lateral
# =======================================================


#image_path = r"C:\Users\aguiar.gustavo\Documents\repos\Teste_gus\NTT_Data-Logo.wine.png"
image = Image.open("NTT_Data-Logo.wine.png")
st.sidebar.image(image, width=180)


st.title("Visao - Empresa - Curry Company")
st.sidebar.markdown("# Curry Company")
st.sidebar.markdown("## Fast Delivery in India")
st.sidebar.markdown("""---""")

#data_maxima = datetime.today() - timedelta(days=1)

st.sidebar.markdown("## Selecione uma data") 
data_slider = st.sidebar.slider('Qual Valor?',
                                value=datetime(2022, 4, 6), 
                                min_value=datetime(2022, 2, 11),
                                max_value=datetime(2022,4,6),
                                format="DD-MM-YYYY")

st.sidebar.markdown("""---""")

traffic_options = ["High","Low","Jam","Medium"]
options = st.sidebar.multiselect("Quais as condições do transito?",traffic_options,
                      default=traffic_options )


Clima_options = ["conditions Sunny","conditions Fog","conditions Cloudy","conditions Windy","conditions Sandstorms","conditions Stormy"]

clima = st.sidebar.multiselect("Quais climas gostaria de ver?",Clima_options, default=Clima_options)

city_options = ["Urban","Semi-Urban","Metropolitian"]

city = st.sidebar.multiselect("Quais cidades gostaria de escolher?", city_options, default=city_options)


st.sidebar.markdown("""---""")

st.sidebar.markdown("### Powered By Cantalice Company")


#filtro de data
linhas_selecionadas = df1["Order_Date"] < data_slider
df1 = df1.loc[linhas_selecionadas,:]


#filtro de Transito
linhas_selec_2 = df1["Road_traffic_density"].isin(options) 
df1 = df1.loc[linhas_selec_2,:]

#filtro clima
linhas_selec_3 = df1["Weatherconditions"].isin(clima)
df1 = df1.loc[linhas_selec_3,:]

#filtro cidade
linhas_selec_4 = df1["City"].isin(city)
df1 = df1.loc[linhas_selec_4,:]

# =======================================================
# Layout do streamlit
# =======================================================


tab1, tab2, tab3 = st.tabs(["Visao 1","Visao 2","Visao 3"])



with tab1:
    with st.container():
        st.markdown("Overall Metrics")
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            #Maior idade dos Entregadores
            Maior_idade = df1.loc[:,"Delivery_person_Age"].max()
            col1.metric("Maior de Idade",Maior_idade)


        
        with col2:
            #Menor Idade dos Entregadores
            Menor_idade = df1.loc[:,"Delivery_person_Age"].min()
            col2.metric("Menor de Idade",Menor_idade)
        with col3:
            Melhor_cond = df1.loc[:,"Vehicle_condition"].max()
            col3.metric("Melhor Condição",Melhor_cond)
        with col4:
            Pior_cond = df1.loc[:,"Vehicle_condition"].min()
            col4.metric("Pior Condição",Pior_cond)


    with st.container():
        st.markdown("""---""")
        st.markdown("Avaliações")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Avaliações Médias por Entregador")
            df_aux_entr_3 = (df1.loc[:,["Delivery_person_ID","Delivery_person_Ratings"]]
                             .groupby("Delivery_person_ID")
                             .agg(Med_entr = ("Delivery_person_Ratings","mean"))
                             .reset_index())

            df_aux_entr_3 = (df_aux_entr_3.sort_values(by="Med_entr",ascending=False)
                             .reset_index(drop=True))

            st.dataframe(df_aux_entr_3)

        with col2:
            st.markdown("Avaliações Média por Transito")
            df_aux_entr_4 = (df1.loc[:,["Delivery_person_Ratings","Road_traffic_density"]]
                             .groupby("Road_traffic_density")
                             .agg(Media_Densidade=("Delivery_person_Ratings","mean"),Desvio_Densidade=("Delivery_person_Ratings","std"))
                             .reset_index())

            df_aux_entr_4 = (df_aux_entr_4.sort_values(by="Media_Densidade",ascending=False)
                             .reset_index(drop=True))
            st.dataframe(df_aux_entr_4)

            st.markdown("Avaliação Média por Clima")
            df_aux_entr_5 = (df1.loc[:,["Delivery_person_Ratings","Weatherconditions"]]
                             .groupby("Weatherconditions")
                             .agg(Media_Densidade=("Delivery_person_Ratings","mean"),Desvio_Densidade=("Delivery_person_Ratings","std"))
                             .reset_index())

            df_aux_entr_5 = (df_aux_entr_5.sort_values(by="Media_Densidade",ascending=False)
                             .reset_index(drop=True))

            st.dataframe(df_aux_entr_5)



    with st.container():
        st.markdown("""---""")
        st.markdown("Velocidade de Entrega")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("Top Entregadores Mais Rápidos")
            df_aux_entr_6 = (df1.loc[:,["Time_taken(min)","City","Delivery_person_ID"]]
                             .groupby(["City","Delivery_person_ID"])
                             .agg(Tempo=("Time_taken(min)","min"))
                             .reset_index())
            

            df_aux_entr_6 = df_aux_entr_6.sort_values(by=["City","Tempo"],ascending=True)

            df_aux_entr_16 = df_aux_entr_6.loc[df_aux_entr_6["City"]=="Metropolitian",:].head(10)

            df_aux_entr_17 = df_aux_entr_6.loc[df_aux_entr_6["City"]=="Urban",:].head(10)

            df_aux_entr_18 = df_aux_entr_6.loc[df_aux_entr_6["City"]=="Semi-Urban",:].head(10)

            df_final_velo = (pd.concat( [df_aux_entr_16,df_aux_entr_17,df_aux_entr_18])
                             .reset_index(drop=True))
            st.dataframe(df_final_velo)


        with col2:
            st.markdown("Top Entregadores Mais Lentos")
            df_aux_entr_7 = (df1.loc[:,["Time_taken(min)","City","Delivery_person_ID"]]
                             .groupby(["City","Delivery_person_ID"])
                             .agg(Tempo=("Time_taken(min)","max"))
                             .reset_index())

            df_aux_entr_7 = df_aux_entr_7.sort_values(by=["City","Tempo"],ascending=False)

            df_aux_entr_19 = df_aux_entr_7.loc[df_aux_entr_6["City"]=="Metropolitian",:].head(10)

            df_aux_entr_20 = df_aux_entr_7.loc[df_aux_entr_6["City"]=="Urban",:].head(10)

            df_aux_entr_21 = df_aux_entr_7.loc[df_aux_entr_6["City"]=="Semi-Urban",:].head(10)

            df_final_velo_2 = (pd.concat( [df_aux_entr_19,df_aux_entr_20,df_aux_entr_21])
                               .sort_values(by=["City","Tempo"],ascending=False)
                               .reset_index(drop=True))
            
            st.dataframe(df_final_velo_2)


        

            
        






















































































































