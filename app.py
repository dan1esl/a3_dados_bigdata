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
# RANKING DE JOGOS
# =========================

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("Jogos Mais Assistidos")

    top_games = (
        df_filtrado
        .groupby("Jogo", as_index=False)
        .agg({
            "Horas Assistidas": "sum"
        })
        .sort_values("Horas Assistidas", ascending=False)
        .head(15)
    )

    fig = px.bar(
        top_games,
        x="Horas Assistidas",
        y="Jogo",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Jogos com Mais Torneios")

    top_tournaments = (
        df_filtrado
        .groupby("Jogo", as_index=False)["Torneios"]
        .sum()
        .sort_values("Torneios", ascending=False)
        .head(15)
    )

    fig = px.bar(
        top_tournaments,
        x="Torneios",
        y="Jogo",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

with col3:

    st.subheader("Jogos com Maiores Premiações")

    top_earnings = (
        df_filtrado
        .groupby("Jogo", as_index=False)["Premiações"]
        .sum()
        .sort_values("Premiações", ascending=False)
        .head(15)
    )

    fig = px.bar(
        top_earnings,
        x="Premiações",
        y="Jogo",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# RELAÇÃO ENTRE AUDIÊNCIA E PREMIAÇÃO
# =========================

st.subheader("Relação entre Audiência e Premiação")

st.subheader("Premiação por Milhão de Horas Assistidas")

eficiencia = (
    df_filtrado
    .groupby(["Jogo"], as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum"
    })
)

eficiencia = eficiencia[
    eficiencia["Horas Assistidas"] > 0
]

eficiencia["Premiação por 1M Horas"] = (
    eficiencia["Premiações"] /
    eficiencia["Horas Assistidas"]
) * 1_000_000

top_eficiencia = (
    eficiencia
    .sort_values("Premiação por 1M Horas", ascending=False)
    .head(15)
)

fig = px.bar(
    top_eficiencia,
    x="Premiação por 1M Horas",
    y="Jogo",
    orientation="h",
    text_auto=".2s",
    color="Premiação por 1M Horas"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Premiação por 1 Milhão de Horas Assistidas",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("10 Maiores Jogos: Audiência x Premiação")

comparativo = (
    df_filtrado
    .groupby(["Jogo"], as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum"
    })
)

top15 = (
    comparativo
    .sort_values("Horas Assistidas", ascending=False)
    .head(10)
)

fig = px.bar(
    top15,
    y="Jogo",
    x=["Horas Assistidas", "Premiações"],
    barmode="group",
    orientation="h"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Valor",
    yaxis_title="",
    legend_title=""
)

st.plotly_chart(fig, use_container_width=True)