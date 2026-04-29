import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import init_db, insert_reponse, get_all_reponses, get_stats

# ===== CONFIG =====
st.set_page_config(
    page_title="DataCollect INF232 - NOUBISSI Yannolf",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS PERSONNALISÉ =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* Fond général */
    .stApp {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #2a2a2a;
    }

    /* Titres */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
    }

    /* Cartes métriques */
    [data-testid="metric-container"] {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Boutons */
    .stButton > button {
        background-color: #c8402a;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        padding: 0.6rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #a83520;
        transform: translateY(-1px);
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        color: #c8402a !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #555;
        font-size: 12px;
        border-top: 1px solid #2a2a2a;
        margin-top: 2rem;
    }

    /* Badge succès */
    .success-box {
        background-color: #0d2e1a;
        border: 1px solid #1a7a45;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #4caf7d;
        margin-top: 1rem;
    }

    /* Divider */
    hr {
        border-color: #2a2a2a !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== INIT DB =====
init_db()

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## 📊 DataCollect")
    st.markdown("**INF232 EC2**")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["📋 Formulaire", "📈 Analyse", "🗃️ Données brutes"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px; color:#555;'>
        <strong style='color:#888'>Étudiant</strong><br/>
        NOUBISSI Yannolf<br/>
        <strong style='color:#888'>Matricule</strong><br/>
        24G2179<br/>
        <strong style='color:#888'>Cours</strong><br/>
        INF232 EC2<br/>
        <strong style='color:#888'>SGBD</strong><br/>
        SQLite
    </div>
    """, unsafe_allow_html=True)

# ===== PAGE FORMULAIRE =====
if page == "📋 Formulaire":
    st.markdown("# Collecte de *données* en ligne")
    st.markdown("Remplissez le formulaire ci-dessous. Vos réponses alimentent l'analyse descriptive en temps réel.")
    st.markdown("---")

    with st.form("formulaire_collecte", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nom = st.text_input("👤 Nom complet *", placeholder="Ex: Jean Dupont")
            age = st.number_input("🎂 Âge *", min_value=10, max_value=100, value=20)
            genre = st.selectbox("⚥ Genre *", ["— Sélectionner —", "Masculin", "Féminin", "Autre"])
            niveau = st.selectbox("🎓 Niveau d'études *", [
                "— Sélectionner —", "Primaire", "Secondaire",
                "Licence (L1-L3)", "Master (M1-M2)", "Doctorat"
            ])

        with col2:
            secteur = st.selectbox("💼 Secteur d'activité *", [
                "— Sélectionner —", "Informatique / Tech", "Santé",
                "Éducation", "Commerce", "Agriculture", "Finance / Banque", "Autre"
            ])
            revenu = st.number_input("💰 Revenu mensuel (FCFA)", min_value=0, value=0, step=5000)
            satisfaction = st.slider("⭐ Satisfaction générale *", min_value=1, max_value=5, value=3,
                                     help="1 = Très insatisfait | 5 = Très satisfait")
            st.caption(f"Niveau sélectionné : {'⭐' * satisfaction}")

        commentaire = st.text_area("💬 Commentaire libre", placeholder="Partagez votre avis, suggestion ou observation...", height=80)

        submitted = st.form_submit_button("✅ Soumettre ma réponse")

        if submitted:
            # Validation
            erreurs = []
            if not nom.strip():
                erreurs.append("Le nom est obligatoire.")
            if genre == "— Sélectionner —":
                erreurs.append("Veuillez sélectionner un genre.")
            if niveau == "— Sélectionner —":
                erreurs.append("Veuillez sélectionner un niveau d'études.")
            if secteur == "— Sélectionner —":
                erreurs.append("Veuillez sélectionner un secteur.")

            if erreurs:
                for e in erreurs:
                    st.error(e)
            else:
                insert_reponse(
                    nom.strip(), age, genre, niveau, secteur,
                    revenu if revenu > 0 else None,
                    satisfaction, commentaire.strip()
                )
                st.success(f"✅ Réponse de **{nom}** enregistrée avec succès !")
                st.balloons()

# ===== PAGE ANALYSE =====
elif page == "📈 Analyse":
    st.markdown("# Analyse *descriptive*")
    st.markdown("Statistiques calculées en temps réel sur toutes les réponses collectées.")
    st.markdown("---")

    stats = get_stats()

    if stats["total"] == 0:
        st.info("📭 Aucune donnée collectée pour l'instant. Commencez par remplir le formulaire !")
    else:
        # Métriques
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Total réponses", stats["total"])
        c2.metric("🎂 Âge moyen", f"{stats['age_moy']} ans" if stats['age_moy'] else "—")
        c3.metric("⭐ Satisfaction moyenne", f"{stats['sat_moy']} / 5" if stats['sat_moy'] else "—")
        c4.metric("💰 Revenu moyen", f"{int(stats['rev_moy']):,} FCFA".replace(",", " ") if stats['rev_moy'] else "—")

        st.markdown("---")

        # Graphiques
        col1, col2 = st.columns(2)

        with col1:
            if not stats["genre"].empty:
                fig_genre = px.pie(
                    stats["genre"], values="count", names="genre",
                    title="Répartition par genre",
                    color_discrete_sequence=["#c8402a", "#e8b84b", "#888780"],
                    hole=0.4
                )
                fig_genre.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#f0f0f0"
                )
                st.plotly_chart(fig_genre, use_container_width=True)

        with col2:
            if not stats["secteur"].empty:
                fig_secteur = px.bar(
                    stats["secteur"], x="count", y="secteur",
                    orientation="h", title="Répartition par secteur",
                    color="count",
                    color_continuous_scale=["#1a1a1a", "#c8402a"]
                )
                fig_secteur.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#f0f0f0",
                    showlegend=False,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_secteur, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            if not stats["satisfaction"].empty:
                fig_sat = px.bar(
                    stats["satisfaction"], x="satisfaction", y="count",
                    title="Distribution de satisfaction",
                    labels={"satisfaction": "Note (1-5)", "count": "Nombre"},
                    color="satisfaction",
                    color_continuous_scale=["#c8402a", "#e8b84b", "#1D9E75"]
                )
                fig_sat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#f0f0f0",
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_sat, use_container_width=True)

        with col4:
            if not stats["niveau"].empty:
                fig_niv = px.pie(
                    stats["niveau"], values="count", names="niveau_etude",
                    title="Répartition par niveau d'études",
                    color_discrete_sequence=px.colors.sequential.Reds_r
                )
                fig_niv.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#f0f0f0"
                )
                st.plotly_chart(fig_niv, use_container_width=True)

        if st.button("↻ Actualiser les statistiques"):
            st.rerun()

# ===== PAGE DONNÉES BRUTES =====
elif page == "🗃️ Données brutes":
    st.markdown("# Données *brutes*")
    st.markdown("Toutes les réponses enregistrées dans la base de données SQLite.")
    st.markdown("---")

    df = get_all_reponses()

    if df.empty:
        st.info("📭 Aucune donnée collectée pour l'instant.")
    else:
        st.markdown(f"**{len(df)} réponse(s) au total**")

        # Filtre
        col1, col2 = st.columns(2)
        with col1:
            filtre_genre = st.multiselect("Filtrer par genre", options=df["genre"].unique())
        with col2:
            filtre_secteur = st.multiselect("Filtrer par secteur", options=df["secteur"].unique())

        df_filtered = df.copy()
        if filtre_genre:
            df_filtered = df_filtered[df_filtered["genre"].isin(filtre_genre)]
        if filtre_secteur:
            df_filtered = df_filtered[df_filtered["secteur"].isin(filtre_secteur)]

        st.dataframe(
            df_filtered[["id", "nom", "age", "genre", "niveau_etude", "secteur", "revenu_mensuel", "satisfaction", "created_at"]],
            use_container_width=True,
            hide_index=True
        )

        # Export CSV
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=csv,
            file_name="donnees_inf232.csv",
            mime="text/csv"
        )

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div class='footer'>
    TP INF232 EC2 — Réalisé par <strong>NOUBISSI Yannolf</strong> | Matricule : <strong>24G2179</strong>
</div>
""", unsafe_allow_html=True)
