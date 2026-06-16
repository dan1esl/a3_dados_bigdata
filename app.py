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

st.subheader("Heatmap dos 10 Maiores Jogos por Premiação e Audiência")

heatmap_df = (
    df_filtrado
    .groupby("Jogo", as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum",
        "Torneios": "sum"
    })
)

top10 = (
    heatmap_df
    .sort_values("Horas Assistidas", ascending=False)
    .head(10)
    .copy()
)

top10["Audiência"] = (
    top10["Horas Assistidas"] /
    top10["Horas Assistidas"].max()
) * 100

top10["Premiações (%)"] = (
    top10["Premiações"] /
    top10["Premiações"].max()
) * 100

top10["Torneios (%)"] = (
    top10["Torneios"] /
    top10["Torneios"].max()
) * 100

heatmap_data = (
    top10[
        ["Jogo", "Audiência", "Premiações (%)", "Torneios (%)"]
    ]
    .set_index("Jogo")
)

fig = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    labels={
        "x": "Métrica",
        "y": "Jogo",
        "color": "Índice"
    }
)

fig.update_layout(
    title="Top 10 Jogos — Comparação Normalizada (%)",
    coloraxis_colorbar_title="Índice"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Principais Insights")

insights = (
    df_filtrado
    .groupby("Jogo", as_index=False)
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum",
        "Torneios": "sum"
    })
)

mais_assistido = insights.loc[
    insights["Horas Assistidas"].idxmax()
]

mais_premiado = insights.loc[
    insights["Premiações"].idxmax()
]

mais_torneios = insights.loc[
    insights["Torneios"].idxmax()
]

insights = insights[
    insights["Horas Assistidas"] > 0
].copy()

insights["Premiação por 1M Horas"] = (
    insights["Premiações"] /
    insights["Horas Assistidas"]
) * 1_000_000

insights_relacao = insights[
    insights["Horas Assistidas"] >= insights["Horas Assistidas"].quantile(0.25)
]

melhor_relacao = insights_relacao.loc[
    insights_relacao["Premiação por 1M Horas"].idxmax()
]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎮 Jogo Mais Assistido",
        mais_assistido["Jogo"]
    )

    st.caption(
        f"{mais_assistido['Horas Assistidas']:,.0f} horas assistidas"
    )

    st.metric(
        "💰 Jogo com Maior Premiação",
        mais_premiado["Jogo"]
    )

    st.caption(
        f"US$ {mais_premiado['Premiações']:,.0f}"
    )

with col2:
    st.metric(
        "🏆 Jogo com Mais Torneios",
        mais_torneios["Jogo"]
    )

    st.caption(
        f"{mais_torneios['Torneios']:,.0f} torneios"
    )

    st.metric(
        "📈 Melhor Relação Premiação/Audiência",
        melhor_relacao["Jogo"]
    )

    st.caption(
        f"US$ {melhor_relacao['Premiação por 1M Horas']:,.0f} por 1 milhão de horas assistidas"
    )

st.markdown("---")

st.info(
    f"""
### Resumo do Período

🎮 **{mais_assistido['Jogo']}** foi o jogo mais assistido, acumulando **{mais_assistido['Horas Assistidas']:,.0f} horas assistidas**.

💰 **{mais_premiado['Jogo']}** distribuiu o maior volume de premiações, totalizando **US$ {mais_premiado['Premiações']:,.0f}**.

🏆 **{mais_torneios['Jogo']}** liderou em quantidade de torneios, com **{mais_torneios['Torneios']:,.0f} eventos realizados**.

📈 Considerando a relação entre audiência e premiações, **{melhor_relacao['Jogo']}** apresentou o melhor desempenho, gerando aproximadamente **US$ {melhor_relacao['Premiação por 1M Horas']:,.0f}** em premiações para cada milhão de horas assistidas.
"""
)