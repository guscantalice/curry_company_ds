#Bibliotecas


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium

#Livrarias
from streamlit_folium import folium_static
from PIL import Image
from datetime import datetime, timedelta
from haversine import haversine



st.set_page_config(page_title="Visão Empresa", page_icon="📈", layout="wide")

#------------------------------------------------------------------

# Funções

#-----------------------------------------------------------------
def order_metric(df1):
    cols = ["ID","Order_Date"]
    df1_ = df1.loc[:,cols].groupby("Order_Date").agg(Pedidos=("ID","count")).reset_index()
    fig1 = px.bar( df1_, x="Order_Date", y="Pedidos")        
    
    
    return fig1


def share_semana(df1):
     filtro_3 = ["ID","Road_traffic_density"]
     df2_aux = df1.loc[:,filtro_3].groupby("Road_traffic_density").agg(Pedidos=("ID","count")).reset_index()
     df2_aux["Share"] =  df2_aux["Pedidos"]/ df2_aux["Pedidos"].sum()
     fig2 = px.pie(df2_aux, values="Share", names="Road_traffic_density")
     

     return fig2


def traffic_order_share(df1):
    traf_ = ["ID","City","Road_traffic_density"]
    df_aux_4 = (df1.loc[:,traf_]
                .groupby(["City","Road_traffic_density"])
                .agg(Pedidos=("ID","count"))
                .reset_index())
    
    fig3 = px.scatter(df_aux_4, x="City", y="Road_traffic_density",size="Pedidos", color="City")
    return fig3



def order_by_week(df1):
    df1["Week_of_Year"] = df1["Order_Date"].dt.strftime("%U")
    cols_2 = ["Week_of_Year","ID"]
    week_f = df1.loc[:,cols_2].groupby("Week_of_Year").agg(Pedidos=("Week_of_Year","count")).reset_index()
    fig4 = px.line(week_f , x="Week_of_Year",y="Pedidos")

    return fig4


def entregadores_by_week (df1):
    df_04 = (df1.loc[:,["ID","Delivery_person_ID","Week_of_Year"]]
             .groupby("Week_of_Year")
             .agg(Pedidos=("ID","count"),Entregadores=("Delivery_person_ID","nunique"))
             .reset_index())
    
    df_04["Qtd_Med_Pedidos"] = df_04["Pedidos"]/df_04["Entregadores"]
    fig5 = px.line(df_04, x="Week_of_Year", y="Qtd_Med_Pedidos" )

    return fig5

def mapa_mundi (df1):
        df_aux_6 = (df1.loc[:,["City", "Road_traffic_density","Delivery_location_latitude","Delivery_location_longitude"]]
                    .groupby(["City","Road_traffic_density"])
                    .median()
                    .reset_index())

        map = folium.Map()


        for i in range(len(df_aux_6)):
            folium.Marker([df_aux_6.loc[i,"Delivery_location_latitude"],
                           df_aux_6.loc[i,"Delivery_location_longitude"]],
                          popup=df_aux_6.loc[i,["City","Road_traffic_density"]]).add_to(map)

        return map





def clean_code( df1 ):

    """ Essa função tem a responsabilidade de limpar o dataframe
    
        Tipos de Limpeza:
        1- Remoção dos dados NaN
        2- Remoção de Espaço no final da String
        3- Conversão de cada coluna em objeto para DateTime, Int, Float e Conversão de TimeTaken para Número

        Input: Dataframe
        Output: DataFrame
    
    
    """
    
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
    df1["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y")
    df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
    df1["Time_taken(min)"] = df1.loc[:,"Time_taken(min)"].str.split(" ").str[1]
    df1["Time_taken(min)"] = df1["Time_taken(min)"].astype(int)

    return df1

#------------------------------------------------------------------

# Término de funções

#-----------------------------------------------------------------

#-- Importando o Código

#ler arquivo
df = pd.read_csv("C:\\Users\\aguiar.gustavo\\Documents\\repos\\ftc_programacao_python\\dataset\\train.csv")


#Limpando os Dados
df1 = clean_code( df )





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



tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])





with tab1: 
    with st.container():
        fig1 = order_metric(df1)
        st.markdown("# Orders by day")
        st.plotly_chart(fig1 , use_container_width=True)
        
       
        

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                #Resposta 2 - Gráfico de Pizza - Share
                #Acrescentar Semana
                fig2 = share_semana(df1)
                st.markdown("### Distribuição dos pedidos por tipo de tráfego")               
                st.plotly_chart(fig2, use_container_width=True)
    
                
            
            with col2:
                fig3 = traffic_order_share(df1)
                st.markdown("### Volume de Pedidos por Cidade e Tráfego")                
                st.plotly_chart(fig3, use_container_width=True)

                


                
                

with tab2:
     with st.container():
        fig4 = order_by_week(df1)
        st.markdown("## Pedidos por Semana")        
        st.plotly_chart(fig4, use_container_width=True) 

    
        

         #Resposta - Week - Entregadores por semana - Tab2
        fig5 = entregadores_by_week (df1)
        st.markdown("## Entregadores por Semana")
        st.plotly_chart(fig5,use_container_width=True)
                 
         
        

with tab3:
    #Mapa Geográfico - Visão Geográfica - Tab3
        map = mapa_mundi(df1)
        folium_static(map, width=1024 , height=600)




































