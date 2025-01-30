#Bibliotecas


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np

#Livrarias
from streamlit_folium import folium_static
from PIL import Image
from datetime import datetime, timedelta
from haversine import haversine

st.set_page_config(page_title="Visão Restaurantes", page_icon="🥪", layout="wide")


#ler arquivo
df = pd.read_csv("dataset\train.csv")

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


tab1, tab2, tab3 = st.tabs(["Visão Gerencial","-","-"])


with tab1:
    with st.container():
        st.markdown("### Principais Métricas")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            ##st.markdown("Entregadores Únicos")
            Qtd_Entregador = len(df1.loc[:,"Delivery_person_ID"].unique())
            
            col1.metric("Entregadores", Qtd_Entregador)
    
        with col2:
            #st.markdown("Distância Média")
            cols_res_dv =["Restaurant_latitude","Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude"]
            df1["Distance"] = df1.loc[:,cols_res_dv].apply(lambda x: haversine((x["Restaurant_latitude"],x["Restaurant_longitude"]),(x["Delivery_location_latitude"],x["Delivery_location_longitude"])), axis=1)
            avg_distance = np.round(df1["Distance"].mean(),2)

            col2.metric("Distância Média",avg_distance)

    
        with col3:
            #st.markdown("Tempo de Entrega Médio c/ Festival")
            cols_time_4 = ["Time_taken(min)","Festival"]

            df_06_res = (df1.loc[:,cols_time_4]
                         .groupby("Festival")
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index())

            df_06_res = (df_06_res.sort_values(by="Medio_tempo",ascending=False)
                         .reset_index(drop=True))
            
            line_selec = np.round(df_06_res.loc[df_06_res["Festival"]=="Yes","Medio_tempo"],2)

            col3.metric("Tempo Medio",line_selec)

            
            
        with col4:
            #st.markdown("Desvio Padrão de Entrega c Festival")
            cols_time_5 = ["Time_taken(min)","Festival"]

            df_07_res = (df1.loc[:,cols_time_5]
                         .groupby("Festival")
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index())

            df_07_res = (df_07_res.sort_values(by="Medio_tempo",ascending=False)
                         .reset_index(drop=True))
            
            line_selec2 = np.round(df_07_res.loc[df_07_res["Festival"]=="Yes","Desvio_"],2)

            col4.metric("STD Entrega",line_selec2)
            
    
        with col5:
            #st.markdown("Tempo de Entrega Media s/ Festival")
            cols_time_6 = ["Time_taken(min)","Festival"]

            df_08_res = (df1.loc[:,cols_time_6]
                         .groupby("Festival")
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index())

            df_08_res = (df_08_res.sort_values(by="Medio_tempo",ascending=False)
                         .reset_index(drop=True))
            
            line_selec3 = np.round(df_08_res.loc[df_08_res["Festival"]=="No","Medio_tempo"],2)

            col5.metric("Tempo Medio",line_selec3)
    
        with col6:
            #st.markdown("Desvio Padrão de Entregas s/ Festival")
            cols_time_7 = ["Time_taken(min)","Festival"]

            df_09_res = (df1.loc[:,cols_time_7]
                         .groupby("Festival")
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index())

            df_09_res = (df_09_res.sort_values(by="Medio_tempo",ascending=False)
                         .reset_index(drop=True))
            
            line_selec4 = np.round(df_09_res.loc[df_09_res["Festival"]=="No","Desvio_"],2)

            col6.metric("STD Entrega",line_selec4)
    
        st.markdown("""---""")
    
    with st.container():
        st.markdown("### Tempo Médio de Entrega por Cidade")
        #st.markdown("Distancia Media de entrega por cidade")
        
        cols_res_dv = ["Restaurant_latitude","Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude"]
        df1["Distance"] = df1.loc[:,cols_res_dv].apply(lambda x: haversine((x["Restaurant_latitude"],x["Restaurant_longitude"]),(x["Delivery_location_latitude"],x["Delivery_location_longitude"])), axis=1)
        avg_distance = df1.loc[:,["City","Distance"]].groupby("City").mean().reset_index()

        fig = go.Figure( data=[go.Pie( labels=avg_distance['City'], values=avg_distance['Distance'], pull= [0,0.1,0])])
        st.plotly_chart(fig)
        
        st.markdown("""---""")
    
    with st.container():
        st.markdown("### Principais Insights")
    
        col1, col2 = st.columns(2, gap='large')
    
        with col1:
            st.markdown("Ditribuição do tempo por cidade")
            cols_time = ["Time_taken(min)","City"]

            df_03_res = (df1.loc[:,cols_time]
                         .groupby("City")
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index())

            
            df_03_res = np.round(df_03_res.sort_values(by="Medio_tempo",ascending=False),2)

            fig2 = go.Figure()
            fig2.add_trace( go.Bar ( name= 'Control',
                                   x= df_03_res["City"],
                                   y= df_03_res["Medio_tempo"],
                                   error_y= dict( type='data', array=df_03_res["Desvio_"] ) ) )

            fig2.update_layout(barmode='group')

            st.plotly_chart(fig2)

        
    
        with col2:
            st.markdown("Tempo médio por cidade")
            cols_time_3 = ["Time_taken(min)","City","Road_traffic_density"]

            df_05_res = (np.round(df1.loc[:,cols_time_3]
                         .groupby(["City","Road_traffic_density"])
                         .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                         .reset_index(),2))

            df_05_res = np.round(df_05_res.sort_values(by=["City","Medio_tempo"],ascending=False),2)

            fig3 = px.sunburst(df_05_res, path=['City','Road_traffic_density'], values='Medio_tempo',
                              color= 'Desvio_', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df_05_res["Desvio_"]))

            st.plotly_chart(fig3)
    
        st.markdown("""---""")
    
    with st.container():
        st.markdown("### Tabela")
    
        st.markdown("Tempo Medio por cidade e tipo de tráfego")
        cols_time_2 = ["Time_taken(min)","City","Type_of_order"]

        df_04_res = (df1.loc[:,cols_time_2]
                     .groupby(["City","Type_of_order"])
                     .agg(Medio_tempo=("Time_taken(min)","mean"),Desvio_=("Time_taken(min)","std"))
                     .reset_index())

        df_04_res = df_04_res.sort_values(by="Medio_tempo",ascending=False).reset_index(drop=True)

        st.dataframe(df_04_res)
    
    
