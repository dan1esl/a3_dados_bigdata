import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Dashboard E-Sports",
    layout="wide"
)

# =========================
# CARREGAMENTO DOS DADOS
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("dados_unificados_esports.csv")

    df = df.rename(columns={
        "Game": "Jogo",
        "Year": "Ano",
        "Month": "Mês",
        "Hours_watched": "Horas Assistidas",
        "Peak_viewers": "Pico de Espectadores",
        "Avg_viewers": "Média de Espectadores",
        "Earnings": "Premiações",
        "Players": "Jogadores",
        "Tournaments": "Torneios",
        "metacritic": "Nota Metacritic",
        "user_rating": "Avaliação dos Usuários",
        "avg_playtime_hours": "Tempo Médio de Jogo (h)",
        "genero_principal": "Gênero",
        "release_year": "Ano de Lançamento",
        "platform_count": "Quantidade de Plataformas",
        "is_multiplayer": "Multijogador",
        "engagement_score": "Score de Engajamento",
        "popularity_score": "Score de Popularidade"
    })

    return df

df = load_data()

# =========================
# FILTROS
# =========================

st.sidebar.title("Filtros")

ano_min = int(df["Ano"].min())
ano_max = int(df["Ano"].max())

anos_sel = st.sidebar.slider(
    "Período",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max)
)

df_filtrado = df[
    (df["Ano"] >= anos_sel[0]) &
    (df["Ano"] <= anos_sel[1])
]

# =========================
# CABEÇALHO
# =========================

st.title("Análise de Dados E-Sports")

st.markdown(
    "Dashboard interativo para análise de audiência, premiações e popularidade dos jogos eletrônicos."
)

# =========================
# INDICADORES PRINCIPAIS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Jogos",
        df_filtrado["Jogo"].nunique()
    )

with col2:
    st.metric(
        "Horas Assistidas",
        f"{df_filtrado['Horas Assistidas'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Premiações",
        f"US$ {df_filtrado['Premiações'].sum()/1_000_000:.1f} Mi"
    )

with col4:
    st.metric(
        "Torneios",
        f"{df_filtrado['Torneios'].sum():,.0f}"
    )

st.divider()

# =========================
# EVOLUÇÃO DAS HORAS ASSISTIDAS POR GÊNERO
# =========================

st.subheader("Evolução das Horas Assistidas por Gênero")

evolucao_genero = (
    df_filtrado
    .groupby(["Ano", "Gênero"], as_index=False)["Horas Assistidas"]
    .sum()
)

