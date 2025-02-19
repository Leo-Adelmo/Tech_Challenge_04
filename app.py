import streamlit as st 
import pandas as pd
from web_scraping import web_scraping_dados_ipea
from model import ModeloPrevisao, tratando_base_dados
from datetime import datetime

def atualizar_base_dados_modelo(): 
    df = web_scraping_dados_ipea()
    df = tratando_base_dados(df)

    return df    

def carregar_infos_modelo(df):
    modelo = ModeloPrevisao(df)
    mae, rmse, r2 = modelo.avaliar_modelo()



# Criando o container com a classe CSS
    with st.container(): 
        st.markdown("## Características do modelo:")
        st.write(f"Mean Absolute Error (MAE): {mae:.4f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
        st.write(f"R² Score: {r2:.4f}")


    return modelo

st.title("Modelo preditivo do Preço do Petroleo brant")
df = atualizar_base_dados_modelo()
modelo = carregar_infos_modelo(df)


    
# Selectbox para escolher uma data para previsão
data_opcoes = df['Data'].dt.strftime('%d/%m/%Y').tail(30).tolist()
data_especifica = st.selectbox("Escolha uma data para previsão:", data_opcoes)

if data_especifica:
    data_especifica = datetime.strptime(data_especifica, '%d/%m/%Y')
    data, valor_previsto, valor_real = modelo.prever_valor_para_data_especifica(data_especifica)
    st.write(f"Valor previsto pelo modelo na data: {data} é R${valor_previsto:.2f}")
    st.write(f"Valor real nesse dia: {valor_real:.2f}")

if st.button("Atualizar Base de Dados"):
    df = atualizar_base_dados_modelo()
