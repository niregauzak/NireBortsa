import streamlit as st

st.title('Nire bortsa')
st.write('Jarraipen bat egiteko: prezioak ikusi eta aztertu')

# --- PAGE SETUP ---
original_page = st.Page(
    "pages/05b-My_Dashboard_LeChat.py",
    title="Inicial App",
    #icon=":material/account_circle:",
    default=True,
)

Ikerketak_SP = st.Page(
    "pages/05c-ikerketak_SP.py",
    title="Standard and Pools",
    #icon=":material/bar_chart:",
)

Ikerketak_NYSE = st.Page(
    "pages/05c-ikerketak_NYSE.py",
    title="New York Stock Exchange (NYSE)",
    #icon=":material/bar_chart:",
)

Ikerketak_NASDAQ = st.Page(
    "pages/05c-ikerketak_NASDAQ.py",
    title="NASDAQ",
    #icon=":material/bar_chart:",
)

Ikerketak_Euro = st.Page(
    "pages/05c-ikerketak_Euro.py",
    title="Euronext",
    #icon=":material/bar_chart:",
)

Ikerketak_DAX = st.Page(
    "pages/05c-ikerketak_DAX.py",
    title="DAX",
    #icon=":material/bar_chart:",
)

Ikerketak_IBEX = st.Page(
    "pages/05c-ikerketak_IBEX.py",
    title="IBEX",
    #icon=":material/bar_chart:",
)

Azalpenak = st.Page(
    "pages/09-azalpenak.py",
    title="Azalpenak",
    #icon=":material/bar_chart:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
                #"Aurrenekoa (IA)": [original_page],
        "Nire ikerketak egiteko": [Ikerketak_SP,Ikerketak_NYSE,Ikerketak_NASDAQ,Ikerketak_Euro,Ikerketak_DAX,Ikerketak_IBEX],
        "Azalpenak": [Azalpenak],
        #"Urteka, batera": [urteka_bateratuta],
        #"Merkatuak": [s_and_p_mp_sub,ibex35],
        
    }
)


# --- SHARED ON ALL PAGES ---
#st.logo("assets/codingisfun_logo.png")
#st.sidebar.text("Joniren boltsa")


# --- RUN NAVIGATION ---
pg.run()