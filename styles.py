import streamlit as st


def apply_styles():

    st.set_page_config(
        page_title="UNROT | Learn Something Daily",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <style>

    /* =========================
       GLOBAL DESIGN SYSTEM
    ========================= */

    :root {
        --marine: #07596B;
        --teal: #168C91;
        --cyan: #9AD8D1;

        --paper: #F7F5EF;
        --sidebar: #DCEAE5;
        --sand: #D8D8CE;

        --ink: #263A3D;
        --muted: #667779;

        --white: #FFFFFF;
    }


    /* =========================
       MAIN APPLICATION
    ========================= */

    .stApp {
        background-color: var(--paper);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background-color: var(--paper);
    }

    [data-testid="stMain"] {
        background-color: var(--paper);
    }


    /* =========================
       TYPOGRAPHY
    ========================= */

    h1, h2, h3 {
        font-family: Georgia, "Times New Roman", serif !important;
        color: var(--marine);
        font-weight: 600;
    }

    .hero h1 {
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: clamp(2.5rem, 4vw, 3.5rem);
        font-weight: 600;
        letter-spacing: -1px;
        color: var(--white);
    }

    p, label, .stMarkdown {
        color: var(--ink);
    }


    /* =========================
       SIDEBAR
    ========================= */

    [data-testid="stSidebar"] {
        background-color: var(--sidebar);
        border-right: 1px solid var(--sand);
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--ink) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #C5D7D0;
    }


    /* =========================
       HERO SECTION
    ========================= */

    .hero {
        background: linear-gradient(
            115deg,
            #07596B,
            #087F8C
        );

        color: var(--white);

        padding: 2rem 2rem 1.8rem;

        border-radius: 3px;

        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #E4F4F0;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .eyebrow {
        color: var(--teal);
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.14em;
        font-weight: 700;
    }


    /* =========================
       ACTIVITY CARDS
    ========================= */

    .activity-card {
        background-color: var(--white);

        border: 1px solid var(--sand);
        border-radius: 3px;

        padding: 1.2rem;

        min-height: 155px;

        margin-bottom: 0.2rem;
    }

    .activity-card h3 {
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: 1.2rem;
        color: var(--marine);
        margin: 0.6rem 0;
    }

    .activity-card p {
        color: var(--muted);
        font-size: 0.93rem;
    }


    /* =========================
       BUTTONS
    ========================= */

    div.stButton > button {
        background-color: var(--teal);
        color: var(--marine);

        border: 1px solid #B8D2CC;
        border-radius: 3px;

        font-weight: 600;

        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: var(--sidebar);
        color: var(--marine);
        border-color: var(--teal);
    }


    /* =========================
       METRICS
    ========================= */

    [data-testid="stMetricValue"] {
        color: var(--marine);
        font-family: Georgia, "Times New Roman", serif;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }


    /* =========================
       PROGRESS BAR
    ========================= */

    [data-testid="stProgress"] {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    [data-testid="stProgress"] div[role="progressbar"] {
        background-color: #DCEAE5;
        border-radius: 2px;
    }


    /* =========================
       GENERAL CLEANUP
    ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """, unsafe_allow_html=True)