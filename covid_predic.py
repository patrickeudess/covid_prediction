import streamlit as st
import pickle
import numpy as np

# Chargement du modèle
with open("covid_pred.pkl", "rb") as file:
    model = pickle.load(file)

# Configuration de la page
st.set_page_config(
    page_title="Prédiction COVID-19",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style de l'application
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    h1 {
        color: #2b6777;
    }
    .sidebar .sidebar-content {
        background-color: #1f487e;
        color: white;
    }
    .stButton>button {
        background-color: #2b6777;
        color: white;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Titre principal
st.title("🦠 Prédiction du risque COVID-19")
st.write(
    "Cette application prédit si un patient atteint du COVID-19 est à haut risque ou non, "
    "en fonction de ses symptômes, de son état et de ses antécédents médicaux."
)

# Disposition : Formulaire des entrées utilisateur
st.sidebar.header("📝 Entrée des données")
st.sidebar.write("Veuillez remplir les informations suivantes pour obtenir une prédiction.")

# Fonction pour collecter les données utilisateur
def user_input_features():
    usmer = st.sidebar.selectbox("Référé par une unité médicale (USMER) ?", ["Non", "Oui"])
    unite_medicale = st.sidebar.selectbox("Traité dans une unité médicale ?", ["Non", "Oui"])
    sexe = st.sidebar.selectbox("Sexe du patient", ["Homme", "Femme"])
    type_patient = st.sidebar.selectbox("Type de patient", ["Ambulatoire", "Hospitalisé"])
    date_de_deces = st.sidebar.selectbox("Le patient est-il décédé ?", ["Non", "Oui"])
    intube = st.sidebar.selectbox("Le patient est-il intubé ?", ["Non", "Oui"])
    pneumonie = st.sidebar.selectbox("Le patient souffre-t-il de pneumonie ?", ["Non", "Oui"])
    age = st.sidebar.slider("Âge du patient", 0, 120, 30, step=1)
    enceinte = st.sidebar.selectbox("Le patient est-il enceinte ?", ["Non", "Oui", "Non applicable"])
    diabete = st.sidebar.selectbox("Le patient est-il diabétique ?", ["Non", "Oui"])
    bpco = st.sidebar.selectbox("Le patient a-t-il une BPCO ?", ["Non", "Oui"])
    asthme = st.sidebar.selectbox("Le patient est-il asthmatique ?", ["Non", "Oui"])
    immunosupprime = st.sidebar.selectbox("Le patient est-il immunosupprimé ?", ["Non", "Oui"])
    hypertension = st.sidebar.selectbox("Le patient a-t-il de l'hypertension ?", ["Non", "Oui"])
    autres_maladies = st.sidebar.selectbox("Le patient souffre-t-il d'autres maladies ?", ["Non", "Oui"])
    cardiovasculaire = st.sidebar.selectbox("Le patient a-t-il des maladies cardiovasculaires ?", ["Non", "Oui"])
    obesite = st.sidebar.selectbox("Le patient souffre-t-il d'obésité ?", ["Non", "Oui"])
    insuffisance_renale = st.sidebar.selectbox("Le patient a-t-il une insuffisance rénale chronique ?", ["Non", "Oui"])
    tabac = st.sidebar.selectbox("Le patient est-il fumeur ?", ["Non", "Oui"])
    classification_finale = st.sidebar.selectbox("Classification finale COVID-19 du patient", ["Bénin", "Grave"])
    usi = st.sidebar.selectbox("Le patient est-il en unité de soins intensifs (USI) ?", ["Non", "Oui"])

    # Préparation des données pour le modèle
    inputs = np.array([
        1 if usmer == "Oui" else 0,
        1 if unite_medicale == "Oui" else 0,
        1 if sexe == "Femme" else 0,  # Femme = 1, Homme = 0
        1 if type_patient == "Hospitalisé" else 0,
        1 if date_de_deces == "Oui" else 0,
        1 if intube == "Oui" else 0,
        1 if pneumonie == "Oui" else 0,
        age,
        1 if enceinte == "Oui" else 0,
        1 if diabete == "Oui" else 0,
        1 if bpco == "Oui" else 0,
        1 if asthme == "Oui" else 0,
        1 if immunosupprime == "Oui" else 0,
        1 if hypertension == "Oui" else 0,
        1 if autres_maladies == "Oui" else 0,
        1 if cardiovasculaire == "Oui" else 0,
        1 if obesite == "Oui" else 0,
        1 if insuffisance_renale == "Oui" else 0,
        1 if tabac == "Oui" else 0,
        1 if classification_finale == "Grave" else 0,
        1 if usi == "Oui" else 0
    ]).reshape(1, -1)

    return inputs

# Collecte des données utilisateur
inputs = user_input_features()

# Bouton de prédiction
if st.button("Prédire"):
    try:
        # Effectuer la prédiction
        prediction = model.predict(inputs)

        # Afficher le résultat
        if prediction[0] == 1:
            st.error("Le patient est à HAUT RISQUE.")
        else:
            st.success("Le patient n'est PAS à haut risque.")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")

# Footer
st.markdown("---")
st.write("Développé par [Patrick ALLA]")
