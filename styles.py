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
    MENTAL MATHS INPUTS
    ========================= */

    div[data-testid="stTextInput"] input,
    div[data-baseweb="input"] > div {
    border-radius: 0px !important;
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
    
LIFE_SCIENCES_CSS = """
    <style>

    .life-header {
    background: linear-gradient(120deg, #073B4C, #087E8B);
    padding: 28px 30px;
    border-left: 5px solid #55D6BE;
    margin-bottom: 25px;
}

    .life-title {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 700;
    margin: 0;
}

    .life-subtitle {
    color: #BDEFE8;
    font-size: 13px;
    letter-spacing: 2px;
    margin-top: 8px;
}

    .life-section {
    color: #087E8B;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 32px 0 14px 0;
}

    .life-question-card {
    background: #EAF8F7;
    border: 1px solid #A8DCD5;
    border-left: 4px solid #087E8B;
    padding: 20px 22px;
    margin: 18px 0 10px 0;
}

    .life-question-number {
    color: #087E8B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

    .life-question-text {
    color: #073B4C;
    font-size: 16px;
    font-weight: 600;
    line-height: 1.6;
}

    .life-topic {
    color: #438F83;
    font-size: 11px;
    margin-top: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

    .life-result {
    padding: 17px 20px;
    margin: 10px 0 22px 0;
    border: 1px solid;
}

    .life-correct {
    background: #E5F6EC;
    border-color: #65B98A;
    border-left: 5px solid #27965B;
}

    .life-incorrect {
    background: #FFF0EB;
    border-color: #E8A18E;
    border-left: 5px solid #D76B52;
}

    .life-result-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 7px;
}

    .life-result-text {
    color: #164B50;
    font-size: 13px;
    line-height: 1.6;
}

    .life-score-card {
    background: linear-gradient(120deg, #073B4C, #087E8B);
    border-bottom: 5px solid #55D6BE;
    padding: 28px;
    text-align: center;
    margin-top: 30px;
}

    .life-score-label {
    color: #BDEFE8;
    font-size: 12px;
    letter-spacing: 2px;
}

    .life-score-number {
    color: #FFFFFF;
    font-size: 46px;
    font-weight: 800;
    margin: 8px 0;
}

    .life-score-caption {
    color: #C8F3E9;
    font-size: 14px;
}

    .life-stat {
    background: #EAF8F7;
    border: 1px solid #A8DCD5;
    padding: 18px;
    text-align: center;
    margin-top: 15px;
}

    .life-stat-label {
    color: #438F83;
    font-size: 11px;
    letter-spacing: 1px;
}

    .life-stat-value {
    color: #073B4C;
    font-size: 25px;
    font-weight: 700;
}

   /* Compact Answer Review Cards */

[class*="st-key-life_review_correct_"],
[class*="st-key-life_review_incorrect_"] {
    padding: 12px 17px;
    margin: 8px 0 15px 0;
    border-radius: 3px;
    font-size: 13px;
    line-height: 1.4;
}

[class*="st-key-life_review_correct_"] {
    background: #E5F6EC;
    border: 1px solid #65B98A;
    border-left: 4px solid #27965B;
}

[class*="st-key-life_review_incorrect_"] {
    background: #FFF0EB;
    border: 1px solid #E8A18E;
    border-left: 4px solid #D76B52;
}

/* Reduce spacing between text elements */
[class*="st-key-life_review_"] p {
    margin-bottom: 5px;
    font-size: 13px;
    line-height: 1.4;
}

[class*="st-key-life_review_"] h3 {
    font-size: 13px;
    margin: 0 0 6px 0;
}
[class*="st-key-life_review_"] {
    padding-bottom: 20px;
}

[class*="st-key-life_review_"] p:last-child {
    margin-bottom: 6px;
}
</style>
"""
    