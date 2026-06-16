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

st.subheader("Mercado Competitivo dos Jogos")

bubble = (
    df_filtrado
    .groupby(
        ["Jogo", "Gênero"],
        as_index=False
    )
    .agg({
        "Horas Assistidas": "sum",
        "Premiações": "sum",
        "Torneios": "sum"
    })
)

bubble = bubble[
    bubble["Horas Assistidas"] > 0
]

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

fig.update_layout(
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# VALIDAÇÃO DE HIPÓTESE: O QUE GERA MAIS GANHOS?
# =========================

st.subheader("Principais Insights & Validação de Hipóteses")

df_hipotese = (
    df_filtrado.groupby("Jogo", as_index=False)
    .agg({"Horas Assistidas": "sum", "Premiações": "sum", "Torneios": "sum"})
    .copy()
)

df_hipotese = df_hipotese[df_hipotese["Horas Assistidas"] > 0]

corr_audiencia_ganhos = df_hipotese["Horas Assistidas"].corr(
    df_hipotese["Premiações"]
)
corr_torneios_ganhos = df_hipotese["Torneios"].corr(df_hipotese["Premiações"])

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="⚡ Força do Impacto da Audiência nos Ganhos",
        value=f"{corr_audiencia_ganhos * 100:.1f}%",
        help="Correlação linear entre Horas Assistidas e Premiações distribuídas.",
    )
    if corr_audiencia_ganhos > 0.7:
        st.success(" **Impacto Crítico:** A audiência é um motor direto de receita.")
    elif corr_audiencia_ganhos > 0.4:
        st.warning(" **Impacto Moderado:** A audiência ajuda, mas não dita tudo.")
    else:
        st.error(" **Impacto Fraco:** Audiência e ganhos operam isolados.")

with col2:
    st.metric(
        label="Impacto dos Torneios nos Ganhos",
        value=f"{corr_torneios_ganhos * 100:.1f}%",
        help="Correlação linear entre Quantidade de Torneios e Premiações distribuídas.",
    )
    if corr_torneios_ganhos > 0.7:
        st.success(
            " **Impacto Crítico:** Fazer mais eventos dita diretamente o tamanho das premiações."
        )
    elif corr_torneios_ganhos > 0.4:
        st.warning(
            " **Impacto Moderado:** O volume de torneios importa, mas o prêmio depende de outros fatores."
        )
    else:
        st.error(
            " **Impacto Fraco:** Ter muitos torneios não garante premiações milionárias."
        )

mais_assistido = df_hipotese.loc[df_hipotese["Horas Assistidas"].idxmax()]
mais_premiado = df_hipotese.loc[df_hipotese["Premiações"].idxmax()]
mais_torneios = df_hipotese.loc[df_hipotese["Torneios"].idxmax()]

df_hipotese["Premiação por 1M Horas"] = (
    df_hipotese["Premiações"] / df_hipotese["Horas Assistidas"]
) * 1_000_000
df_relacao_filtrada = df_hipotese[
    df_hipotese["Horas Assistidas"] >= df_hipotese["Horas Assistidas"].quantile(0.25)
]
melhor_relacao = df_relacao_filtrada.loc[
    df_relacao_filtrada["Premiação por 1M Horas"].idxmax()
]

st.markdown("---")
st.markdown("### 📝 Diagnóstico do Mercado Competitivo")

if corr_audiencia_ganhos > corr_torneios_ganhos:
    conclusao_mercado = f"""
    A análise matemática valida que **a audiência manda no jogo**. A correlação entre Horas Assistidas e Ganhos é de **{corr_audiencia_ganhos*100:.1f}%**, superando o impacto do volume de competições (**{corr_torneios_ganhos*100:.1f}%**). 
    
    Isso prova que o verdadeiro multiplicador financeiro no ecossistema de E-Sports não é a quantidade de campeonatos realizados, mas sim a capacidade do jogo de reter a atenção do público. Plataformas de streaming cheias atraem grandes patrocinadores e direitos de transmissão, inflando de forma exponencial as premiações das ligas principais (como vemos no caso de **{mais_premiado['Jogo']}**).
    """
else:
    conclusao_mercado = f"""
    A análise matemática valida que **o volume de eventos manda no jogo**. A correlação entre a Quantidade de Torneios e os Ganhos é de **{corr_torneios_ganhos*100:.1f}%**, superando o impacto da audiência pura (**{corr_audiencia_ganhos*100:.1f}%**). 
    
    Isso prova que uma cena competitiva capilarizada, ativa e com campeonatos recorrentes (liderada por títulos como **{mais_torneios['Jogo']}**) é o fator principal que movimenta a entrada de capital e a distribuição de prêmios no mercado, agindo de forma mais consistente do que picos de visualização em transmissões de entretenimento.
    """

st.info(
    f"""
{conclusao_mercado}

### 📊 Resumo de Destaques do Período Filtrado:

* 🎮 **{mais_assistido['Jogo']}** foi o campeão de atenção, acumulando um montante impressionante de **{mais_assistido['Horas Assistidas']:,.0f} horas assistidas**.
* 💰 **{mais_premiado['Jogo']}** consolidou-se como o ecossistema mais lucrativo para os competidores, distribuindo um total de **US$ {mais_premiado['Premiações']:,.0f}**.
* 🏆 **{mais_torneios['Jogo']}** apresentou a comunidade mais ativa e pulverizada, registrando **{mais_torneios['Torneios']:,.0f} eventos oficiais**.
* 📈 Fora os gigantes de massa, o título **{melhor_relacao['Jogo']}** obteve a melhor eficiência de conversão monetária, gerando aproximadamente **US$ {melhor_relacao['Premiação por 1M Horas']:,.0f}** em prêmios para cada 1 milhão de horas que a comunidade passou assistindo ao jogo.
"""
)