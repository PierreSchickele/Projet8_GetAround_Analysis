import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings("ignore")

### CONFIG
st.set_page_config(
    page_title="GetAround Analysis",
    page_icon="📝",
    layout="wide"
)

API_URL = os.environ.get("API_URL")
PORT = os.environ.get("PORT")

### TITLE AND TEXT
st.title("GetAround Dashboard")

st.markdown("""
    Bienvenue sur le Dashboard **GetAround**.
    On utilise **deux services** :
    1. Un service client, qui montre l'analyse des retards.
    2. Une API FastAPI que le client utilise pour prédire le montant d'une location.

    Le code est disponible ici 👉 [Source code](https://github.com/PierreSchickele/Projet8_GetAround_Analysis)
""")

@st.cache
def load_data():
    data_file_delay = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
    data_file_pricing = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv'
    data_delay = pd.read_excel(data_file_delay)
    data_pricing = pd.read_csv(data_file_pricing)
    return data_delay, data_pricing

data_load_state = st.text('Loading data...')
df_delay, df_pricing = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df_delay) 

st.markdown('## Analyse des retards')

# Graphique 1 : Scatter Plot des retards au checkout par rapport au temps depuis la dernière location

st.markdown('### Retards au checkout par rapport à la dernière location')
delay_by_timedelta = px.scatter(df_delay,
                 x='time_delta_with_previous_rental_in_minutes',
                 y='delay_at_checkout_in_minutes',
                 color='checkin_type',
                 range_y=[-5000,12000])
st.plotly_chart(delay_by_timedelta, use_container_width=True)

# Graphique 2 : Pie Chart des proportions de retards

# Fonction pour calculer les proportions de retards
def calculate_proportions(df, checkin_type=None):
    if checkin_type:
        df = df[df['checkin_type'] == checkin_type]
    f_retards = len(df[df['delay_at_checkout_in_minutes'] > 0])
    f_non_retards = len(df[df['delay_at_checkout_in_minutes'] <= 0])
    return [f_non_retards, f_retards]

proportions_tout = calculate_proportions(df_delay)
proportions_mobile = calculate_proportions(df_delay, 'mobile')
proportions_connect = calculate_proportions(df_delay, 'connect')

colors = ['blue', 'red']
pie_retards = go.Figure()
pie_retards.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_tout,
                             name="Mobile & Connect", sort=False, marker_colors=colors))
pie_retards.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_mobile,
                             name="Mobile", visible=False, sort=False, marker_colors=colors))
pie_retards.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_connect,
                             name="Connect", visible=False, sort=False, marker_colors=colors))
pie_retards.update_traces(hole=.4, hoverinfo="label+percent+name")
pie_retards.update_layout(
    updatemenus=[{
        "buttons": [
            {
                "label": "Mobile & Connect",
                "method": "update",
                "args": [{"visible": [True, False, False]}]
            },
            {
                "label": "Mobile",
                "method": "update",
                "args": [{"visible": [False, True, False]}]
            },
            {
                "label": "Connect",
                "method": "update",
                "args": [{"visible": [False, False, True]}]
            }
        ],
        "direction": "down",
        "showactive": True,
        "bgcolor": "lightgrey",  # Couleur de fond par défaut
        "font": {"color": "black"},  # Couleur du texte
    }]
)

st.markdown('### Proportion de retards par type de checkin')
st.plotly_chart(pie_retards, use_container_width=True)

# Graphique 3 : Box Plot des retards au checkout par type de checkin
delay_by_checkin_type = px.box(df_delay, y='delay_at_checkout_in_minutes', color='checkin_type', range_y=[-25000,72000])

st.markdown('### Répartition des longueurs de retards par type de checkin')
st.plotly_chart(delay_by_checkin_type, use_container_width=True)

# Graphique 4 : Histogramme des proportions de retards par valeur de seuil

def calculate_proportions2(df):
    thresholds_in_minutes = [0, 50, 100, 150, 200, 250, 300, 350, 400]
    mask = (df['delay_at_checkout_in_minutes'].notnull())
    mask_connect = (df['checkin_type'] == 'connect')
    mask_mobile = (df['checkin_type'] == 'mobile')
    proportions = pd.DataFrame({
        'thresholds': thresholds_in_minutes,
        'prop_retards': [df.loc[mask, 'delay_at_checkout_in_minutes'].
                        gt(threshold).mean() for threshold in thresholds_in_minutes],
        'prop_retards_connect': [df.loc[mask & mask_connect, 'delay_at_checkout_in_minutes'].
                                gt(threshold).mean() for threshold in thresholds_in_minutes],
        'prop_retards_mobile': [df.loc[mask & mask_mobile, 'delay_at_checkout_in_minutes'].
                                gt(threshold).mean() for threshold in thresholds_in_minutes]
    })
    return proportions

proportion_de_retards = calculate_proportions2(df_delay)

delay_by_thresholds = go.Figure()
delay_by_thresholds.add_trace(
    go.Bar(
        x=proportion_de_retards["thresholds"],
        y=proportion_de_retards["prop_retards"],
        name="Proportion de retards"
    )
)
delay_by_thresholds.add_trace(
    go.Bar(
        x=proportion_de_retards["thresholds"],
        y=proportion_de_retards["prop_retards_mobile"],
        name="Proportion de retards (only mobile)"
    )
)
delay_by_thresholds.add_trace(
    go.Bar(
        x=proportion_de_retards["thresholds"],
        y=proportion_de_retards["prop_retards_connect"],
        name="Proportion de retards (only connect)"
    )
)
delay_by_thresholds.update_layout(
    title='Proportion de retards selon le seuil et le scope',
    xaxis_title='Seuil',
    yaxis_title='Proportion de retards',
    bargap=0.2
)

st.markdown('### Proportion de retards par seuil')
st.plotly_chart(delay_by_thresholds, use_container_width=True)

