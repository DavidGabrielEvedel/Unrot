import streamlit as st


def apply_styles():

    st.set_page_config(
        page_title="UNROT | Learn Something Daily",
        page_icon="🪷",
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

   /*---UNROT DSA-------*/

    .dsa-header {
    background: linear-gradient(120deg, #EAF8F7, #DDF3EF);
    border-left: 4px solid #087E8B;
    padding: 22px 25px;
    margin-bottom: 25px;
}

    .dsa-eyebrow {
    color: #438F83;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

    .dsa-title {
    color: #073B4C;
    font-size: 27px;
    font-weight: 700;
}

    .dsa-subtitle {
    color: #438F83;
    font-size: 13px;
    margin-top: 7px;
}

    .dsa-problem-header {
    display: flex;
    align-items: center;
    gap: 13px;
    flex-wrap: wrap;
    margin-top: 12px;
    margin-bottom: 8px;
}

    .dsa-problem-title {
    color: #073B4C;
    font-size: 23px;
    font-weight: 700;
}

    .dsa-difficulty {
    background: #DDF3E8;
    color: #287A59;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 0px;}
    
    /* LeetCode / NeetCode buttons */
    .stButton button[kind="secondary"] {
    color: white !important;
}
    

/* Default state */
    div[data-testid="stExpander"] details > summary {
    background-color: #FFFFFF;
    border: 1px solid #DCE5E5;
    border-radius: 0px;
    padding: 10px 15px;
    color: #18343A;
    transition: background-color 0.2s ease;
}

/* Hover state */
    div[data-testid="stExpander"] details > summary:hover {
    background-color: #EAF8F7;
    color: #087F8C;
    border-color: #A8DCD5;
}

/* Expanded / clicked state */
    div[data-testid="stExpander"] details[open] > summary {
    background-color: #EAF8F7;
    color: #073B4C;
    border-color: #A8DCD5;
    border-left: 4px solid #087E8B;
}

/* Focus state — remove dark default outline */
    div[data-testid="stExpander"] details > summary:focus {
    outline: none;
    box-shadow: none;
}

/* Expanded content */
    div[data-testid="stExpander"] details > div {
    background-color: #FFFFFF;
    border: 1px solid #DCE5E5;
    border-top: none;
    padding: 12px 16px;
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
WILDCARD_CSS = """
/* Question boxes */
[class*="st-key-wildcard_q_"] {
    padding: 15px 19px 10px 19px;
    margin: 9px 0 13px 0;
    border: 1px solid #C8D8DF;
    border-radius: 0px;
    color: #172B35;
}

[class*="st-key-wildcard_q_0"] {
    background: #EAF2F7;
    border-color: #C1D5E2;
}

[class*="st-key-wildcard_q_1"] {
    background: #F4F0E8;
    border-color: #DDD1BC;
}

[class*="st-key-wildcard_q_2"] {
    background: #F0EEF6;
    border-color: #D4CEE2;
}

[class*="st-key-wildcard_q_3"] {
    background: #EAF1F3;
    border-color: #C8D8DC;
}

[class*="st-key-wildcard_q_4"] {
    background: #F5F0EA;
    border-color: #DED2C5;
}

/* Question typography */
[class*="st-key-wildcard_q_"] p {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 14px;
    line-height: 1.45;
    color: #172B35;
    margin-bottom: 5px;
}

.wildcard-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: "Times New Roman", serif;
    font-size: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: #426477;
    margin-bottom: 8px;
}

.wildcard-question {
    font-family: "Times New Roman", serif;
    font-size: 17px;
    font-weight: 600;
    color: #172B35;
    line-height: 1.35;
    margin-bottom: 8px;
}

/* Radio options */
[class*="st-key-wildcard_q_"] [data-testid="stRadio"] label {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 13px;
    color: #172B35;
}

[class*="st-key-wildcard_q_"] [data-testid="stRadio"] {
    gap: 3px;
}

/* Review cards */
[class*="st-key-wildcard_review_correct_"],
[class*="st-key-wildcard_review_incorrect_"] {
    padding: 12px 17px;
    margin: 8px 0 14px 0;
    border-radius: 0px;
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 13px;
    line-height: 1.4;
}

[class*="st-key-wildcard_review_correct_"] {
    background: #E5F6EC;
    border: 1px solid #65B98A;
    border-left: 4px solid #27965B;
}

[class*="st-key-wildcard_review_incorrect_"] {
    background: #FFF0EB;
    border: 1px solid #E8A18E;
    border-left: 4px solid #D76B52;
}

[class*="st-key-wildcard_review_"] p {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 13px;
    line-height: 1.4;
    margin-bottom: 5px;
    color: #172B35;
}

.wildcard-review-label {
    font-family: "Times New Roman", serif;
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 7px;
    color: #172B35;
}

/* Headings */
.wildcard-heading {
    font-family: "Times New Roman", serif;
    font-size: 27px;
    font-weight: 600;
    color: #173D50;
    margin-bottom: 2px;
}

.wildcard-subtitle {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 15px;
    font-style: italic;
    letter-spacing: 0.15px;
    line-height: 1.5;
    color: #526C78;
    margin-top: 5px;
    margin-bottom: 18px;
}

.st-key-wildcard_submit button,
button[kind="primaryFormSubmit"] {
    background-color: #E89A52 !important;
    color: #FFFFFF !important;
    border: 1px solid #D88940 !important;
    border-radius: 0px !important;
    font-family: "Georgia Pro", Georgia, serif !important;
    font-weight: 700 !important;
}

.st-key-wildcard_submit button:hover,
button[kind="primaryFormSubmit"]:hover {
    background-color: #D98236 !important;
    border-color: #D98236 !important;
}
"""   

CS_PREP_CSS = """
/* CS Prep — Question boxes */
[class*="st-key-cs_q_"] {
    padding: 15px 19px 10px 19px;
    margin: 9px 0 13px 0;
    background: #F6F3EC;
    border: 1px solid #DED8CB;
    border-left: 3px solid #527487;
    border-radius: 0px;
    color: #172B35;
}

/* Question typography */
[class*="st-key-cs_q_"] p {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 14px;
    line-height: 1.45;
    color: #172B35;
    margin-bottom: 5px;
}
/* CS Prep typography */
.cs-eyebrow {
    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    color: #527487;
    margin-bottom: 8px;
}

.cs-daily-label {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 1px;
    color: #527487;
    border-top: 1px solid #C8D8DF;
    border-bottom: 1px solid #C8D8DF;
    padding: 10px 0;
    margin: 18px 0;
}

.cs-meta {
    display: flex;
    justify-content: space-between;
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
    color: #527487;
    margin-bottom: 7px;
}

.cs-topic {
    font-family: Consolas, monospace;
    font-size: 11px;
    color: #98734E;
    margin-bottom: 8px;
}

.cs-question {
    font-family: "Times New Roman", serif;
    font-size: 17px;
    font-weight: bold;
    line-height: 1.4;
    color: #172B35;
    margin-bottom: 10px;
}

[class*="st-key-cs_q_"] label {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 13px;
    color: #172B35;
}

.cs-set-note {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 0.7px;
    color: #527487;
    text-align: center;
    padding: 12px 0;
}
/* Results header */
.cs-results-eyebrow,
.cs-review-intro {
    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1.5px;
    color: #527487;
    margin-bottom: 8px;
}

.cs-score {
    font-family: "Times New Roman", serif;
    font-size: 48px;
    font-weight: bold;
    color: #173D50;
    line-height: 1.1;
}

.cs-score span {
    font-size: 25px;
    color: #82949B;
}

.cs-results-subtitle {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 1px;
    color: #527487;
    margin-bottom: 15px;
}

.cs-performance-line {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 0.5px;
    color: #526C78;
    margin-bottom: 12px;
}

.cs-review-intro {
    margin-top: 24px;
    margin-bottom: 12px;
}

.cs-review-meta {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 0.5px;
    color: #71858E;
    margin-bottom: 12px;
}

.cs-review-section {
    font-family: Consolas, monospace;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    color: #527487;
    margin-top: 15px;
    margin-bottom: 5px;
}

.cs-review-question {
    font-family: "Times New Roman", serif;
    font-size: 17px;
    font-weight: bold;
    line-height: 1.45;
    color: #172B35;
    margin-bottom: 12px;
}

.cs-review-answer {
    font-family: "Georgia Pro", Georgia, serif;
    font-size: 13px;
    line-height: 1.55;
    color: #263E49;
}

/* Unattempted cards */
[class*="st-key-cs_review_unattempted_"] {
    padding: 17px 20px;
    margin: 10px 0 16px;
    background: #EEF1F3;
    border: 1px solid #CDD7DC;
    border-left: 4px solid #718B99;
    border-radius: 0px;
}
"""

TODO_CSS="""

.todo-eyebrow {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #6F9EAA;
    margin-bottom: 5px;
}

.todo-heading {
    font-family: Georgia, serif;
    font-size: 43px;
    color: #173D50;
    line-height: 1.1;
    margin: 0;
}

.todo-subtitle {
    font-family: Georgia, serif;
    font-size: 15px;
    font-style: italic;
    color: #788C91;
    margin-top: 5px;
    margin-bottom: 8px;
}

.todo-task-meta {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 1.2px;
    color: #6F9EAA;
    margin: 5px 0;
}

.todo-label {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: bold;
    color: #173D50;
    margin: 5px 0 8px 0;
}

.todo-task-title {
    font-family: Georgia, serif;
    font-size: 17px;
    color: #173D50;
    line-height: 1.4;
    margin: 3px 0;
}

.todo-completed {
    font-family: Georgia, serif;
    font-size: 15px;
    color: #91A5A5;
    text-decoration: line-through;
}

/* Compact page spacing */

.stMainBlockContainer {
    padding-top: 2rem !important;
}

.stMainBlockContainer [data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

.stMainBlockContainer [data-testid="stElementContainer"] {
    margin-bottom: 0 !important;
}

/* Dividers */

.stMainBlockContainer hr {
    border-color: #DCE5E1 !important;
    margin: 0.8rem 0 !important;
}

/* Buttons */

.stMainBlockContainer .stButton > button,
.stMainBlockContainer button[kind="primaryFormSubmit"] {
    border-radius: 0px !important;
    border: 1px solid #173D50 !important;
    background: #173D50 !important;
    color: #F8F7F2 !important;
    font-family: Consolas, monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    font-weight: 600 !important;
    min-height: 36px !important;
    padding: 5px 14px !important;
    box-shadow: none !important;
    transition: 0.2s ease;
}

.stMainBlockContainer .stButton > button:hover,
.stMainBlockContainer button[kind="primaryFormSubmit"]:hover {
    background: #6F9EAA !important;
    border-color: #6F9EAA !important;
    color: white !important;
}

/* Delete buttons */

.stMainBlockContainer [class*="st-key-todo_delete_"] button {
    background: transparent !important;
    color: #B56F55 !important;
    border: 1px solid #D9B8A8 !important;
    font-size: 17px !important;
}

/* Input fields */

.stMainBlockContainer .stTextInput input,
.stMainBlockContainer .stDateInput input {
    border-radius: 0 !important;
    border: 1px solid #C9D8D5 !important;
    background: #FFFFFF !important;
    color: #173D50 !important;
    font-family: Georgia, serif !important;
    min-height: 38px !important;
}

.stMainBlockContainer .stTextInput input:focus,
.stMainBlockContainer .stDateInput input:focus {
    border-color: #6F9EAA !important;
    box-shadow: 0 0 0 1px #6F9EAA !important;
}

/* Dropdowns */

.stMainBlockContainer [data-baseweb="select"] > div {
    border-radius: 0 !important;
    border-color: #C9D8D5 !important;
    background: #FFFFFF !important;
}

/* Checkboxes */

.stMainBlockContainer [data-testid="stCheckbox"] label {
    color: #527487 !important;
    font-family: Consolas, monospace !important;
    font-size: 11px !important;
}

/* Task rows */

.stMainBlockContainer [class*="st-key-todo_card_"] {
    background: #F0F3EF;
    border-left: 3px solid #6F9EAA;
    padding: 10px 14px;
    margin: 3px 0;
}

/* Expanders */

.stMainBlockContainer [data-testid="stExpander"] {
    border: 1px solid #DCE5E1 !important;
    border-radius: 0 !important;
    background: #F0F3EF !important;
}

.stMainBlockContainer [data-testid="stExpander"] summary {
    font-family: Consolas, monospace;
    color: #173D50 !important;
    font-size: 11px;
    letter-spacing: 1px;
}

/* Heatmap */

.stMainBlockContainer [data-testid="stPlotlyChart"] {
    background: #F8F7F2;
}
/* ADD TASK + CREATE SECTION */
div[data-testid="stFormSubmitButton"] button {
    background: #173D50 !important;
    border: 1px solid #173D50 !important;
    border-radius: 0px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stFormSubmitButton"] button p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #6F9EAA !important;
    border-color: #6F9EAA !important;
}
.stMainBlockContainer .stButton > button {
    background: #173D50 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #173D50 !important;
}

.stMainBlockContainer .stButton > button:hover {
    background: #6F9EAA !important;
    color: #FFFFFF !important;
}
"""
KALAS_CSS = """
<style>

.stApp {
    background: #F6F5EF;
    color: #243C40;
}

.stMainBlockContainer {
    max-width: 1300px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    font-family: Georgia, serif !important;
    color: #164E59 !important;
    font-weight: 400 !important;
}

p, label {
    color: #243C40;
}

/* BUTTONS */

div[data-testid="stButton"] > button,
div[data-testid="stFormSubmitButton"] button {
    background: #164E59 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #164E59 !important;
    border-radius: 0px !important;
    padding: 0.55rem 1.1rem !important;
    font-weight: 500 !important;
}

div[data-testid="stButton"] > button *,
div[data-testid="stFormSubmitButton"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-testid="stButton"] > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: #39AFA6 !important;
    border-color: #39AFA6 !important;
}

/* INPUTS */

input, textarea,
div[data-baseweb="select"] > div {
    border-radius: 0px !important;
    border-color: #B7D4CE !important;
    background: #FFFFFF !important;
}

/* GENERAL */

hr {
    border-color: #D5E3DC !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #D5E3DC !important;
    border-radius: 0px !important;
    background: #FFFFFF !important;
}

/* HEADER */

.kala-eyebrow {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #399B94;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.kala-hero {
    background: #E4F1EC;
    border: 1px solid #C8DED5;
    border-left: 5px solid #39AFA6;
    padding: 42px;
    margin: 12px 0 30px 0;
}

.kala-hero-number {
    font-family: Georgia, serif;
    font-size: 76px;
    color: #80BDB4;
    text-align: left;
    line-height: 1;
    margin-bottom: 18px;
}

.kala-hero h1 {
    font-size: 46px;
    color: #164E59;
    margin: 8px 0;
}

.kala-hero p {
    font-size: 15px;
    line-height: 1.8;
    color: #58716F;
    max-width: 760px;
}

/* SECTION HEADINGS */

.kala-section-title {
    font-family: Georgia, serif;
    font-size: 29px;
    color: #164E59;
    margin: 30px 0 5px 0;
}

.kala-section-subtitle {
    font-size: 13px;
    color: #788B89;
    margin-bottom: 20px;
}

/* STATS */

.kala-stat {
    background: #FFFFFF;
    border-top: 3px solid #39AFA6;
    padding: 18px;
    border-bottom: 1px solid #D8E5DE;
}

.kala-stat-number {
    font-family: Georgia, serif;
    font-size: 32px;
    color: #164E59;
}

.kala-stat-label {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 1px;
    color: #788B89;
    text-transform: uppercase;
}

/* FEATURED SKILL */

.kala-feature {
    background: #164E59;
    padding: 36px;
    margin: 20px 0 28px 0;
    border-left: 6px solid #39AFA6;
}

.kala-feature .feature-label {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #A8DCD5;
    text-transform: uppercase;
}

.kala-feature h1 {
    color: #FFFFFF !important;
    font-size: 42px;
    margin: 15px 0;
}

.kala-feature p {
    color: #E0EFEB;
    line-height: 1.85;
    font-size: 15px;
}

.kala-feature .feature-meta {
    color: #A8DCD5;
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 1px;
    margin-top: 18px;
}

/* CATEGORY CARDS */

.kala-card {
    background: #FFFFFF;
    border: 1px solid #D8E5DE;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 12px;
    transition: 0.2s ease;
}

.kala-card:hover {
    border-color: #39AFA6;
    background: #F0F8F4;
}

.kala-card-number {
    font-family: Consolas, monospace;
    font-size: 11px;
    letter-spacing: 2px;
    color: #39AFA6;
    margin-bottom: 12px;
}

.kala-card h3 {
    font-size: 20px;
    margin: 0 0 9px 0;
}

.kala-card p {
    font-size: 12px;
    color: #788B89;
    line-height: 1.6;
}

/* CONTENT SECTIONS */

.kala-content-section {
    background: #FFFFFF;
    border: 1px solid #D8E5DE;
    border-left: 3px solid #80BDB4;
    padding: 24px;
    margin: 12px 0;
}

.kala-content-section h3 {
    font-size: 23px;
    margin-bottom: 12px;
}

.kala-content-section p {
    line-height: 1.85;
}

.kala-detail-label {
    font-family: Consolas, monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: #399B94;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* CHALLENGE */

.kala-challenge {
    background: #E4F1EC;
    border: 1px solid #C8DED5;
    border-left: 5px solid #39AFA6;
    padding: 27px;
    margin: 18px 0;
}

/* CLASSICAL VERSE */

.kala-verse {
    background: #F1F5F0;
    border-left: 4px solid #C29A58;
    padding: 24px;
    margin: 15px 0;
    line-height: 2;
}

.kala-verse-text {
    font-family: Georgia, serif;
    font-size: 21px;
    color: #164E59;
    line-height: 2;
}

/* RESOURCE CARDS */

.kala-resource {
    background: #FFFFFF;
    border: 1px solid #D8E5DE;
    padding: 17px;
    margin: 8px 0;
}

.kala-resource a {
    color: #205C70;
    font-weight: 600;
    text-decoration: none;
}

.kala-resource p {
    font-size: 13px;
    color: #788B89;
}

/* PROGRESS */

div[data-testid="stProgressBar"] > div > div {
    background: #39AFA6 !important;
}
/* MAIN KALAS INTRO CARD */

div[class*="st-key-kala-overview-card"] {
    background: #E4F1EC !important;
    border: 1px solid #9CCFC3 !important;
    border-left: 6px solid #39AFA6 !important;
    padding: 30px 34px !important;
    margin: 18px 0 28px 0 !important;
}

/* FEATURED SKILL INTRO CARD */

div[class*="st-key-kala-feature-card"] {
    background: #E4F1EC !important;
    border: 1px solid #9CCFC3 !important;
    border-left: 5px solid #39AFA6 !important;
    padding: 26px 30px !important;
    margin: 14px 0 24px 0 !important;
}


div[class*="st-key-kala-insight-"] {
    background: #FFFFFF !important;
    border: 1px solid #B7D4CE !important;
    border-top: 4px solid #39AFA6 !important;
    padding: 22px 24px !important;
    margin-bottom: 18px !important;
    min-height: 220px;
    box-sizing: border-box;
}

div[class*="st-key-kala-insight-"] h4 {
    margin-top: 0 !important;
    margin-bottom: 14px !important;
    color: #164E59 !important;
}

div[class*="st-key-kala-insight-"] p {
    line-height: 1.8 !important;
    color: #405B5A !important;
}
</style>
"""