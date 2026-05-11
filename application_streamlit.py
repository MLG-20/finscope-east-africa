import re
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ═════════════════════════════════════════════════════════════════════════════
# 1. CONFIG PAGE
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Inclusion Financière - Afrique de l'Est",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Empêche Google Translate et Grammarly de modifier le DOM (cause du removeChild React)
components.html("""
<script>
try {
    var d = parent.document;
    d.documentElement.setAttribute('translate', 'no');
    d.documentElement.classList.add('notranslate');
    var meta = d.createElement('meta');
    meta.name = 'google';
    meta.content = 'notranslate';
    d.head.appendChild(meta);
    // Désactive Grammarly sur tous les éléments texte
    d.querySelectorAll('[data-gramm]').forEach(function(el) {
        el.setAttribute('data-gramm', 'false');
    });
} catch(e) {}
</script>
""", height=0)

# CSS personnalisé amélioré
css_enabled = False
if css_enabled:
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }

    /* ── GLOBAL HEADERS ── */
    h1 { color: #1a3a5c !important; font-weight: 700 !important; letter-spacing: -0.5px; }
    h2 { color: #1a3a5c !important; font-weight: 600 !important; }
    h3 { color: #2563a8 !important; font-weight: 600 !important; }

    /* ── HERO BANNER ── */
    .hero-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.75) !important;
        font-size: 1rem;
        margin: 0;
        max-width: 700px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0,212,255,0.2);
        border: 1px solid rgba(0,212,255,0.4);
        color: #00d4ff !important;
        border-radius: 50px;
        padding: 0.25rem 0.9rem;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e8edf3;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        border-left: 4px solid #2563a8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a3a5c;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-card .metric-delta {
        font-size: 0.8rem;
        color: #64748b;
    }

    /* ── INSIGHT BOXES ── */
    .insight-box {
        background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 100%);
        border: 1px solid #bdd7f0;
        border-left: 4px solid #2563a8;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    .insight-box .insight-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #1a3a5c;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .insight-box p {
        font-size: 0.9rem;
        color: #334155 !important;
        margin: 0;
        line-height: 1.6;
    }

    .warning-box {
        background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    .warning-box .insight-title { color: #92400e; }
    .warning-box p { color: #78350f !important; }

    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #86efac;
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    .success-box .insight-title { color: #166534; }
    .success-box p { color: #14532d !important; }

    /* ── SECTION DESCRIPTION ── */
    .section-desc {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    .section-desc p {
        color: #475569 !important;
        font-size: 0.92rem;
        margin: 0;
        line-height: 1.7;
    }

    /* ── KPI STRIP ── */
    .kpi-strip {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .kpi-item {
        flex: 1;
        background: #fff;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .kpi-item .kpi-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2563a8;
    }
    .kpi-item .kpi-lbl {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* ── CHART CONTAINER ── */
    .chart-wrapper {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #e8edf3;
        margin-bottom: 1rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }
    .chart-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1a3a5c;
        margin-bottom: 0.3rem;
    }
    .chart-subtitle {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-bottom: 1rem;
    }

    /* ── RECOMMANDATION CARD ── */
    .rec-card {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
    }
    .rec-number {
        font-size: 1.3rem;
        font-weight: 800;
        color: #2563a8;
        min-width: 2rem;
        line-height: 1;
    }
    .rec-content { flex: 1; }
    .rec-title { font-weight: 700; color: #1a3a5c; font-size: 0.95rem; }
    .rec-detail { color: #64748b; font-size: 0.82rem; margin-top: 0.2rem; }

    /* ── FOOTER ── */
    .app-footer {
        margin-top: 3rem;
        padding: 1.5rem;
        text-align: center;
        background: #f8fafc;
        border-radius: 12px;
        border-top: 2px solid #e2e8f0;
    }
    .app-footer p { color: #94a3b8 !important; font-size: 0.8rem; margin: 0.2rem 0; }

    /* ── TABS ── */
    button[data-baseweb="tab"] { color: #475569 !important; font-weight: 500 !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563a8 !important;
        border-bottom-color: #2563a8 !important;
    }

    /* ── SIDEBAR FILTER LABELS ── */
    .filter-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: rgba(255,255,255,0.5) !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.2rem;
    }

    /* ── PHASE CARDS ── */
    .phase-card {
        background: linear-gradient(135deg, #1a3a5c 0%, #2563a8 100%);
        color: #fff;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }
    .phase-card h4 { color: #fff !important; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
    .phase-card ul { margin: 0; padding-left: 1.2rem; }
    .phase-card li { color: rgba(255,255,255,0.85) !important; font-size: 0.85rem; margin: 0.25rem 0; }

    /* Code blocks */
    code {
        background-color: #1e293b !important;
        color: #7dd3fc !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# 2. HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _html_to_md(text):
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<br\s*/?>', '\n\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text

def insight(text, kind="info"):
    icon = {"info": "💡", "warning": "⚠️", "success": "✅"}.get(kind, "💡")
    md = _html_to_md(text)
    msg = f"{icon} **Analyse & interprétation**\n\n{md}"
    if kind == "warning":
        st.warning(msg)
    elif kind == "success":
        st.success(msg)
    else:
        st.info(msg)

def section_desc(text):
    st.markdown(_html_to_md(text))

def chart_header(title, subtitle=""):
    st.markdown(f"**{title}**")
    if subtitle:
        st.caption(subtitle)

PALETTE_PAYS = px.colors.qualitative.Set2
PALETTE_GENRE = ['#f472b6', '#60a5fa']
PALETTE_DIVERGE = 'RdYlGn'


# ═════════════════════════════════════════════════════════════════════════════
# 3. DATA LOADING
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    df = pd.read_csv('Test.csv')

    traductions = {
        'country': 'pays', 'age_of_respondent': 'age_repondant',
        'gender_of_respondent': 'genre', 'location_type': 'type_zone',
        'cellphone_access': 'acces_telephone', 'job_type': 'type_emploi',
        'education_level': 'niveau_education', 'household_size': 'taille_menage',
        'marital_status': 'statut_matrimonial', 'has_bank_account': 'compte_bancaire',
        'has_mobile_money': 'argent_mobile',
        'has_mobile_money_service': 'service_argent_mobile', 'year': 'annee'
    }
    df.rename(columns=traductions, inplace=True)

    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    df['genre'] = df['genre'].replace({'Male': 'Homme', 'Female': 'Femme'})
    df['type_zone'] = df['type_zone'].replace({'Urban': 'Urbain', 'Rural': 'Rural'})
    df['acces_telephone'] = df['acces_telephone'].replace({'Yes': 'Oui', 'No': 'Non'})
    df['niveau_education'] = df['niveau_education'].replace({
        'No formal education': 'Aucune éducation formelle',
        'Primary education': 'Éducation primaire',
        'Secondary education': 'Secondaire',
        'Vocational/Specialised training': 'Formation professionnelle',
        'Tertiary education': 'Supérieur',
        'Other/Dont know/RTA': 'Autre'
    })
    df['type_emploi'] = df['type_emploi'].replace({
        'Self employed': 'Indépendant',
        'Informally employed': 'Emploi informel',
        'Farming and Fishing': 'Agriculture et Pêche',
        'Remittance Dependent': 'Dépendant des transferts de fonds',
        'Other Income': 'Autre revenu',
        'Formally employed Private': 'Secteur privé formel',
        'No Income': 'Sans revenu',
        'Formally employed Government': 'Secteur public formel',
        'Government Dependent': "Dépendant de l'État",
        'Dont Know/Refuse to answer': 'Inconnu/Refus'
    })
    return df

df = load_data()


# ═════════════════════════════════════════════════════════════════════════════
# 4. SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🌍 FinScope East Africa")
    st.caption("Analyse de l'inclusion financière")

    pages = [
        "🏠 Dashboard",
        "👥 Q1. Démographie",
        "📱 Q2. Inclusion Numérique",
        "💼 Q3. Socio-Économique",
        "👨‍👩‍👧 Q4. Ménages",
        "🔍 Q5. Comportements",
        "📋 Q6. Synthèse Exécutive"
    ]
    selected = st.radio("Navigation", pages, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🔧 Filtres globaux**")

    pays_filter = st.multiselect(
        "Pays", options=sorted(df['pays'].unique()), default=sorted(df['pays'].unique())
    )
    genre_filter = st.multiselect(
        "Genre", options=sorted(df['genre'].unique()), default=sorted(df['genre'].unique())
    )
    zone_filter = st.multiselect(
        "Zone", options=sorted(df['type_zone'].unique()), default=sorted(df['type_zone'].unique())
    )
    age_range = st.slider(
        "Tranche d'âge",
        min_value=int(df['age_repondant'].min()),
        max_value=int(df['age_repondant'].max()),
        value=(16, 65), step=1
    )

    st.markdown("---")
    total = len(df)
    filtre = len(df[
        (df['pays'].isin(pays_filter)) & (df['genre'].isin(genre_filter)) &
        (df['type_zone'].isin(zone_filter)) &
        (df['age_repondant'] >= age_range[0]) & (df['age_repondant'] <= age_range[1])
    ])
    pct_sel = filtre / total * 100 if total > 0 else 0
    st.caption("SÉLECTION ACTIVE")
    st.metric(label="", value=f"{filtre:,}", delta=f"/ {total:,} répondants ({pct_sel:.0f}%)")


# Appliquer filtres
df_filtered = df[
    (df['pays'].isin(pays_filter)) &
    (df['genre'].isin(genre_filter)) &
    (df['type_zone'].isin(zone_filter)) &
    (df['age_repondant'] >= age_range[0]) &
    (df['age_repondant'] <= age_range[1])
].copy()

n = len(df_filtered)

# ═════════════════════════════════════════════════════════════════════════════
# 5. PAGES
# ═════════════════════════════════════════════════════════════════════════════

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
if selected == "🏠 Dashboard":

    st.title("📊 Inclusion Financière & Numérique en Afrique de l'Est")
    st.caption("FinScope East Africa · 2016–2018")
    st.markdown(
        "Cette application explore les données de **10 086 répondants** répartis dans "
        "**4 pays** (Kenya, Rwanda, Tanzanie, Ouganda) pour analyser les dynamiques "
        "d'accès aux services financiers numériques, les inégalités socio-économiques et les leviers "
        "de développement de l'inclusion financière."
    )
    st.markdown("---")

    if n == 0:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    else:
        acces_tel = (df_filtered['acces_telephone'] == 'Oui').sum() / n * 100
        emploi_stable = (df_filtered['type_emploi'].isin(
            ['Secteur privé formel', 'Secteur public formel', 'Indépendant'])).sum() / n * 100
        femmes = (df_filtered['genre'] == 'Femme').sum() / n * 100
        age_moy = df_filtered['age_repondant'].mean()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Répondants sélectionnés", f"{n:,}", f"/ {len(df):,} total")
        with col2:
            st.metric("📱 Accès téléphone", f"{acces_tel:.1f}%", "Inclusion numérique")
        with col3:
            st.metric("💼 Emploi stable", f"{emploi_stable:.1f}%", "Secteur formel + indépendants")
        with col4:
            st.metric("👩 Part femmes", f"{femmes:.1f}%", f"Âge moyen : {age_moy:.0f} ans")

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            chart_header("Distribution par pays", "Nombre de répondants par pays dans la sélection active")
            pays_counts = df_filtered['pays'].value_counts()
            fig = px.bar(
                x=pays_counts.index, y=pays_counts.values,
                labels={'x': 'Pays', 'y': 'Répondants'},
                color_discrete_sequence=PALETTE_PAYS,
                text=pays_counts.values
            )
            fig.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig.update_layout(height=300, showlegend=False, coloraxis_showscale=False,
                              margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="dashboard_pays")

        with col2:
            chart_header("Répartition Genre", "Proportion Hommes / Femmes dans l'échantillon")
            genre_counts = df_filtered['genre'].value_counts()
            fig = px.pie(
                values=genre_counts.values, names=genre_counts.index,
                color_discrete_sequence=PALETTE_GENRE, hole=0.45
            )
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="dashboard_genre")

        col1, col2 = st.columns(2)
        with col1:
            chart_header("Distribution par âge", "Pyramide des âges des répondants")
            fig = px.histogram(
                df_filtered, x='age_repondant', nbins=30,
                labels={'age_repondant': 'Âge', 'count': 'Nombre'},
                color_discrete_sequence=['#2563a8']
            )
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="dashboard_age")

        with col2:
            chart_header("Zone Urbain / Rural", "Origine géographique des répondants")
            zone_counts = df_filtered['type_zone'].value_counts()
            fig = px.pie(
                values=zone_counts.values, names=zone_counts.index,
                color_discrete_sequence=['#34d399', '#fbbf24'], hole=0.45
            )
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="dashboard_zone")

        insight(
            f"<strong>74,9 % de l'échantillon a accès à un téléphone</strong>, mais 2 527 personnes (25,1 %) "
            f"en sont encore exclues — soit potentiellement des millions à l'échelle de la région. "
            f"Le Rwanda affiche le meilleur taux (83,1 %) tandis que la Tanzanie est la plus en retard (60,5 %), "
            f"un écart de 22,6 points entre les deux pays. "
            f"L'écart de genre est de <strong>7,8 points</strong> (hommes 79,5 % vs femmes 71,7 %). "
            f"Ces inégalités structurelles appellent des stratégies différenciées par pays et par groupe cible."
        )


# ─── Q1. DÉMOGRAPHIE ─────────────────────────────────────────────────────────
elif selected == "👥 Q1. Démographie":
    st.title("1️⃣ Répartition démographique des répondants")

    section_desc(
        "Cette section examine la <strong>composition démographique</strong> de l'échantillon : "
        "distribution par pays, par âge et par genre. Ces données de cadrage permettent de "
        "contextualiser toutes les analyses ultérieures et de vérifier la représentativité "
        "de l'échantillon."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            chart_header("📊 Distribution par pays", "Effectifs et parts relatives")
            pays_counts = df_filtered['pays'].value_counts()
            fig = px.bar(
                x=pays_counts.index, y=pays_counts.values,
                labels={'x': 'Pays', 'y': 'Nombre'},
                color_discrete_sequence=PALETTE_PAYS, text=pays_counts.values
            )
            fig.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig.update_layout(height=300, showlegend=False, coloraxis_showscale=False,
                              margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_1")
            for pays, count in pays_counts.items():
                pct = count / n * 100
                st.markdown(f"- **{pays}** : {count:,} répondants ({pct:.1f}%)")

        with col2:
            chart_header("📈 Distribution par âge", "Histogramme avec densité")
            fig = px.histogram(
                df_filtered, x='age_repondant', nbins=30,
                labels={'age_repondant': 'Âge', 'count': 'Nombre'},
                color_discrete_sequence=['#2563a8']
            )
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_2")
            st.markdown(f"""
            - **Moyenne :** {df_filtered['age_repondant'].mean():.1f} ans  
            - **Médiane :** {df_filtered['age_repondant'].median():.0f} ans  
            - **Écart-type :** {df_filtered['age_repondant'].std():.1f} ans
            """)

        with col3:
            chart_header("👥 Distribution par genre", "Répartition Hommes / Femmes")
            genre_counts = df_filtered['genre'].value_counts()
            fig = px.pie(
                values=genre_counts.values, names=genre_counts.index,
                color_discrete_sequence=PALETTE_GENRE, hole=0.5
            )
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_3")
            for genre, count in genre_counts.items():
                pct = count / n * 100
                st.markdown(f"- **{genre}** : {count:,} ({pct:.1f}%)")

        insight(
            "Le Rwanda (37,1 %) et la Tanzanie (28,1 %) représentent à eux deux <strong>65 % de l'échantillon</strong> "
            "— les résultats sont donc plus représentatifs de ces deux pays. "
            "L'âge médian est de <strong>35 ans</strong> (moyenne 38,3 ans) : la population est jeune et active, "
            "ce qui est un levier majeur pour l'adoption du mobile banking. "
            "Les femmes représentent <strong>58 %</strong> de l'échantillon (5 847 personnes) — "
            "tout programme d'inclusion doit en priorité cibler ce groupe majoritaire mais sous-servi."
        )


# ─── Q2. INCLUSION NUMÉRIQUE ─────────────────────────────────────────────────
elif selected == "📱 Q2. Inclusion Numérique":
    st.title("2️⃣ État de l'inclusion numérique — Accès au téléphone")

    section_desc(
        "L'accès au téléphone portable est le <strong>premier maillon</strong> de l'inclusion "
        "financière numérique. Sans cet accès, les services de mobile money, de paiement "
        "électronique ou de crédit digital sont inaccessibles. Cette section analyse les disparités "
        "selon le pays, la zone géographique (urbain/rural) et le genre."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        acces_global = (df_filtered['acces_telephone'] == 'Oui').sum() / n * 100

        kc1, kc2, kc3 = st.columns(3)
        kc1.metric("📱 Accès téléphone global", f"{acces_global:.1f}%")
        kc2.metric("✅ Personnes connectées", f"{(df_filtered['acces_telephone']=='Oui').sum():,}")
        kc3.metric("⚠️ Sans accès", f"{(df_filtered['acces_telephone']=='Non').sum():,}")

        col1, col2 = st.columns(2)

        with col1:
            chart_header("📱 Accès par pays", "Proportion Oui/Non par pays (barres empilées 100%)")
            pays_tel = pd.crosstab(df_filtered['pays'], df_filtered['acces_telephone'], normalize='index') * 100
            fig = px.bar(
                pays_tel.reset_index().melt(id_vars='pays', var_name='Accès', value_name='%'),
                x='pays', y='%', color='Accès', barmode='stack',
                color_discrete_sequence=['#f87171', '#34d399']
            )
            fig.update_layout(height=350, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_4")
            st.markdown("**Taux d'accès par pays :**")
            for pays in sorted(df_filtered['pays'].unique()):
                sub = df_filtered[df_filtered['pays'] == pays]
                if len(sub) > 0:
                    pct = (sub['acces_telephone'] == 'Oui').sum() / len(sub) * 100
                    st.markdown(f"- **{pays}** : {pct:.1f}%")

        with col2:
            chart_header("🏙️ Urbain vs Rural", "Disparité ville / campagne dans l'accès numérique")
            zone_tel = pd.crosstab(df_filtered['type_zone'], df_filtered['acces_telephone'], normalize='index') * 100
            fig = px.bar(
                zone_tel.reset_index().melt(id_vars='type_zone', var_name='Accès', value_name='%'),
                x='type_zone', y='%', color='Accès', barmode='group',
                color_discrete_sequence=['#f87171', '#34d399']
            )
            fig.update_layout(height=350, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_5")
            st.markdown("**Taux d'accès par zone :**")
            for zone in sorted(df_filtered['type_zone'].unique()):
                sub = df_filtered[df_filtered['type_zone'] == zone]
                if len(sub) > 0:
                    pct = (sub['acces_telephone'] == 'Oui').sum() / len(sub) * 100
                    st.markdown(f"- **{zone}** : {pct:.1f}%")

        # Accès par genre
        st.markdown("---")
        chart_header("👥 Accès au téléphone par genre", "Inégalité de genre dans l'accès numérique")
        genre_tel = pd.crosstab(df_filtered['genre'], df_filtered['acces_telephone'], normalize='index') * 100
        fig = px.bar(
            genre_tel.reset_index().melt(id_vars='genre', var_name='Accès', value_name='%'),
            x='genre', y='%', color='Accès', barmode='group',
            color_discrete_sequence=['#f87171', '#34d399']
        )
        fig.update_layout(height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True, key="chart_6")

        # Accès par tranche d'âge
        df_filtered['tranche_age'] = pd.cut(
            df_filtered['age_repondant'],
            bins=[0, 25, 35, 45, 55, 100],
            labels=['16-25', '26-35', '36-45', '46-55', '56+']
        )
        age_tel = df_filtered.groupby('tranche_age').apply(
            lambda x: (x['acces_telephone'] == 'Oui').sum() / len(x) * 100 if len(x) > 0 else 0
        ).reset_index()
        age_tel.columns = ['Tranche', 'Accès (%)']
        chart_header("📊 Accès par tranche d'âge", "Évolution du taux d'accès selon l'âge")
        fig = px.line(age_tel, x='Tranche', y='Accès (%)', markers=True,
                      color_discrete_sequence=['#2563a8'])
        fig.update_layout(height=280, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True, key="chart_7")

        insight(
            "<strong>Résultat contre-intuitif :</strong> les zones rurales affichent un meilleur taux d'accès "
            "(77,5 %) que les zones urbaines (71,0 %), soit un écart de +6,5 points en faveur du rural. "
            "Cela peut s'expliquer par un effet de partage d'appareils au sein des communautés rurales. "
            "En revanche, <strong>l'écart de genre est réel et documenté</strong> : 79,5 % des hommes ont un téléphone "
            "contre 71,7 % des femmes (−7,8 points). Avec 5 847 femmes dans l'échantillon, "
            "cela représente ~456 femmes supplémentaires sans accès par rapport aux hommes. "
            "La Tanzanie (60,5 %) nécessite une intervention prioritaire en infrastructures numériques.",
            kind="warning"
        )


# ─── Q3. SOCIO-ÉCONOMIQUE ────────────────────────────────────────────────────
elif selected == "💼 Q3. Socio-Économique":
    st.title("3️⃣ Profil socio-économique des populations")

    section_desc(
        "Cette section croise les <strong>niveaux d'éducation</strong> et les <strong>types d'emploi</strong> "
        "pour cartographier le profil socio-économique des répondants. L'éducation et l'emploi sont "
        "deux déterminants majeurs de l'accès aux services financiers formels."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        chart_header("🔥 Heatmap Éducation × Emploi", "Nombre de répondants à l'intersection de chaque combinaison")
        crosstab = pd.crosstab(df_filtered['niveau_education'], df_filtered['type_emploi'])
        if len(crosstab) > 0:
            fig = go.Figure(data=go.Heatmap(
                z=crosstab.values,
                x=crosstab.columns,
                y=crosstab.index,
                colorscale='YlOrRd',
                text=crosstab.values,
                texttemplate='%{text}',
                textfont={"size": 9}
            ))
            fig.update_layout(
                height=500, xaxis_tickangle=-40,
                margin=dict(t=20, b=80),
                xaxis_title="Type d'emploi",
                yaxis_title="Niveau d'éducation"
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_8")

        st.markdown("---")
        chart_header("📊 Distribution emploi par éducation", "Parts relatives (%) de chaque type d'emploi selon le niveau d'éducation")
        crosstab_pct = pd.crosstab(df_filtered['niveau_education'], df_filtered['type_emploi'], normalize='index') * 100
        fig = px.bar(
            crosstab_pct.reset_index().melt(id_vars='niveau_education', var_name='Emploi', value_name='%'),
            x='niveau_education', y='%', color='Emploi', barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=450, xaxis_tickangle=-35, margin=dict(t=10, b=80))
        st.plotly_chart(fig, use_container_width=True, key="chart_9")

        # Stats rapides
        col1, col2 = st.columns(2)
        with col1:
            edu_counts = df_filtered['niveau_education'].value_counts()
            st.markdown("**Répartition par niveau d'éducation :**")
            for edu, cnt in edu_counts.items():
                st.markdown(f"- **{edu}** : {cnt:,} ({cnt/n*100:.1f}%)")
        with col2:
            emp_counts = df_filtered['type_emploi'].value_counts().head(6)
            st.markdown("**Top 6 types d'emploi :**")
            for emp, cnt in emp_counts.items():
                st.markdown(f"- **{emp}** : {cnt:,} ({cnt/n*100:.1f}%)")

        insight(
            "L'éducation est le <strong>principal déterminant de l'emploi formel</strong> : "
            "57,1 % des personnes ayant une formation professionnelle occupent un emploi stable, "
            "contre seulement <strong>23,7 % pour ceux sans éducation formelle</strong> (18,2 % de l'échantillon, soit 1 836 personnes). "
            "Chez les sans-diplôme, 31,0 % travaillent dans l'agriculture/pêche et 23,4 % dans l'emploi informel — "
            "deux secteurs à revenus irréguliers qui bloquent l'accès au crédit structuré. "
            "À l'inverse, les diplômés du supérieur (seulement 4,9 % de l'échantillon) accèdent au secteur privé formel (14,2 %) "
            "et public (9,1 %), ce qui crée une fracture économique profonde."
        )


# ─── Q4. MÉNAGES ─────────────────────────────────────────────────────────────
elif selected == "👨‍👩‍👧 Q4. Ménages":
    st.title("4️⃣ Taille des ménages et taux de dépendance")

    section_desc(
        "La <strong>taille du ménage</strong> influence directement la pression financière sur chaque "
        "répondant. Un ménage de grande taille avec un seul revenu implique un taux de dépendance "
        "élevé, ce qui réduit la capacité d'épargne et limite l'accès aux produits financiers. "
        "Cette section analyse comment la composition familiale varie selon les pays et l'âge."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        taille_moy = df_filtered['taille_menage'].mean()
        taille_med = df_filtered['taille_menage'].median()
        corr = df_filtered['age_repondant'].corr(df_filtered['taille_menage'])

        col1, col2, col3 = st.columns(3)
        col1.metric("👨‍👩‍👧 Taille moyenne", f"{taille_moy:.1f} personnes")
        col2.metric("📊 Taille médiane", f"{taille_med:.0f} personnes")
        col3.metric("📈 Corrélation Âge/Taille", f"{corr:.3f}",
                    "Positive = ménages plus grands avec l'âge")

        col1, col2 = st.columns(2)

        with col1:
            chart_header("📦 Distribution par pays (Boxplot)", "Variabilité et médiane de la taille selon le pays")
            fig = px.box(
                df_filtered, x='pays', y='taille_menage',
                labels={'taille_menage': 'Personnes dans le ménage'},
                color='pays', color_discrete_sequence=PALETTE_PAYS
            )
            fig.update_layout(height=380, showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_10")

        with col2:
            chart_header("📈 Âge vs Taille du ménage", "Nuage de points avec régression linéaire (OLS)")
            sample = df_filtered.sample(n=min(800, n), random_state=42)
            _x = sample['age_repondant'].dropna()
            _y = sample['taille_menage'].dropna()
            _common = sample[['age_repondant', 'taille_menage']].dropna()
            _coef = np.polyfit(_common['age_repondant'], _common['taille_menage'], 1)
            _x_range = np.linspace(_common['age_repondant'].min(), _common['age_repondant'].max(), 100)
            _y_range = np.polyval(_coef, _x_range)
            fig = px.scatter(
                sample, x='age_repondant', y='taille_menage',
                opacity=0.4,
                labels={'age_repondant': 'Âge du répondant', 'taille_menage': 'Taille du ménage'},
                color_discrete_sequence=['#2563a8']
            )
            fig.add_scatter(x=_x_range, y=_y_range, mode='lines', name='Tendance',
                            line=dict(color='#e74c3c', width=2))
            fig.update_layout(height=380, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_11")

        # Distribution taille
        chart_header("📊 Distribution de la taille des ménages", "Fréquence de chaque taille de ménage")
        fig = px.histogram(
            df_filtered, x='taille_menage', nbins=20,
            labels={'taille_menage': 'Taille du ménage', 'count': 'Nombre'},
            color_discrete_sequence=['#6366f1']
        )
        fig.update_layout(height=280, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True, key="chart_12")

        insight(
            f"<strong>Disparités majeures entre pays :</strong> l'Ouganda a les ménages les plus grands "
            f"(moyenne 5,0 personnes) et la Tanzanie les plus petits (2,3 personnes) — un rapport de 1 à 2. "
            f"11,9 % des ménages comptent 7 personnes ou plus, créant une forte pression financière par individu. "
            f"La corrélation âge/taille est <strong>négative (−0,118)</strong> : les personnes plus âgées gèrent des ménages "
            f"plus petits (effet cycle de vie — les enfants quittent le foyer). "
            f"Pour un décideur, cela signifie que les programmes de micro-crédit doivent intégrer "
            f"la taille du ménage comme variable de scoring, pas seulement le revenu individuel."
        )


# ─── Q5. COMPORTEMENTS ───────────────────────────────────────────────────────
elif selected == "🔍 Q5. Comportements":
    st.title("5️⃣ Analyse comportementale — Patterns & Corrélations")

    section_desc(
        "Cette section explore les <strong>déterminants comportementaux</strong> de l'accès au téléphone "
        "(proxy de l'inclusion numérique) en croisant les facteurs éducatifs, professionnels, "
        "de genre et de composition familiale. Elle se termine par une matrice de corrélation "
        "entre les principales variables quantitatives."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📚 Éducation", "💼 Emploi", "👥 Genre", "🏠 Ménage", "🔥 Corrélations"
        ])

        with tab1:
            st.markdown("**Objectif :** Mesurer si un niveau d'éducation plus élevé est associé à un meilleur accès au téléphone.")
            edu_tel = df_filtered.groupby('niveau_education').apply(
                lambda x: (x['acces_telephone'] == 'Oui').sum() / len(x) * 100 if len(x) > 0 else 0
            ).reset_index()
            edu_tel.columns = ['Éducation', 'Accès (%)']
            edu_tel = edu_tel.sort_values('Accès (%)', ascending=True)
            fig = px.bar(
                edu_tel, x='Accès (%)', y='Éducation', orientation='h',
                color='Accès (%)', color_continuous_scale='Viridis',
                text='Accès (%)'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=350, coloraxis_showscale=False, margin=dict(t=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_13")
            insight(
                "Le gradient éducation → accès numérique est <strong>net et chiffré</strong> : "
                "formation professionnelle (95,8 %), supérieur (93,5 %), secondaire (84,4 %), primaire (74,6 %), "
                "sans éducation (57,2 %). "
                "L'écart entre le bas et le haut de l'échelle est de <strong>38,6 points</strong>. "
                "Décision prioritaire : chaque année d'éducation supplémentaire augmente significativement "
                "la probabilité d'inclusion numérique et financière. "
                "Investir dans l'éducation de base est donc aussi un investissement dans l'inclusion financière."
            )

        with tab2:
            st.markdown("**Objectif :** Comparer l'accès numérique entre emploi formel (stable) et emploi précaire/informel.")
            emplois_stables = ['Secteur privé formel', 'Secteur public formel', 'Indépendant']
            df_filtered['emploi_statut'] = df_filtered['type_emploi'].apply(
                lambda x: 'Emploi formel / stable' if x in emplois_stables else 'Emploi précaire / informel'
            )
            emp_tel = df_filtered.groupby('emploi_statut').apply(
                lambda x: (x['acces_telephone'] == 'Oui').sum() / len(x) * 100 if len(x) > 0 else 0
            ).reset_index()
            emp_tel.columns = ['Statut', 'Accès (%)']
            fig = px.bar(
                emp_tel, x='Statut', y='Accès (%)',
                color='Accès (%)', color_continuous_scale='RdYlGn',
                text='Accès (%)'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=350, coloraxis_showscale=False, margin=dict(t=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_14")
            insight(
                "<strong>Résultat surprenant :</strong> l'écart entre emploi formel (75,5 %) et emploi précaire (74,7 %) "
                "n'est que de <strong>0,8 point</strong> — quasi nul. "
                "Le type d'emploi seul n'explique donc pas l'exclusion numérique. "
                "C'est la combinaison emploi précaire + faible éducation + grand ménage qui crée la vulnérabilité. "
                "Pour les décideurs : éviter les programmes d'inclusion qui ciblent uniquement le statut d'emploi "
                "— une approche multi-critères (éducation + emploi + localisation) sera bien plus efficace.",
                kind="warning"
            )

        with tab3:
            st.markdown("**Objectif :** Quantifier l'écart de genre dans l'accès au téléphone et visualiser sa distribution.")
            genre_tel = df_filtered.groupby('genre').apply(
                lambda x: (x['acces_telephone'] == 'Oui').sum() / len(x) * 100 if len(x) > 0 else 0
            ).reset_index()
            genre_tel.columns = ['Genre', 'Accès (%)']
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    values=genre_tel['Accès (%)'], names=genre_tel['Genre'],
                    color_discrete_sequence=PALETTE_GENRE, hole=0.5
                )
                fig.update_layout(height=320)
                st.plotly_chart(fig, use_container_width=True, key="chart_15")
            with col2:
                fig = px.bar(
                    genre_tel, x='Genre', y='Accès (%)',
                    color='Genre', color_discrete_sequence=PALETTE_GENRE, text='Accès (%)'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(height=320, showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key="chart_16")
            insight(
                "Hommes : 79,5 % d'accès — Femmes : 71,7 % d'accès → <strong>écart de 7,8 points</strong>. "
                "Avec 5 847 femmes dans l'échantillon (58 % du total), cet écart représente environ "
                "<strong>456 femmes supplémentaires sans accès</strong> par rapport aux hommes à proportion égale. "
                "Ces femmes exclues du numérique sont automatiquement exclues du mobile money, des transferts "
                "d'argent et du crédit digital. "
                "L'effet de cumul est le plus dangereux : une femme sans téléphone + sans éducation + en emploi informel "
                "fait face à une triple barrière d'exclusion financière.",
                kind="warning"
            )

        with tab4:
            st.markdown("**Objectif :** Vérifier si la taille du ménage influence l'accès au téléphone (pression financière vs réseau de partage).")
            df_filtered['cat_menage'] = pd.cut(
                df_filtered['taille_menage'], bins=[0, 3, 6, 10, 100],
                labels=['Petit (1–3)', 'Moyen (4–6)', 'Grand (7–10)', 'Très grand (11+)']
            )
            menage_tel = df_filtered.groupby('cat_menage').apply(
                lambda x: (x['acces_telephone'] == 'Oui').sum() / len(x) * 100 if len(x) > 0 else 0
            ).reset_index()
            menage_tel.columns = ['Catégorie', 'Accès (%)']
            fig = px.bar(
                menage_tel, x='Catégorie', y='Accès (%)',
                color='Accès (%)', color_continuous_scale='RdYlGn', text='Accès (%)'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=350, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, key="chart_17")
            insight(
                "<strong>Résultat inattendu :</strong> les ménages moyens (4–6 personnes) ont le meilleur taux d'accès "
                "(79,0 %), devant les petits ménages (71,1 %). "
                "Explication probable : dans les ménages intermédiaires, plusieurs membres travaillent et "
                "se partagent les coûts d'équipement. "
                "Les très grands ménages (11+ personnes) affichent le pire taux (67,6 %) car la pression "
                "financière par individu dépasse l'effet de partage. "
                "Implication opérationnelle : les programmes de subvention d'appareils mobiles devraient "
                "cibler en priorité les ménages de 7 personnes ou plus (11,9 % de l'échantillon)."
            )

        with tab5:
            st.markdown("**Objectif :** Identifier les corrélations linéaires entre l'âge, la taille du ménage et l'accès au téléphone.")
            df_num = df_filtered.copy()
            df_num['acces_tel_num'] = (df_num['acces_telephone'] == 'Oui').astype(int)
            corr = df_num[['age_repondant', 'taille_menage', 'acces_tel_num']].corr()
            labels = ['Âge', 'Taille ménage', 'Accès téléphone']
            fig = go.Figure(data=go.Heatmap(
                z=corr.values, x=labels, y=labels,
                colorscale='RdBu', zmid=0,
                text=corr.values.round(3), texttemplate='%{text}',
                textfont={"size": 12}
            ))
            fig.update_layout(height=380, margin=dict(t=20))
            st.plotly_chart(fig, use_container_width=True, key="chart_18")
            insight(
                "Les trois corrélations linéaires sont <strong>toutes faibles</strong> (valeurs proches de 0). "
                "Corrélation âge/taille ménage : −0,118 (légèrement négative — les plus âgés ont des ménages plus petits). "
                "Corrélation âge/accès et taille/accès : quasi nulles. "
                "<strong>Conclusion décisionnelle majeure :</strong> aucun de ces facteurs seul ne prédit l'exclusion. "
                "C'est leur combinaison (femme + sans éducation + emploi informel + grand ménage) qui crée la vulnérabilité. "
                "Les modèles de scoring pour le micro-crédit ou les programmes d'aide doivent impérativement "
                "intégrer plusieurs variables simultanément, pas une seule dimension."
            )


# ─── Q6. SYNTHÈSE EXÉCUTIVE ──────────────────────────────────────────────────
elif selected == "📋 Q6. Synthèse Exécutive":
    st.title("6️⃣ Synthèse Exécutive & Recommandations Stratégiques")

    section_desc(
        "Cette synthèse consolide les <strong>principaux enseignements</strong> des analyses précédentes "
        "et formule des recommandations actionnables pour les décideurs, ONG et institutions "
        "financières souhaitant améliorer l'inclusion financière numérique en Afrique de l'Est."
    )

    if n == 0:
        st.warning("Aucune donnée pour les filtres sélectionnés.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 KPIs", "🔴 Profils de risque", "💡 Recommandations", "📅 Plan d'action"])

        with tab1:
            st.markdown("**Vue d'ensemble des indicateurs clés sur la sélection active.**")
            acces_tel = (df_filtered['acces_telephone'] == 'Oui').sum() / n * 100
            emploi = (df_filtered['type_emploi'].isin(
                ['Secteur privé formel', 'Secteur public formel', 'Indépendant'])).sum() / n * 100
            taille = df_filtered['taille_menage'].mean()
            femmes = (df_filtered['genre'] == 'Femme').sum() / n * 100
            age_moy = df_filtered['age_repondant'].mean()

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("📱 Accès téléphone", f"{acces_tel:.1f}%")
            col2.metric("💼 Emploi stable", f"{emploi:.1f}%")
            col3.metric("👨‍👩‍👧 Taille moy. ménage", f"{taille:.1f}")
            col4.metric("👩 Part femmes", f"{femmes:.1f}%")
            col5.metric("🎂 Âge moyen", f"{age_moy:.0f} ans")

            st.markdown("---")
            # Accès par pays — radar-like bar
            chart_header("📊 Comparaison des pays sur les KPIs clés")
            pays_kpis = []
            for pays in sorted(df_filtered['pays'].unique()):
                sub = df_filtered[df_filtered['pays'] == pays]
                if len(sub) > 0:
                    pays_kpis.append({
                        'Pays': pays,
                        'Accès téléphone (%)': (sub['acces_telephone'] == 'Oui').sum() / len(sub) * 100,
                        'Emploi stable (%)': sub['type_emploi'].isin(
                            ['Secteur privé formel', 'Secteur public formel', 'Indépendant']).sum() / len(sub) * 100,
                        'Part femmes (%)': (sub['genre'] == 'Femme').sum() / len(sub) * 100,
                    })
            df_kpis = pd.DataFrame(pays_kpis)
            fig = px.bar(
                df_kpis.melt(id_vars='Pays', var_name='Indicateur', value_name='%'),
                x='Pays', y='%', color='Indicateur', barmode='group',
                color_discrete_sequence=['#2563a8', '#22c55e', '#f472b6']
            )
            fig.update_layout(height=380, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_19")

        with tab2:
            st.markdown("""
            Les **profils de vulnérabilité** permettent de cibler les interventions sur les populations
            les plus exposées à l'exclusion financière.
            """)

            ultra_vuln = df_filtered[
                (df_filtered['genre'] == 'Femme') &
                (df_filtered['niveau_education'] == 'Aucune éducation formelle') &
                (df_filtered['type_emploi'].isin(['Emploi informel', 'Sans revenu']))
            ]
            tres_vuln = df_filtered[
                (df_filtered['niveau_education'] == 'Aucune éducation formelle') |
                (df_filtered['type_emploi'] == 'Sans revenu')
            ]
            vuln_mod = df_filtered[
                (df_filtered['type_emploi'].isin(['Agriculture et Pêche', 'Dépendant des transferts de fonds'])) &
                (df_filtered['acces_telephone'] == 'Non')
            ]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.error(f"🔴 **Ultra-vulnérables**\n\n**{len(ultra_vuln):,}** personnes ({len(ultra_vuln)/n*100:.1f}%)\n\nFemmes + sans éducation + emploi informel/nul")
            with col2:
                st.warning(f"🟠 **Très vulnérables**\n\n**{len(tres_vuln):,}** personnes ({len(tres_vuln)/n*100:.1f}%)\n\nSans éducation formelle OU sans revenu")
            with col3:
                st.warning(f"🟡 **Vulnérabilité modérée**\n\n**{len(vuln_mod):,}** personnes ({len(vuln_mod)/n*100:.1f}%)\n\nAgriculture/transferts ET sans téléphone")

            insight(
                "Sur l'ensemble de l'échantillon (10 086 personnes) : "
                "<strong>318 ultra-vulnérables (3,2 %)</strong> — femmes sans éducation en emploi informel/nul — "
                "nécessitent une intervention immédiate et multidimensionnelle (éducation + revenu + numérique simultanément). "
                "<strong>~2 110 très vulnérables (20,9 %)</strong> — sans éducation formelle ou sans revenu — "
                "nécessitent des programmes structurels sur 6 à 12 mois. "
                "L'exclusion n'est donc pas marginale : elle est <strong>systémique</strong>. "
                "Les ultra-vulnérables doivent être la priorité n°1 car leurs barrières sont cumulées et "
                "aucun programme mono-dimensionnel ne peut les atteindre efficacement.",
                kind="warning"
            )

        with tab3:
            st.markdown("**8 recommandations stratégiques issues des analyses, classées par priorité d'impact.**")

            recs = [
                ("🌐 Universaliser l'accès numérique", "Déployer des infrastructures réseau rural et subventionner les smartphones dans les zones sous-desservies. Horizon : 2–3 ans."),
                ("📚 Éducation financière ciblée femmes", "Programmes d'alphabétisation financière et numérique prioritairement dédiés aux femmes rurales sans éducation formelle. Horizon : 1–3 ans."),
                ("📊 Inclusion financière par paliers", "Proposer des produits financiers simplifiés (épargne mobile, micro-crédit) accessibles sans compte bancaire classique. Continu."),
                ("💳 Crédit adapté à l'emploi informel", "Développer des offres de micro-crédit avec scoring alternatif (historique mobile money) pour les travailleurs informels. Horizon : 1–2 ans."),
                ("🌍 Approche différenciée par pays", "Adapter les stratégies aux spécificités de chaque pays (taux d'accès, structure économique, régulation). Continu."),
                ("🛡️ Protection contre la surendette", "Mettre en place des plafonds et une éducation au risque pour éviter les travers de l'hypercrédit dans les populations vulnérables."),
                ("👦 Programme dédié aux jeunes (16–35 ans)", "Créer des offres jeunes (épargne, premier crédit) pour capitaliser sur la population jeune et numériquement agile."),
                ("🏥 Micro-assurance contre les chocs", "Développer des micro-assurances (santé, récolte) distribuées via mobile pour renforcer la résilience des ménages. Horizon : 2025+.")
            ]

            for i, (titre, detail) in enumerate(recs, 1):
                st.markdown(f"**{i}. {titre}**")
                st.caption(detail)
                st.divider()

        with tab4:
            st.markdown("**Feuille de route de mise en œuvre des recommandations sur 3 ans.**")

            phases = {
                "⏱️ Phase 1 — Court terme (0–6 mois)": {
                    "color": "#dc2626",
                    "actions": [
                        "Cartographie des zones blanches numériques",
                        "Lancement des programmes d'éducation financière femmes",
                        "Cadre réglementaire minimal pour le mobile money"
                    ]
                },
                "📊 Phase 2 — Moyen terme (6–18 mois)": {
                    "color": "#f59e0b",
                    "actions": [
                        "Déploiement des produits financiers par paliers",
                        "Lancement micro-crédit scoring mobile",
                        "Stratégies différenciées par pays"
                    ]
                },
                "🚀 Phase 3 — Long terme (18–36 mois)": {
                    "color": "#2563a8",
                    "actions": [
                        "Programme dédié aux jeunes 16–35 ans",
                        "Déploiement micro-assurance (santé, récolte)",
                        "Mesure d'impact et ajustement des programmes"
                    ]
                },
                "🎯 Phase 4 — Cibles à 3 ans": {
                    "color": "#22c55e",
                    "actions": [
                        "95% de la population avec accès à un téléphone",
                        "70% avec un compte mobile money actif",
                        "50% avec accès à un produit de crédit formel"
                    ]
                }
            }

            for phase, data in phases.items():
                with st.expander(phase, expanded=True):
                    for action in data['actions']:
                        st.markdown(f"✓ {action}")

            insight(
                "<strong>Le Rwanda est le pays le mieux positionné</strong> pour déployer rapidement des services fintech "
                "(83,1 % d'accès téléphone, économie formalisée) — c'est le marché pilote idéal. "
                "La Tanzanie doit d'abord investir dans l'infrastructure réseau avant tout produit financier (60,5 % seulement). "
                "L'Ouganda, avec les ménages les plus grands (5,0 personnes en moyenne), nécessite "
                "des produits adaptés à la gestion collective des finances familiales. "
                "Cible à 3 ans : <strong>passer de 74,9 % à 85 %+ d'accès téléphone</strong>, "
                "réduire l'écart de genre sous 3 points, et amener 50 % des travailleurs informels "
                "vers un produit de micro-crédit avec scoring alternatif. "
                "Un suivi d'impact trimestriel par pays est indispensable pour ajuster les allocations budgétaires.",
                kind="success"
            )


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📊 **FinScope East Africa** — Application EDA sur l'Inclusion Financière Numérique")
st.caption("Données : 10 086 répondants · 4 pays (Kenya, Rwanda, Tanzanie, Ouganda) · 2016–2018 · Développé avec Streamlit · Plotly · Pandas")
