import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import os

#Page Config
st.set_page_config(
    page_title="Tennis-Dashboard Fulda",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Custom CSS for background,metrics, navigation-bar 
st.markdown("""
    <style>
    /* background and font */
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3d59; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { font-size: 2rem; color: #ff6e40; }
    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Vergrößert die Navigations-Schrift in der Sidebar */
    [data-testid="stSidebarNav"] label, 
    div[data-testid="stWidgetLabel"] p {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
        
    /* Vergrößert die Emojis/Icons in der Radio-Navigation */
    .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 1.25rem !important;
    }

    /* Reduziert den Abstand zum oberen Rand */
    .block-container {
        padding-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

#Loading the data
@st.cache_data
def load_all_data():
    
    #Searching for folder in which app.py lies
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    path_total = os.path.join(base_dir, "data", "df_clubs_complete_final.csv")
    path_unique = os.path.join(base_dir, "data", "df_clubs_unique_final.csv")
    
    df_total = pd.read_csv(path_total)
    df_unique = pd.read_csv(path_unique)
    
    #Cleaning coordinates for interactive map
    df_unique = df_unique.dropna(subset=['latitude', 'longitude'])
    df_unique.columns = df_unique.columns.str.strip()

    df_unique = df_unique.rename(columns={"scraped_club_name": "Vereinsname"})
    df_total = df_total.rename(columns={"scraped_club_name": "Vereinsname"})
    
    return df_total, df_unique

df_total, df_unique = load_all_data()

if 'selected_club' not in st.session_state:
    st.session_state.selected_club = None

#SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Tennis-Dashboard Fulda")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🔍 Vereinsdetails"],
        index=0
    )



    st.markdown("---")

    #Info box data sources and last date of updating
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: none;">
            <p style="margin: 0; color: #555; font-size: 1.2rem;">
                <strong>📊 Datenquellen (Web Scraping):</strong><br>
                • <a href="https://htv.liga.nu/" target="_blank" style="color: #1e3d59; text-decoration: none; font-weight: bold;">nuLiga HTV</a><br>
                • <a href="https://www.sportkreis-fulda-huenfeld.de/" target="_blank" style="color: #1e3d59; text-decoration: none; font-weight: bold;">Sportkreis Fulda-Hünfeld e.V.</a><br><br>
                <strong>📅 Letztes Update:</strong><br>
                15. Februar 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

#STARTSEITE
if page == "📊 Dashboard":
    st.title("Dashboard: Tennisvereine im Landkreis Fulda")

    st.markdown(""" 
                Liebe/r Besucher/in,

                herzlich Willkommen auf der Website unseres interaktiven Tennis-Dashboard für die Region Fulda.
                Dieses Dashboard hat das Ziel, einen möglichst detaillierten aber gleichzeitig auch 
                benutzerfreundlichen Überblick über die Tennisvereine in unserem schönen Landkreis zu bieten. 
                Das Dashboard richtet sich damit an alle tennisinteressierten, aber natürlich auch bereits tennisspielenden Menschen sowie 
                insbesondere an Tennisanfänger/innen sowie Trainer/innen, die auf der Suche nach dem passenden Verein
                in ihrem Umkreis sind.

                Viel Spaß mit unserem Dashboard und auf dem Tennisplatz wünscht Ihnen das Team vom 
                Tennis-Dashboard Fulda!
                """)
    
    metrics_container = st.container()
    map_container = st.container()
    list_container = st.container()

    with list_container:
        st.subheader("📋 Vereinsauswahl")
        st.info("Klicken Sie auf die Checkbox links vor der jeweiligen Zeile, um Karte und Kennzahlen nach dem entsprechenden Verein zu filtern.")
        
        #Selection in the table
        selection = st.dataframe(
            df_unique[['Vereinsname']],
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
            use_container_width=True
        )

    #Which club has been selected
    selected_rows = selection.selection.rows
    if selected_rows:
        #Extracting data of the chosen club
        display_df = df_unique.iloc[selected_rows]
        st.session_state.selected_club = display_df.iloc[0]['Vereinsname']
        
        #Focus-view for the map
        lat, lon, zoom = display_df.iloc[0]['latitude'], display_df.iloc[0]['longitude'], 14
        status_text = f"Fokus auf: {st.session_state.selected_club}"
    else:
        #overall view if nothing is selected
        display_df = df_unique
        st.session_state.selected_club = None
        lat, lon, zoom = 50.55, 9.68, 10
        status_text = "Gesamter Landkreis Fulda"

    # Definition of tooltip for map
    tooltip_config = {
    "html": """
        <b>Verein:</b> {Vereinsname} <br/>
        <b>Freiplätze:</b> {Anzahl_Freiplaetze} <br/>
        <b>Hallenplätze:</b> {Anzahl_Hallenplaetze} <br/>
        <b>Mitglieder:</b> {Mitglieder_Gesamt_Gesamt}
    """,
    "style": {
        "backgroundColor": "#1e3d59",
        "color": "white",
        "font-family": "sans-serif",
        "z-index": "10000"
    }
    }

    #Metrics
    with metrics_container:
        st.write(f"### Kennzahlen: {status_text}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Vereine", len(display_df))
        m2.metric("Plätze", int(display_df['Anzahl_Freiplaetze'].sum() + display_df['Anzahl_Hallenplaetze'].sum()))
        m3.metric("Mitglieder", f"{int(display_df['Mitglieder_Gesamt_Gesamt'].sum()):,}".replace(",", "."))
        st.write("---")

    #Map
    with map_container:

        st.subheader("Interaktive Vereinskarte")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light',
            initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=0),
            layers=[pdk.Layer(
                'ScatterplotLayer',
                data=display_df,
                get_position='[longitude, latitude]',
                get_color='[255, 75, 75, 180]', # Markante rote Punkte
                get_radius=250 if selected_rows else 450,
                pickable=True
            )],
            tooltip=tooltip_config
        ))
        st.write("---")

#SEITE: VEREINS-DETAILS
elif page == "🔍 Vereinsdetails":
    st.title("🔍 Detailinfos zu den Vereinen")
    
    #Selection of club (synchronized with main page)
    all_clubs = sorted(df_unique['Vereinsname'].unique())
    default_idx = all_clubs.index(st.session_state.selected_club) if st.session_state.selected_club in all_clubs else 0
    
    selected_club = st.selectbox("Wählen Sie einen Verein aus:", all_clubs, index=default_idx)

    if selected_club:
        #Filtering data
        club_info = df_unique[df_unique['Vereinsname'] == selected_club].iloc[0]
        
        club_details = df_total[df_total['Vereinsname'] == selected_club]

        #ALLGEMEINE INFORMATIONEN
        st.subheader("📍 Allgemeine Informationen")
        with st.container(border=True):
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.markdown(f"**🏠 Adresse**\n\n{club_info.get('Platzadresse', 'K.A.')}")
            with col_a2:
                web = club_info.get('website', 'Nicht angegeben')
                st.markdown(f"**🌐 Website**\n\n[{web}]({web})" if "http" in str(web) else f"**🌐 Website**\n\n{web}")
            with col_a3:
                st.markdown(f"**🎯 Zielgruppe**\n\nJugend & Erwachsene")

        #MITGLIEDER
        st.subheader("👥 Mitglieder")
        with st.container(border=True):
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Männlich", int(club_info.get('Mitglieder_Maennlich_Gesamt', 0)))
            col_m2.metric("Weiblich", int(club_info.get('Mitglieder_Weiblich_Gesamt', 0)))
            col_m3.metric("Gesamt", int(club_info.get('Mitglieder_Gesamt_Gesamt', 0)))

        #PLÄTZE
        st.subheader("Tennisplätze")
        with st.container(border=True):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("Freiplätze", int(club_info.get('Anzahl_Freiplaetze', 0)))
                st.caption(f"Belag: {club_info.get('Belag_Freiplaetze', 'Sand')}")
            with col_p2:
                st.metric("Hallenplätze", int(club_info.get('Anzahl_Hallenplaetze', 0)))
                st.caption(f"Belag: {club_info.get('Belag_Hallenplaetze', 'K.A.')}")

        #ANSPRECHPARTNER/INNEN
        st.subheader("👤 Ansprechpartner/innen")
        if not club_details.empty:

            display_staff = club_details[['Funktion', 'Name','Telefon']].copy()
            st.dataframe(
                display_staff.fillna("Nicht angegeben"),
                hide_index=True,
                use_container_width=True
            )
        else:

            st.info("Für diesen Verein wurden keine Ansprechpartner im Detail-Datensatz gefunden.")