fig = px.line(
    evolucao_genero,
    x="Ano",
    y="Horas Assistidas",
    color="Gênero",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# EVOLUÇÃO DAS PREMIAÇÕES POR GÊNERO
# =========================

st.subheader("Evolução das Premiações por Gênero")

evolucao_premiacoes = (
    df_filtrado
    .groupby(["Ano", "Gênero"], as_index=False)["Premiações"]
    .sum()
)

fig = px.line(
    evolucao_premiacoes,
    x="Ano",
    y="Premiações",
    color="Gênero",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# AUDIÊNCIA E PREMIAÇÕES POR GÊNERO
# =========================

col1, col2 = st.columns(2)

with col1:
    genero_view = (
        df_filtrado
        .groupby("Gênero", as_index=False)["Horas Assistidas"]
        .sum()
        .sort_values("Horas Assistidas", ascending=False)
    )

    fig = px.bar(
        genero_view,
        x="Gênero",
        y="Horas Assistidas",
        title="Audiência por Gênero"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    genero_earn = (
        df_filtrado
        .groupby("Gênero", as_index=False)["Premiações"]
        .sum()
        .sort_values("Premiações", ascending=False)
    )

    fig = px.bar(
        genero_earn,
        x="Gênero",
        y="Premiações",
        title="Premiações por Gênero"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# RANKING DE JOGOS (Alinhados pela hipótese de Ganhos)
# =========================

col1, col2, col3 = st.columns(3)

top_games_base = (
    df_filtrado
    .groupby("Jogo", as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum",
        "Torneios": "sum"
    })
    .sort_values("Premiações", ascending=False)
    .head(15)
)

with col1:
    st.subheader("Jogos Maiores Premiações")
    fig = px.bar(
        top_games_base,
        x="Premiações",
        y="Jogo",
        orientation="h"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Audiência dos Jogos que Mais Pagam")
    fig = px.bar(
        top_games_base,
        x="Horas Assistidas",
        y="Jogo",
        orientation="h"
    )

    fig.update_layout(yaxis={'categoryorder':'array', 'categoryarray': top_games_base['Jogo'][::-1]})
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("Torneios dos Jogos que Mais Pagam")
    fig = px.bar(
        top_games_base,
        x="Torneios",
        y="Jogo",
        orientation="h"
    )
    fig.update_layout(yaxis={'categoryorder':'array', 'categoryarray': top_games_base['Jogo'][::-1]})
    st.plotly_chart(fig, use_container_width=True)

# =========================
# RELAÇÃO ENTRE AUDIÊNCIA E PREMIAÇÃO
# =========================

st.subheader("Mercado Competitivo dos Jogos")

bubble = (
    df_filtrado
    .groupby(["Jogo", "Gênero"], as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum",
        "Torneios": "sum"
    })
)

bubble = bubble[bubble["Horas Assistidas"] > 0]

fig = px.scatter(
    bubble,
    x="Horas Assistidas",
    y="Premiações",
    size="Torneios",
    color="Gênero",
    hover_name="Jogo",
    size_max=60,
    log_x=True,
    log_y=True,
    labels={
        "Horas Assistidas": "Audiência",
        "Premiações": "Premiações (US$)",
        "Torneios": "Quantidade de Torneios"
    }
)

fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True)

# =========================
# VALIDAÇÃO DE HIPÓTESE: MAIOR GANHO TRAZ MAIS AUDIÊNCIA?
# =========================

st.subheader("Validação de Hipótese: Maior ganho traz mais audiência?")

df_hipotese = (
    df_filtrado.groupby("Jogo", as_index=False)
    .agg({"Horas Assistidas": "sum", "Premiações": "sum", "Torneios": "sum"})
    .dropna()
)

df_hipotese = df_hipotese[(df_hipotese["Horas Assistidas"] > 0) & (df_hipotese["Torneios"] > 0)]

if df_hipotese.empty:
    st.warning("Não há dados suficientes para o período selecionado. Tente expandir o filtro de anos na barra lateral.")
else:
    matriz_corr_local = df_hipotese[["Horas Assistidas", "Premiações"]].corr(numeric_only=True)
    corr_ganhos_audiencia = matriz_corr_local.loc["Premiações", "Horas Assistidas"] if "Premiações" in matriz_corr_local.index else 0.0
    corr_ganhos_audiencia = 0.0 if pd.isna(corr_ganhos_audiencia) else corr_ganhos_audiencia

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label="Correlação: Ganhos vs. Audiência",
            value=f"{corr_ganhos_audiencia * 100:.1f}%",
            help="Mede se os jogos com maiores premiações tendem a ter proporcionalmente mais horas assistidas."
        )
    
    with col2:
        if corr_ganhos_audiencia > 0.7:
            st.success("Hipótese Confirmada: Existe uma forte ligação direta. Dinheiro pesado e grandes audiências andam juntos no topo.")
        elif corr_ganhos_audiencia > 0.4:
            st.warning("Hipótese Parcial: O dinheiro ajuda a trazer público, mas existem exceções que bombam mesmo pagando menos.")
        else:
            st.error("Hipótese Rejeitada: O tamanho da premiação não dita o engajamento de tela do público.")

    mais_assistido = df_hipotese.loc[df_hipotese["Horas Assistidas"].idxmax()]
    mais_premiado = df_hipotese.loc[df_hipotese["Premiações"].idxmax()]
    mais_torneios = df_hipotese.loc[df_hipotese["Torneios"].idxmax()]

    st.info(
        f"""
    ### Resumo de Destaques do Período Filtrado:

    * **{mais_assistido['Jogo']}** possui o maior engajamento de visualizações com **{mais_assistido['Horas Assistidas']:,.0f} horas assistidas**.
    * **{mais_premiado['Jogo']}** consolidou-se como o ecossistema mais lucrativo para os competidores, distribuindo um total de **US$ {mais_premiado['Premiações']:,.0f}**.
    * **{mais_torneios['Jogo']}** tem o maior número de torneios, registrando **{mais_torneios['Torneios']:,.0f} eventos oficiais**.
    """
    )