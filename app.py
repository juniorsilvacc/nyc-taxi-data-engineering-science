import streamlit as st
import pandas as pd
import joblib
import os
from sqlalchemy import create_engine, text
import pydeck as pdk

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NYC Taxi Heatmap & Predictor | Junior Silva",
    page_icon="🚕",
    layout="wide"
)

# --- CONEXÃO E RECURSOS (CACHE) ---
@st.cache_resource
def load_resources():
    # 1. Carregar Modelo
    model_path = 'modelo_taxi_nyc.pkl'
    if not os.path.exists(model_path):
        return None, None
    
    model = joblib.load(model_path)
    
    # 2. Conexão Postgres
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/nyc_taxi_db')
    return model, engine

model, engine = load_resources()

# --- INTERFACE PRINCIPAL ---
st.title("🚕 NYC Taxi Data Analytics")
st.markdown("""
Esta aplicação utiliza um modelo de **Machine Learning (Random Forest)** para prever o valor de corridas 
e analisa a densidade de tráfego baseada na arquitetura **Medallion (dbt + Postgres)**.
""")

if model is None:
    st.error("O arquivo 'modelo_taxi_nyc.pkl' não foi encontrado na raiz do projeto.")
    st.info("Certifique-se de gerá-lo no seu notebook de treino antes de rodar o Streamlit.")
    st.stop()

# --- SIDEBAR: PREVISÃO DE TARIFAS ---
st.sidebar.header("🤖 Calculadora de Tarifa (ML)")
st.sidebar.markdown("Insira os detalhes para prever o custo:")

distancia = st.sidebar.number_input("Distância da Viagem (milhas)", min_value=0.1, value=1.5, step=0.1)
hora = st.sidebar.slider("Hora do Dia", 0, 23, 12)
dia_semana = st.sidebar.selectbox("Dia da Semana", 
                                ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
passageiros = st.sidebar.number_input("Qtd de Passageiros", min_value=1, max_value=6, value=1)

# Mapeamento para o modelo
dias_map = {"Segunda":0, "Terça":1, "Quarta":2, "Quinta":3, "Sexta":4, "Sábado":5, "Domingo":6}
fds = 1 if dia_semana in ["Sábado", "Domingo"] else 0

if st.sidebar.button("💸 Calcular Previsão"):
    # Criar DataFrame com a mesma estrutura usada no treino
    input_df = pd.DataFrame([[distancia, hora, dias_map[dia_semana], fds]], 
                           columns=['trip_distance', 'hour_of_day', 'day_of_week', 'is_weekend'])
    
    with st.spinner('Calculando previsão...'):
        predicao = model.predict(input_df)[0]
    
    st.sidebar.metric("Valor Estimado", f"$ {predicao:.2f}")
    st.sidebar.info("Nota: O valor inclui taxas base e impacto do trânsito.")

# --- CORPO PRINCIPAL: MAPA E MÉTRICAS ---
tab1, tab2 = st.tabs(["🔥 Mapa de Calor (Heatmap)", "📊 Métricas do Modelo"])

with tab1:
    st.subheader("Densidade de Coletas por Turno")
    col_sel, col_leg = st.columns([1, 2])
    
    with col_sel:
        turno = st.selectbox("Selecione o Turno para analisar a demanda:", 
                           ['Manhã', 'Tarde', 'Noite', 'Madrugada'])

    @st.cache_data(ttl=600)
    def get_heatmap_data(turno_sel):
        # Aumentamos o sample para 2.5% para o Heatmap ficar mais preenchido, 
        # mas com filtro rígido de Manhattan para não quebrar.
        query = f"""
        SELECT 
            pickup_latitude as lat, 
            pickup_longitude as lon
        FROM public.fct_taxi_trips f
        JOIN public.dim_time t ON f.time_key = t.time_key
        WHERE t.shift_name = '{turno_sel}'
          AND pickup_latitude BETWEEN 40.68 AND 40.85
          AND pickup_longitude BETWEEN -74.02 AND -73.93
          AND random() < 0.025 
        LIMIT 10000;
        """
        return pd.read_sql(text(query), engine)

    with st.spinner(f'Gerando mapa de calor para o turno: {turno}...'):
        df_heatmap = get_heatmap_data(turno)
        
        if not df_heatmap.empty:
            st.write(f"Exibindo densidade baseada em {len(df_heatmap)} pontos de coleta.")
            
            # Configuração do Mapa de Calor (Pydeck HeatmapLayer)
            view_state = pdk.ViewState(
                latitude=40.7600, 
                longitude=-73.9800, 
                zoom=11.8, 
                pitch=0
            )
            
            # Camada de Heatmap: Clássica e leve para o WSL
            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                df_heatmap,
                get_position="[lon, lat]",
                # Define a intensidade do ponto: 
                # Maior rádio = manchas maiores, menor rádio = manchas menores
                aggregation=pdk.types.String('SUM'),
                get_weight="[1]", # Cada ponto conta como 1
                radius_pixels=30, # Tamanho do "blur" de cada ponto
                intensity=1,
                threshold=0.05,
                color_range=[ # Paleta de cores (do claro ao vermelho escuro)
                    [255, 255, 178], # Amarelo (Demanda Baixa)
                    [254, 217, 118],
                    [254, 178, 76],
                    [253, 141, 60],
                    [240, 59, 32],
                    [189, 0, 38]     # Vermelho Escuro (Demanda Alta)
                ]
            )
            
            # Renderiza o mapa com estilo escuro (Dark Mode)
            st.pydeck_chart(pdk.Deck(
                layers=[heatmap_layer], 
                initial_view_state=view_state, 
                map_style="mapbox://styles/mapbox/dark-v9"
            ))
        else:
            st.warning(f"Sem dados suficientes para gerar o mapa de calor no turno: {turno}.")

with tab2:
    st.subheader("Performance e Insights da Modelagem")
    c1, c2, c3 = st.columns(3)
    c1.metric("Dataset Total (Warehouse)", "47M+ Linhas")
    c2.metric("MAE (Erro Médio)", "$ 2.15")
    c3.metric("R² Score", "0.88")

    st.markdown("""
    ### Por que esse App é útil?
    * **Para Passageiros:** A calculadora ajuda a estimar custos rapidamente, considerando a hora do dia.
    * **Para Motoristas/Empresas:** O mapa de calor revela as "zonas quentes" de Manhattan, ajudando a posicionar a frota onde a demanda é maior em cada turno.
    * **Para o Portfólio:** Demonstra a união de Engenharia de Dados (dbt/Postgres) com Ciência de Dados (Machine Learning) e Desenvolvimento Web (Streamlit).
    """)

st.divider()
st.caption("Projeto desenvolvido por Junior Silva - Engenheiro de Dados")