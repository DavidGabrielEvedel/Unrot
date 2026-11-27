import random
import time
import json
import uuid
import streamlit as st
import sympy as sp
import plotly.graph_objects as go
from styles import apply_styles, WILDCARD_CSS, CS_PREP_CSS, TODO_CSS, KALAS_CSS, BUTTON_CSS
from datetime import date, timedelta
from pathlib import Path
from auth import render_auth, logout
from logic import (
    KALA_PROGRESS_PATH,
    load_activities,
    get_daily_greeting,
    get_completed_count,
    load_integrals,
    get_random_integral,
    get_random_exam_integral,
    get_daily_phrasal_verb,
    get_daily_vocabulary,
    get_daily_figure_of_speech,
    get_daily_linux_commands,
    get_random_physics_question,
    get_daily_gita_verse,
    get_daily_life_sciences_questions,
    load_wildcard_questions, 
    get_daily_wildcard_questions,
    load_cs_questions,
    get_daily_cs_questions,
    load_kalas,
    load_json,
    save_json,
    get_week_key,
    get_featured_skill,
    continue_featured_skill
)
apply_styles()
st.markdown(
    f"<style>{BUTTON_CSS}</style>",
    unsafe_allow_html=True
)
import html

@st.fragment(run_every="1s")
def live_timer():

    if st.session_state.mental_maths_end is not None:
        elapsed = st.session_state.mental_maths_end
    else:
        elapsed = time.perf_counter() - st.session_state.mental_maths_start

    minutes, seconds = divmod(int(elapsed), 60)

    st.metric("⏱️ Time Taken", f"{minutes:02d}:{seconds:02d}")
# ----- MENTAL MATHS ENGINE -----

def generate_sum(digits, terms):
    numbers = []

    for i in range(terms):
        number = random.randint(10 ** (digits - 1), (10 ** digits) - 1)

        if i == 0:
            sign = 1
        else:
            sign = random.choice([1, -1])

        numbers.append((sign, number))

    answer = sum(sign * number for sign, number in numbers)

    return numbers, answer


def generate_multiplication():
    a = random.randint(100, 999)
    b = random.randint(10, 99)

    return f"{a} × {b}", a * b


def generate_division():
    dividend = random.randint(1000, 9999)
    divisor = random.randint(10, 99)

    quotient = dividend // divisor
    remainder = dividend % divisor

    return f"{dividend} ÷ {divisor}", f"{quotient},{remainder}"


def generate_alphabet_sum():
    letters = []
    answer = 0

    for i in range(20):
        letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        value = ord(letter) - ord("A") + 1

        if i == 0:
            sign = 1
        else:
            sign = random.choice([1, -1])

        answer += sign * value
        letters.append((sign, letter))

    return letters, answer
def generate_single_digit_chain():

    numbers = []
    running_total = 0

    for _ in range(30):

        if running_total == 0:
            sign = 1
        else:
            sign = random.choice([1, -1])

        if sign == 1:
            number = random.randint(1, 9)
            running_total += number

        else:
            number = random.randint(1, min(9, running_total))
            running_total -= number

        numbers.append((sign, number))

    return numbers, running_total

def generate_mental_maths_set():

    questions = []

    # 1–2: Two-digit, 20-term sums
    for _ in range(2):
        numbers, answer = generate_sum(2, 20)

        questions.append({
            "type": "sum",
            "title": "Double-digit addition & subtraction",
            "numbers": numbers,
            "answer": str(answer),
        })

    # 3–4: Three-digit, 5-term sums
    for _ in range(2):
        numbers, answer = generate_sum(3, 5)

        questions.append({
            "type": "sum",
            "title": "Triple-digit addition & subtraction",
            "numbers": numbers,
            "answer": str(answer),
        })

    # 5–6: Multiplication
    for _ in range(2):
        question, answer = generate_multiplication()

        questions.append({
            "type": "normal",
            "title": "Multiplication",
            "question": question,
            "answer": str(answer),
        })

    # 7–8: Division
    for _ in range(2):
        question, answer = generate_division()

        questions.append({
            "type": "division",
            "title": "Division (Quotient, Remainder)",
            "question": question,
            "answer": answer,
        })

    # 9: Alphabetical sum
    letters, answer = generate_alphabet_sum()

    questions.append({
        "type": "alphabet",
        "title": "Alphabetical Long Sum",
        "numbers": letters,
        "answer": str(answer),
    })
    # 10: 30-line single-digit addition and subtraction
    numbers, answer = generate_single_digit_chain()

    questions.append({
        "type": "sum",
        "title": "Single-digit Long Sum · 30 rows",
        "numbers": numbers,
        "answer": str(answer),
    })
    return questions

def render_mental_maths():

    st.caption("ABACUS MENTAL CALCULATION")
    st.markdown("""
    <style>

    /* Mental Maths answer feedback */
div[data-testid="stAlert"] {
    border-radius: 0px !important;
}

    /* Correct answer — light green */
div[data-testid="stAlert"][kind="success"] {
    background-color: #DDF0E2 !important;
    color: #245C35 !important;
    border: 1px solid #A5CDAE !important;
}

    /* Incorrect answer — light red */
div[data-testid="stAlert"][kind="error"] {
    background-color: #F5DEDE !important;
    color: #8B3030 !important;
    border: 1px solid #D9AAAA !important;
}

</style>
""", unsafe_allow_html=True)
    if "mental_maths_questions" not in st.session_state:
        st.session_state.mental_maths_questions = generate_mental_maths_set()

    questions = st.session_state.mental_maths_questions

    if "mental_maths_start" not in st.session_state:
        st.session_state.mental_maths_start = time.perf_counter()

    if "mental_maths_end" not in st.session_state:
        st.session_state.mental_maths_end = None

    live_timer()

    st.markdown(
        """
        <div style="
            background: #E7F3F1;
            padding: 16px 20px;
            margin: 15px 0 25px 0;
            border-left: 3px solid #087F8C;
        ">
            <span style="font-family: Georgia, serif; color: #18343A;">
                Calculate mentally or with an Abacus. No calculator. No written working.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----- ANSWER CHECKING ENGINE -----

    def check_answer(user_answer, correct_answer, question_type):

        user_answer = user_answer.strip().replace(" ", "")

        if question_type == "division":
            return user_answer == correct_answer

        try:
            return int(user_answer) == int(correct_answer)

        except ValueError:
            return False

    # ----- DISPLAY QUESTIONS -----

    for index, question in enumerate(questions):

        st.markdown("---")

        st.markdown(
            f"**{index + 1:02d}. {question['title']}**"
        )

        if question["type"] == "sum":

            for sign, number in question["numbers"]:
                symbol = "+" if sign == 1 else "−"
                st.markdown(f"`{symbol} {number}`")

        elif question["type"] == "alphabet":

            st.caption("A = 1 · B = 2 · C = 3 · ... · Z = 26")

            for sign, letter in question["numbers"]:
                symbol = "+" if sign == 1 else "−"
                st.markdown(f"`{symbol} {letter}`")

        else:
            st.markdown(f"### {question['question']}")

        # Answer input
        user_answer = st.text_input(
            "Your answer",
            key=f"mental_answer_{index}",
            placeholder=(
                "Quotient, remainder"
                if question["type"] == "division"
                else "Enter your answer"
            ),
        )

        # Individual check button
        if st.button(
            "Check answer",
            key=f"check_mental_{index}",
            use_container_width=True,
        ):

            is_correct = check_answer(
                user_answer,
                question["answer"],
                question["type"],
            )

            st.session_state[f"mental_result_{index}"] = {
                "answer": user_answer.strip().replace(" ", ""),
                "correct": is_correct,
            }

        # Display individual result
        result = st.session_state.get(
            f"mental_result_{index}"
        )

        current_answer = user_answer.strip().replace(" ", "")

        if result and result["answer"] == current_answer:

            if result["correct"]:
                st.success("Correct! Well calculated.")

            else:
                st.error(
                    f"Incorrect. Correct answer: {question['answer']}"
                )

    # ----- CHECK ALL ANSWERS (UNCHANGED FUNCTIONALITY) -----

    st.markdown("---")

    if st.button(
        "Check all answers",
        type="primary",
        use_container_width=True,
    ):

        if st.session_state.mental_maths_end is None:
            st.session_state.mental_maths_end = (
                time.perf_counter() - st.session_state.mental_maths_start
            )

        score = 0

        for index, question in enumerate(questions):

            user_answer = st.session_state.get(
                f"mental_answer_{index}", ""
            )

            is_correct = check_answer(
                user_answer,
                question["answer"],
                question["type"],
            )

            if is_correct:
                score += 1
                st.success(f"Question {index + 1}: Correct!")

            else:
                st.error(
                    f"Question {index + 1}: Incorrect. "
                    f"Correct answer: {question['answer']}"
                )

        st.session_state.mental_maths_score = score

        st.markdown(f"## Your score: {score}/10")

        if score == 10:
            st.balloons()
            st.success("Perfect result!")

        elif score >= 6:
            st.success("Good work. Keep practicing!")

        else:
            st.info("Don't give up. Focus on Accuracy. Speed comes with consistency.")

    # ----- GENERATE NEW SET -----

    if st.button(
        "Generate Different Set",
        use_container_width=True,
    ):

        st.session_state.mental_maths_questions = generate_mental_maths_set()
        st.session_state.mental_maths_start = time.perf_counter()
        st.session_state.mental_maths_end = None

        for index in range(10):
            st.session_state.pop(f"mental_answer_{index}", None)
            st.session_state.pop(f"mental_result_{index}", None)

        st.session_state.pop("mental_maths_score", None)

        st.rerun()
        
# ----- ENGLISH LAB: PHRASAL VERBS -----

def render_phrasal_verb():

    st.caption("ENGLISH LAB · VOCABULARY & EXPRESSION")

    if "active_phrasal_verb" not in st.session_state:
        st.session_state.active_phrasal_verb = get_daily_phrasal_verb()

    entry = st.session_state.active_phrasal_verb

    if not entry:
        st.warning("No phrasal verbs found.")
        return

    st.markdown(
        f"""
        <div style="
            background: #E7F3F1;
            padding: 25px;
            border-left: 4px solid #087F8C;
            margin: 15px 0;
        ">
            <div style="color: #527477; font-size: 12px;">
                {entry['cefr_level']} LEVEL ·
                DIFFICULTY {entry['difficulty_score']}/5
            </div>
            <h1 style="
                font-family: Georgia, serif;
                color: #18343A;
                margin-bottom: 5px;
            ">{entry['phrasal_verb'].title()}</h1>
            <p style="color: #527477;">
                {entry['category'].title()}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Meaning & Usage")

    for index, meaning in enumerate(entry["meanings"], 1):

        st.markdown(f"**Meaning {index}**")

        st.write(meaning["definition"])

        st.markdown(
            f"> {meaning['example']}"
        )

        st.caption(
            f"Register: {meaning['register'].title()} · "
            f"Context: {meaning['context'].title()}"
        )


    with st.expander("Explore linguistic details"):

        st.write(f"**Base verb:** {entry['base_verb']}")

        st.write(
            f"**Particles:** {', '.join(entry['particles'])}"
        )

        st.write(
            f"**Transitivity:** {entry['transitivity']}"
        )

        st.write(
            f"**Separability:** {entry['separability']}"
        )

    st.markdown("### Your Turn")

    st.write(
        "Write an original sentence using this phrasal verb. "
        "Try using it in a professional or academic context."
    )

    st.text_area(
        "Construct your sentence",
        key=f"phrasal_sentence_{entry['id']}",
        height=110,
        placeholder="Write your sentence here..."
    )

    st.markdown("")

    if st.button(
        "Another Phrasal Verb",
        use_container_width=True
    ):
        st.session_state.active_phrasal_verb = get_daily_phrasal_verb()
        st.rerun()

# ----- ENGLISH LAB: ADVANCED VOCABULARY -----

def render_vocabulary():

    st.markdown("## Daily Vocabulary")
    st.caption("THREE WORDS. THREE NEW ADDITIONS TO YOUR VOCABULARY.")

    if "daily_vocabulary" not in st.session_state:
        st.session_state.daily_vocabulary = get_daily_vocabulary()

    entries = st.session_state.daily_vocabulary

    for entry in entries:

        synonyms = " · ".join(entry.get("synonyms", []))

        html_card = f"""
        <div style="
    background-color: #E7F3F1;
    padding: 13px 18px;
    margin-top: 10px;
    margin-bottom: 5px;
    border-left: 3px solid #087F8C;
    border-radius: 0px;
">
        <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    ">
            <span style="
            font-family: Georgia, serif;
            font-size: 25px;
            color: #18343A;
        ">{entry['word'].title()}</span>

        <span style="font-size: 13px; color: #527477;">
            {synonyms}
        </span>
    </div>

        <div style="font-size: 14px; color: #34575A; margin-top: 7px;">
        {entry['definition']}
        </div>

        <div style="font-size: 13px; color: #527477; margin-top: 7px; font-style: italic;">
        {entry['example']}
    </div>
</div>
""" 

        st.html(html_card)
        st.text_area(
            "Write your own sentence",
            key=f"vocabulary_sentence_{entry['id']}",
            height=75,
            placeholder=f"Use '{entry['word']}' in your own sentence..."
        )

def render_figures_of_speech():

    st.subheader("Figure of Speech of the Day")
    st.caption("UNDERSTAND THE LITERARY DEVICE. RECOGNISE IT. USE IT.")

    if "daily_figure" not in st.session_state:
        st.session_state.daily_figure = get_daily_figure_of_speech()

    figure = st.session_state.daily_figure

    if not figure:
        st.warning("No figures of speech found.")
        return

    html_card = f"""
    <div style="
    background-color: #eaf7fa;
    border: 1px solid #42bfc8;
    padding: 22px;
    margin: 12px 0;
    border-radius: 0px;
    color: #173b45;
    ">
    <div style="font-size:12px; letter-spacing:2px; opacity:0.7;">
        {figure['category'].upper()}
    </div>

    <h2 style="margin:10px 0;">
        {figure['name']}
    </h2>

    <div style="font-size:12px; opacity:0.7;">
        DIFFICULTY: {figure['difficulty'].upper()}
    </div>

    <hr style="opacity:0.25;">

    <p><b>Definition</b><br>
    {figure['definition']}</p>

    <p><b>Example</b><br>
    <i>"{figure['example']}"</i></p>

    <p><b>Explanation</b><br>
    {figure['explanation']}</p>

    <p><b>Effect</b><br>
    {figure['effect']}</p>
    </div>
    """

    st.html(html_card)

    if figure.get("related_terms"):
        st.markdown(
            "**Related concepts:** " +
            " · ".join(figure["related_terms"])
        )

    st.markdown("### Your Turn")

    st.text_area(
        "Write your own example using this figure of speech:",
        key=f"figure_sentence_{figure['id']}",
        height=100,
        placeholder="Write your sentence here..."
    )

    st.button(
        "Another Figure of Speech →",
        key="next_figure",
        on_click=lambda: st.session_state.update({
            "daily_figure": get_daily_figure_of_speech()
        })
    )

def render_wildcard():

    st.markdown(
    f"<style>{WILDCARD_CSS}</style>",
    unsafe_allow_html=True
)

    # Load dataset
    if "wildcard_all_questions" not in st.session_state:
        st.session_state.wildcard_all_questions = load_wildcard_questions()

    all_questions = st.session_state.wildcard_all_questions

    if len(all_questions) < 5:
        st.error("Not enough valid questions in wildcard.jsonl.")
        return

    # Initialise today's question set
    if "wildcard_questions" not in st.session_state:
        st.session_state.wildcard_questions = get_daily_wildcard_questions(
            all_questions, 5
        )
        st.session_state.wildcard_version = 0
        st.session_state.wildcard_submitted = False

    questions = st.session_state.wildcard_questions
    version = st.session_state.wildcard_version

    # QUIZ
    if not st.session_state.wildcard_submitted:

        with st.form(key=f"wildcard_form_{version}"):

            for i, q in enumerate(questions):

                with st.container(key=f"wildcard_q_{i}"):

                    st.html(f"""
                        <div class="wildcard-meta">
                            <span>{html.escape(q['cat'])}</span>
                            <span>{html.escape(q['level'])}</span>
                        </div>
                        <div class="wildcard-question">
                            {i + 1}. {html.escape(q['q'])}
                        </div>
                    """)

                    st.radio(
                        "Choose your answer",
                        q["opts"],
                        index=None,
                        key=f"wildcard_answer_{version}_{i}",
                        label_visibility="collapsed"
                    )

            submitted = st.form_submit_button(
                "Check My Answers",
                use_container_width=True,
                type="primary"
            )

        if submitted:

            answers = [
                st.session_state.get(f"wildcard_answer_{version}_{i}")
                for i in range(5)
            ]

            st.session_state.wildcard_answers = answers
            st.session_state.wildcard_submitted = True
            st.rerun()

    # RESULTS AND EXPLANATIONS
    if st.session_state.wildcard_submitted:

        answers = st.session_state.wildcard_answers

        score = sum(
            1 for q, a in zip(questions, answers)
            if a is not None and str(a).strip().casefold() == str(q["ans"]).strip().casefold()
        )

        st.markdown(
            f"""
            <div class="wildcard-heading">Your Results: {score}/5</div>
            <div class="wildcard-subtitle">
                Review your answers and explore the explanations below.
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, (q, selected) in enumerate(zip(questions, answers)):

            correct = (
                selected is not None
                and str(selected).strip().casefold() == str(q["ans"]).strip().casefold()
            )

            status = "CORRECT" if correct else "INCORRECT"
            container_key = (
                f"wildcard_review_correct_{i}"
                if correct
                else f"wildcard_review_incorrect_{i}"
            )

            with st.container(key=container_key):

                st.html(f"""
                    <div class="wildcard-review-label">
                        QUESTION {i + 1} — {status}
                    </div>
                """)

                st.markdown(f"**{q['q']}**")

                st.markdown(
                    f"**Your answer:** {selected if selected is not None else 'Not answered'}"
                )

                if not correct:
                    st.markdown(f"**Correct answer:** {q['ans']}")

                st.markdown(f"**Explanation:** {q['why']}")

                if q.get("extra"):
                    st.markdown(f"**Did you know?** {q['extra']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "↻ Reattempt",
                key="wildcard_reattempt",
                use_container_width=True
            ):
                # Clear previous answers
                st.session_state.wildcard_answers = []

                # Reset submission status
                st.session_state.wildcard_submitted = False

                # Increment version to create fresh radio widgets
                st.session_state.wildcard_version += 1

                st.rerun()

        with col2:
            if st.button(
                "Generate a Different Set",
                key="wildcard_new_set",
                use_container_width=True
            ):
                previous_ids = {q["id"] for q in questions}

                available = [
                    q for q in all_questions
                    if q["id"] not in previous_ids
                ]

                if len(available) < 5:
                    available = all_questions

                new_questions = random.sample(available, 5)

                attempts = 0
                while (
                    {q["id"] for q in new_questions} == previous_ids
                    and attempts < 20
                ):
                    new_questions = random.sample(available, 5)
                    attempts += 1

                st.session_state.wildcard_questions = new_questions
                st.session_state.wildcard_version += 1
                st.session_state.wildcard_answers = []
                st.session_state.wildcard_submitted = False

                st.rerun()
                
# TO-DO LIST

TODO_FILE = Path(__file__).resolve().parent / "data_sources" / "todo_data.json"


def load_todo_data():

    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not TODO_FILE.exists():
        return {
            "sections": ["Personal"],
            "tasks": []
        }

    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_todo_data(data):

    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def render_todo():

    st.markdown(
        f"<style>{TODO_CSS}</style>",
        unsafe_allow_html=True
    )

    data = load_todo_data()

    sections = data["sections"]
    tasks = data["tasks"]

    today = date.today()

    # HEADER
    st.markdown("""
        <div class="todo-eyebrow">PERSONAL ORGANISATION</div>
        <div class="todo-heading">My Tasks.</div>
        <div class="todo-subtitle">
            Make time for what matters.
        </div>
    """, unsafe_allow_html=True)

    completed_tasks = [t for t in tasks if t["completed"]]
    pending_tasks = [t for t in tasks if not t["completed"]]

    st.markdown(
        f"""
        <div class="todo-task-meta">
            {len(completed_tasks):02d} COMPLETED
            &nbsp;&nbsp;·&nbsp;&nbsp;
            {len(pending_tasks):02d} REMAINING
            &nbsp;&nbsp;·&nbsp;&nbsp;
            {len(tasks):02d} TOTAL TASKS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ADD TASK + CREATE SECTION
    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown(
            '<div class="todo-label">+ ADD A TASK</div>',
            unsafe_allow_html=True
        )

        with st.form("todo_add_form", clear_on_submit=True):

            task_title = st.text_input(
                "Task",
                placeholder="What needs to get done?"
            )

            task_section = st.selectbox(
                "Section",
                sections
            )

            has_deadline = st.checkbox("Set a deadline")

            deadline = None

            if has_deadline:
                deadline = st.date_input(
                    "Deadline",
                    value=today,
                    min_value=today
                )

            add_task = st.form_submit_button(
                "Add Task",
                use_container_width=True
            )

            if add_task and task_title.strip():

                tasks.append({
                    "id": str(uuid.uuid4()),
                    "title": task_title.strip(),
                    "section": task_section,
                    "deadline": deadline.isoformat() if deadline else None,
                    "completed": False,
                    "completed_on": None
                })

                save_todo_data(data)
                st.rerun()

    with col2:

        st.markdown(
            '<div class="todo-label">+ CREATE A SECTION</div>',
            unsafe_allow_html=True
        )

        with st.form("todo_section_form", clear_on_submit=True):

            new_section = st.text_input(
                "Folder name",
                placeholder="e.g. College, Work, Home"
            )

            create_section = st.form_submit_button(
                "Create Section",
                use_container_width=True
            )

            if create_section and new_section.strip():

                if new_section.strip() not in sections:

                    sections.append(new_section.strip())
                    save_todo_data(data)
                    st.rerun()

                else:
                    st.warning("This section already exists.")

    st.divider()

    # UPCOMING TASKS + CALENDAR
    st.markdown(
        '<div class="todo-label">UPCOMING</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.4, 1])

    upcoming = sorted(
        [
            t for t in tasks
            if not t["completed"]
            and t["deadline"]
            and date.fromisoformat(t["deadline"]) >= today
        ],
        key=lambda t: t["deadline"]
    )

    with col1:

        if upcoming:

            for task in upcoming[:4]:

                deadline_date = date.fromisoformat(task["deadline"])

                st.markdown(
                    f"""
                    <div class="todo-task-meta">
                        {deadline_date.strftime("%d %b %Y").upper()}
                        &nbsp;·&nbsp; {task["section"].upper()}
                    </div>
                    <div class="todo-task-title">
                        {task["title"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("<br>", unsafe_allow_html=True)

        else:

            st.markdown(
                '<div class="todo-subtitle">No upcoming deadlines.</div>',
                unsafe_allow_html=True
            )

    with col2:

        selected_date = st.date_input(
            "Calendar",
            value=today,
            key="todo_calendar"
        )

        selected_tasks = [
            t for t in tasks
            if t["deadline"] == selected_date.isoformat()
            and not t["completed"]
        ]

        st.caption(
            f"{len(selected_tasks)} task(s) due on "
            f"{selected_date.strftime('%d %b %Y')}."
        )

        for task in selected_tasks:

            st.markdown(
                f"• {task['title']}",
                unsafe_allow_html=True
            )

    st.divider()

    # TASK SECTIONS

    st.markdown(
        '<div class="todo-label">YOUR TASKS</div>',
        unsafe_allow_html=True
    )

    selected_section = st.selectbox(
        "View section",
        ["All Sections"] + sections,
        key="todo_section_filter"
    )

    filtered_tasks = [
        t for t in tasks
        if selected_section == "All Sections"
        or t["section"] == selected_section
    ]

    active_tasks = [t for t in filtered_tasks if not t["completed"]]
    finished_tasks = [t for t in filtered_tasks if t["completed"]]

    # Pending tasks

    for task in active_tasks:

        with st.container(key=f"todo_card_{task['id']}"):

            col1, col2, col3 = st.columns([5, 1.4, 0.7])

            with col1:

                st.markdown(
                    f"""
                    <div class="todo-task-title">
                        {task["title"]}
                    </div>
                    <div class="todo-task-meta">
                        {task["section"].upper()}
                        {" · " + task["deadline"] if task["deadline"] else ""}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "Complete",
                    key=f"todo_complete_{task['id']}"
                ):

                    task["completed"] = True
                    task["completed_on"] = today.isoformat()

                    save_todo_data(data)
                    st.rerun()

            with col3:

                if st.button(
                    "×",
                    key=f"todo_delete_{task['id']}"
                ):

                    data["tasks"] = [
                        t for t in data["tasks"]
                        if t["id"] != task["id"]
                    ]

                    save_todo_data(data)
                    st.rerun()

    if not active_tasks:

        st.markdown(
            '<div class="todo-subtitle">Nothing pending. Enjoy the breathing room.</div>',
            unsafe_allow_html=True
        )

    # Completed tasks

    if finished_tasks:

        with st.expander(
            f"COMPLETED · {len(finished_tasks)}"
        ):

            for task in finished_tasks:

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.markdown(
                        f"""
                        <div class="todo-completed">
                            {task["title"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:

                    if st.button(
                        "Delete",
                        key=f"todo_delete_done_{task['id']}"
                    ):

                        data["tasks"] = [
                            t for t in data["tasks"]
                            if t["id"] != task["id"]
                        ]

                        save_todo_data(data)
                        st.rerun()

    st.divider()

    # ACTIVITY HEATMAP
    st.markdown(
        '<div class="todo-label">YOUR CONSISTENCY</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="todo-subtitle">Every completed task adds up.</div>',
        unsafe_allow_html=True
    )

    # Last 35 days

    start_date = today - timedelta(days=34)

    activity = {}

    for task in tasks:

        completed_on = task.get("completed_on")

        if completed_on:

            activity[completed_on] = (
                activity.get(completed_on, 0) + 1
            )

    # Align calendar to Monday

    calendar_start = start_date - timedelta(
        days=start_date.weekday()
    )

    dates = [
        calendar_start + timedelta(days=i)
        for i in range(42)
    ]

    z_values = []
    hover_text = []

    for week in range(6):

        row_values = []
        row_hover = []

        for day in range(7):

            current_date = dates[week * 7 + day]

            count = activity.get(current_date.isoformat(), 0)

            row_values.append(count)

            row_hover.append(
                f"{current_date.strftime('%d %b %Y')}<br>"
                f"{count} task(s) completed"
            )

        z_values.append(row_values)
        hover_text.append(row_hover)

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            y=["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            colorscale=[
                [0, "#E9EDE9"],
                [0.25, "#C5DAD5"],
                [0.5, "#91B9B2"],
                [0.75, "#528D8B"],
                [1, "#173D50"]
            ],
            showscale=False,
            xgap=5,
            ygap=5
        )
    )

    fig.update_layout(
        height=210,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#F8F7F2",
        plot_bgcolor="#F8F7F2",
        font=dict(
            family="Consolas",
            size=10,
            color="#527487"
        ),
        yaxis=dict(
            autorange="reversed",
            showgrid=False,
            zeroline=False
        ),
        xaxis=dict(
            side="top",
            showgrid=False,
            zeroline=False
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '<div class="todo-task-meta">LAST 35 DAYS · DAILY COMPLETION ACTIVITY</div>',
        unsafe_allow_html=True
    )
    
#LIFE SCIENCES
from styles import LIFE_SCIENCES_CSS
def render_life_sciences():

    st.html(LIFE_SCIENCES_CSS)

    st.html("""
    <div class="life-header">
        <div class="life-title">Life Sciences</div>
        <div class="life-subtitle">
            BIOLOGY · CHEMISTRY · BIOCHEMISTRY · BIOTECH
        </div>
    </div>
    """)

    st.caption(
        "10 questions. Life disciplines. Something new everyday."
        
    )

    try:
        biology, chemistry = get_daily_life_sciences_questions()

    except Exception as e:
        st.error(f"Unable to load question bank: {e}")
        return

    questions = biology + chemistry

    st.html("""
    <div class="life-section">
        01 · BIOLOGY
    </div>
    """)
#QUIZ FORM

    with st.form("life_sciences_quiz"):

        answers = {}

        for i, question in enumerate(questions):

            subject = "BIOLOGY" if i < 5 else "CHEMISTRY"

            number = i + 1

            topic = html.escape(
                str(question.get("topic") or subject)
            )

            st.html(f"""
            <div class="life-question-card">

            <div class="life-question-number">
            QUESTION {number:02d} · {subject}
            </div>

            <div class="life-topic">
            {topic}
            </div>

            </div>
            """)

            st.markdown(
    question["question"],
    unsafe_allow_html=False
)

            option_labels = [
                f"{key}. {question['options'][key]}"
                for key in ["A", "B", "C", "D"]
            ]

            answers[question["id"]] = st.radio(
                "Select your answer:",
                option_labels,
                key=f"life_answer_{i}",
                index=None,
                label_visibility="collapsed"
            )

            if i == 4:
                st.html("""
                <div class="life-section">
                    02 · CHEMISTRY
                </div>
                """)

        submitted = st.form_submit_button(
            "SUBMIT QUIZ",
            use_container_width=True,
            type="primary"
        )

   
    # RESULTS

    if submitted:

        if any(answer is None for answer in answers.values()):

            st.warning(
                "Please answer all 10 questions before submitting."
            )

            return

        biology_score = 0
        chemistry_score = 0

        results = []

        for i, question in enumerate(questions):

            selected = answers[question["id"]]

            selected_letter = selected.split(".", 1)[0]

            correct_letter = question["correct_answer"]

            is_correct = selected_letter == correct_letter

            if is_correct:

                if i < 5:
                    biology_score += 1
                else:
                    chemistry_score += 1

            results.append({
                "question": question,
                "selected": selected_letter,
                "correct": correct_letter,
                "is_correct": is_correct
            })

        total_score = biology_score + chemistry_score

        # Save results in session state.
        st.session_state["life_sciences_results"] = results
        st.session_state["life_sciences_score"] = total_score
        st.session_state["life_biology_score"] = biology_score
        st.session_state["life_chemistry_score"] = chemistry_score

    
    # DISPLAY SAVED RESULTS
   
    if "life_sciences_results" in st.session_state:

        results = st.session_state["life_sciences_results"]

        biology_score = st.session_state["life_biology_score"]
        chemistry_score = st.session_state["life_chemistry_score"]
        total_score = st.session_state["life_sciences_score"]

        st.html("""
<div class="life-section">
    03 · ANSWER REVIEW
</div>
""")

        for i, result in enumerate(results):

            question = result["question"]

            selected = result["selected"]
            correct = result["correct"]

            correct_answer = html.escape(
                question["options"][correct]
        )

            selected_answer = html.escape(
                question["options"][selected]
    )

            if result["is_correct"]:
                title = "✓ CORRECT"
                result_class = "life-correct"
            else:
                title = "✕ INCORRECT"
                result_class = "life-incorrect"

            card_type = "correct" if result["is_correct"] else "incorrect"

            with st.container(key=f"life_review_{card_type}_{i}"):

                st.markdown(f"**{title}**")

                st.markdown(
                    f"**Your answer:** {selected}. {question['options'][selected]}"
                )

                st.markdown(
                    f"**Correct answer:** {correct}. {question['options'][correct]}"
                )

                st.markdown("**Explanation:**")

                st.markdown(
                    question.get("explanation", ""),
                    unsafe_allow_html=False
                )
        # FINAL SCORE
        st.html(f"""
        <div class="life-score-card">

            <div class="life-score-label">
                YOUR DAILY LIFE SCIENCES SCORE
            </div>

            <div class="life-score-number">
                {total_score}/10
            </div>

            <div class="life-score-caption">
                {"Excellent work!" if total_score >= 8 else
                 "Good effort! Keep learning." if total_score >= 5 else
                 "Keep practising. You'll improve."}
            </div>

        </div>
        """)

        col1, col2 = st.columns(2)

        with col1:

            st.html(f"""
            <div class="life-stat">
                <div class="life-stat-label">BIOLOGY</div>
                <div class="life-stat-value">
                    {biology_score}/5
                </div>
            </div>
            """)

        with col2:

            st.html(f"""
            <div class="life-stat">
                <div class="life-stat-label">CHEMISTRY</div>
                <div class="life-stat-value">
                    {chemistry_score}/5
                </div>
            </div>
            """)

        if st.button("RETAKE TODAY'S QUIZ", use_container_width=True):

            for i in range(10):
                st.session_state.pop(f"life_answer_{i}", None)

            st.session_state.pop("life_sciences_results", None)
            st.session_state.pop("life_sciences_score", None)
            st.session_state.pop("life_biology_score", None)
            st.session_state.pop("life_chemistry_score", None)

            st.rerun()
def render_cs_math(content):
    if not content:
        return

    content = str(content)

    # Convert standard LaTeX delimiters to Streamlit-compatible delimiters
    content = content.replace(r"\(", "$")
    content = content.replace(r"\)", "$")
    content = content.replace(r"\[", "$$")
    content = content.replace(r"\]", "$$")

    st.markdown(content)          
def render_cs_prep():

    st.markdown(
        f"<style>{CS_PREP_CSS}</style>",
        unsafe_allow_html=True
    )

    # Load question bank
    if "cs_all_questions" not in st.session_state:
        st.session_state.cs_all_questions = load_cs_questions()

    all_questions = st.session_state.cs_all_questions

    if len(all_questions) < 7:
        st.error("The question bank must contain at least 7 questions.")
        return

    # Fixed daily question set
    if "cs_questions" not in st.session_state:
        st.session_state.cs_questions = get_daily_cs_questions(
        all_questions, 7
        )
        st.session_state.cs_version = 0
        st.session_state.cs_submitted = False

    questions = st.session_state.cs_questions
    version = st.session_state.cs_version

    # PAGE INTRODUCTION
    st.markdown("""
        <div class="cs-eyebrow">
            COMPUTER SCIENCE · GATE PREPARATION
        </div>
        <div class="cs-daily-label">
            TODAY'S QUESTION SET &nbsp;·&nbsp;
            07 QUESTIONS &nbsp;·&nbsp; DAILY PRACTICE
        </div>
    """, unsafe_allow_html=True)

    # QUIZ
    if not st.session_state.cs_submitted:

        with st.form(key=f"cs_form_{version}"):

            for i, q in enumerate(questions):

                with st.container(key=f"cs_q_{i}"):

                    st.markdown(
                        f"""
                        <div class="cs-meta">
                            <span>{html.escape(q.get('subject', 'COMPUTER SCIENCE'))}</span>
                            <span>{q.get('question_type', 'MCQ')} · {q.get('marks', 1)} MARK</span>
                        </div>
                        <div class="cs-topic">
                            {html.escape(q.get('topic', ''))}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"**Q.{i + 1:02d}**"
                    )

                    render_cs_math(q["question"])

                    qtype = q.get("question_type", "MCQ").upper()
                    options = q.get("options", {})

                    if qtype == "MCQ":

                        choices = [
                            f"{key}. {value}"
                            for key, value in options.items()
                        ]

                        st.radio(
                            "Choose one answer",
                            choices,
                            index=None,
                            key=f"cs_answer_{version}_{i}",
                            label_visibility="collapsed"
                        )

                    elif qtype == "MSQ":

                        choices = [
                            f"{key}. {value}"
                            for key, value in options.items()
                        ]

                        st.multiselect(
                            "Select all correct answers",
                            choices,
                            key=f"cs_answer_{version}_{i}",
                            placeholder="Select all that apply"
                        )

                    elif qtype == "NAT":

                        st.text_input(
                            "Enter your numerical answer",
                            key=f"cs_answer_{version}_{i}",
                            placeholder="Enter numerical value"
                        )

            submitted = st.form_submit_button(
                "Check My Answers",
                use_container_width=True,
                type="primary"
            )

        if submitted:

            answers = []

            for i, q in enumerate(questions):

                answer = st.session_state.get(
                    f"cs_answer_{version}_{i}"
                )

                qtype = q.get("question_type", "MCQ").upper()

                if qtype in ("MCQ", "MSQ") and answer:
                    answer = [
                        item.split(".", 1)[0].strip()
                        for item in (
                            answer if isinstance(answer, list) else [answer]
                        )
                    ]

                answers.append(answer)

            st.session_state.cs_answers = answers
            st.session_state.cs_submitted = True
            st.rerun()

            # RESULTS
    if st.session_state.cs_submitted:

        answers = st.session_state.cs_answers

        def check_cs_answer(q, selected):

            correct = q.get("correct_answer", [])
            qtype = q.get("question_type", "MCQ").upper()

            if not correct or selected is None or selected == [] or selected == "":
                return False

            if qtype in ("MCQ", "MSQ"):
                return set(selected) == set(correct)

            if qtype == "NAT":
                try:
                    return abs(
                        float(str(selected).strip()) - float(correct[0])
                    ) <= 0.01
                except (ValueError, TypeError, IndexError):
                    return False

            return False

        def format_cs_answer(q, answer):

            if answer is None or answer == [] or answer == "":
                return "Not attempted"

            qtype = q.get("question_type", "MCQ").upper()
            options = q.get("options", {})

            if qtype in ("MCQ", "MSQ"):
                if not isinstance(answer, list):
                    answer = [answer]

                return " · ".join(
                    f"{key}. {options.get(key, 'Option unavailable')}"
                    for key in answer
                )

            if isinstance(answer, list):
                return str(answer[0]) if answer else "Not attempted"

            return str(answer)

        results = [
            check_cs_answer(q, a)
            for q, a in zip(questions, answers)
        ]

        attempted = sum(
            1 for a in answers if a is not None and a != [] and a != ""
        )

        correct_count = sum(results)
        incorrect_count = attempted - correct_count
        unattempted_count = 7 - attempted

        # PERFORMANCE HEADER
        st.markdown(
            f"""
            <div class="cs-results-eyebrow">
                DAILY PRACTICE · PERFORMANCE REPORT
            </div>

            <div class="cs-score">
                {correct_count:02d}
                <span>/ 07</span>
            </div>

            <div class="cs-results-subtitle">
                QUESTIONS ANSWERED CORRECTLY
            </div>

            <div class="cs-performance-line">
                <span>{correct_count} CORRECT</span>
                <span>{incorrect_count} INCORRECT</span>
                <span>{unattempted_count} UNATTEMPTED</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # PROGRESS BAR
        st.progress(correct_count / 7)


        # INDIVIDUAL QUESTION REVIEWS
        for i, (q, selected, correct) in enumerate(
            zip(questions, answers, results)
        ):

            attempted_question = (
                selected is not None
                and selected != []
                and selected != ""
            )

            if not attempted_question:
                status = "NOT ATTEMPTED"
                container_key = f"cs_review_unattempted_{i}"

            elif correct:
                status = "CORRECT"
                container_key = f"cs_review_correct_{i}"

            else:
                status = "INCORRECT"
                container_key = f"cs_review_incorrect_{i}"

            options = q.get("options", {})
            correct_answers = q.get("correct_answer", [])

            with st.container(key=container_key):

                st.html(f"""
                    <div class="cs-review-label">
                        QUESTION {i + 1:02d}
                        &nbsp;—&nbsp; {status}
                    </div>

                    <div class="cs-review-meta">
                        {html.escape(q.get('subject', 'COMPUTER SCIENCE'))}
                        &nbsp;·&nbsp;
                        {html.escape(q.get('question_type', 'MCQ'))}
                        &nbsp;·&nbsp;
                        {q.get('marks', 1)} MARK
                    </div>
                """)

                st.markdown(
                    '<div class="cs-review-section">QUESTION</div>',
                    unsafe_allow_html=True
                )

                render_cs_math(q["question"])

                # YOUR ANSWER
                st.markdown(
                    '<div class="cs-review-section">YOUR RESPONSE</div>',
                    unsafe_allow_html=True
                )

                render_cs_math(format_cs_answer(q, selected))

                # CORRECT ANSWER
                if correct_answers:

                    correct_display = format_cs_answer(
                        q, correct_answers
                    )

                    render_cs_math(correct_display)

                    st.markdown(
                        f'<div class="cs-review-answer">{html.escape(correct_display)}</div>',
                        unsafe_allow_html=True
                    )

                # WORKED SOLUTION
                if q.get("solution"):

                    st.markdown(
                        '<div class="cs-review-section">WORKED SOLUTION</div>',
                        unsafe_allow_html=True
                    )

                    render_cs_math(q["solution"])
                # CONCEPTUAL EXPLANATION
                if q.get("explanation"):

                    st.markdown(
                        '<div class="cs-review-section">KEY CONCEPT</div>',
                        unsafe_allow_html=True
                    )

                    render_cs_math(q["explanation"])

        st.markdown("")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "↻ Reattempt",
                key="cs_reattempt",
                use_container_width=True
            ):
                st.session_state.cs_answers = []
                st.session_state.cs_submitted = False
                st.session_state.cs_version += 1
                st.rerun()

        with col2:
            st.markdown(
                '<div class="cs-set-note">YOUR DAILY SET · 07 QUESTIONS</div>',
                unsafe_allow_html=True
            )
# ----- Easier ISC / JEE Integral Alternative -----

def render_exam_integral():

    st.markdown("""
        <div style="
            margin-top: 35px;
            padding-top: 22px;
            border-top: 1px solid #C8D9D8;
        ">
            <h3 style="
                font-family: Georgia, serif;
                font-size: 25px;
                color: #18343A;
                font-weight: normal;
                margin-bottom: 5px;
            ">
                Easier Alternative
            </h3>
            <p style="
                font-family: Georgia, serif;
                font-size: 14px;
                color: #668083;
                font-style: italic;
            ">
                ISC & JEE · Previous Year Questions
            </p>
        </div>
    """, unsafe_allow_html=True)

    if "exam_integral" not in st.session_state:
        st.session_state.exam_integral = get_random_exam_integral()

    integral = st.session_state.exam_integral

    if integral is None:
        st.warning("No exam questions found.")
        return

    exam = integral.get("exam", "Exam")
    year = integral.get("year")

    metadata = exam
    if year:
        metadata += f" · {year}"

    st.caption(metadata)
    st.latex(integral["question_latex"])

    if st.button(
        "Different Integral",
        key="different_exam_integral",
        use_container_width=True
    ):
        st.session_state.exam_integral = get_random_exam_integral()
        st.rerun()
 
 # ---------- PHYSICS ----------

import html


import html
import streamlit as st
from logic import load_physics_questions


def render_physics():

    # ---------- SESSION STATE ----------

    if "physics_question" not in st.session_state:
        st.session_state.physics_question = get_random_physics_question()

    question = st.session_state.physics_question

    question_id = question["id"]

    if "physics_checked" not in st.session_state:
        st.session_state.physics_checked = False

    # ---------- QUESTION CARD ----------

    question_card = f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #DCE5E5;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 16px;
        color: #18343A;
    ">

        <div style="
            color: #087F8C;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
        ">
            PHYSICS · {html.escape(question["subject"].upper())}
        </div>

        <div style="
            font-size: 19px;
            font-weight: 600;
            line-height: 1.6;
        ">
            {html.escape(question["question"])}
        </div>

    </div>
    """

    st.html(question_card)

    # ---------- MCQ OPTIONS ----------

    letters = ["A", "B", "C", "D"]

    options = [
        f"{letter}. {choice}"
        for letter, choice in zip(letters, question["choices"])
    ]

    selected_option = st.radio(
        "Choose your answer",
        options,
        index=None,
        key=f"physics_option_{question_id}",
        disabled=st.session_state.physics_checked,
        label_visibility="collapsed"
    )

    # ---------- BUTTONS ----------

    col1, col2 = st.columns(2)

    with col1:
        check = st.button(
            "Check Answer",
            use_container_width=True,
            type="secondary",
            disabled=st.session_state.physics_checked
        )

    with col2:
        different = st.button(
            "Different Question →",
            use_container_width=True
        )

    # ---------- CHECK ANSWER ----------

    if check:

        if selected_option is None:
            st.warning("Select an option first.")

        else:
            selected_letter = selected_option[0]
            st.session_state.physics_checked = True
            st.session_state.physics_user_answer = selected_letter
            st.rerun()

    # ---------- RESULT ----------

    if st.session_state.physics_checked:

        correct_answer = question["answer"].upper()
        user_answer = st.session_state.physics_user_answer

        correct_choice = question["choices"][letters.index(correct_answer)]

        if user_answer == correct_answer:

            result_color = "#E8F5EC"
            border_color = "#79B994"
            result_title = "Correct!"
            result_message = "Well done. You got the answer right."

        else:

            result_color = "#FCEBE8"
            border_color = "#D98C83"
            result_title = "Incorrect!"
            result_message = f"The correct answer is {correct_answer}."

        result_card = f"""
        <div style="
            background: {result_color};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 20px;
            margin-top: 18px;
            color: #18343A;
        ">

            <div style="font-size: 18px; font-weight: 700;">
                {result_title}
            </div>

            <div style="font-size: 14px; margin-top: 6px;">
                {result_message}
            </div>

            <div style="
                border-top: 1px solid {border_color};
                margin-top: 14px;
                padding-top: 14px;
                font-size: 14px;
            ">
                <strong>Correct option:</strong>
                {correct_answer}. {html.escape(correct_choice)}
            </div>

            <div style="
                margin-top: 14px;
                font-size: 14px;
                line-height: 1.7;
            ">
                <strong>Solution & Explanation</strong><br><br>
                {html.escape(question["explanation"])}
            </div>

        </div>
        """

        st.html(result_card)

    # ---------- DIFFERENT QUESTION ----------

    if different:

        questions = load_physics_questions()

        available = [
        q for q in questions
        if q["id"] != question_id
        ]

        if available:
            st.session_state.physics_question = random.choice(available)
            st.session_state.physics_checked = False

            st.session_state.pop("physics_user_answer", None)

            st.rerun() 
            
import json
import streamlit as st
from pathlib import Path


# ==========================================
# DSA DATA LOADER

@st.cache_data
def load_neetcode_data():

    filepath = Path(__file__).parent / "data_sources" / "neetcode_150.jsonl"

    problems = []

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                problems.append(json.loads(line))

    return problems


# ==========================================
# DSA PAGE
# ==========================================

def render_dsa():

    problems = load_neetcode_data()

    st.markdown("""
    <div class="dsa-header">
        <div class="dsa-eyebrow">UNROT · DAILY PRACTICE</div>
        <div class="dsa-title">Data Structures & Algorithms</div>
        <div class="dsa-subtitle">
            Understand the pattern. Learn the approach. Master the problem.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CATEGORY SELECTION

    categories = list(dict.fromkeys(
        p["category"] for p in problems
    ))

    category = st.selectbox(
        "SELECT A CATEGORY",
        categories,
        key="dsa_category"
    )

    category_problems = [
        p for p in problems
        if p["category"] == category
    ]

    st.caption(
        f"{len(category_problems)} problems · {category}"
    )

    # PROBLEM SELECTION

    problem_names = [
        p["problem_name"] for p in category_problems
    ]

    selected_name = st.selectbox(
        "SELECT A PROBLEM",
        problem_names,
        key="dsa_problem"
    )

    problem = next(
        p for p in category_problems
        if p["problem_name"] == selected_name
    )

    st.divider()

    # PROBLEM HEADER

    st.markdown(f"""
    <div class="dsa-problem-header">
        <span class="dsa-problem-title">
            {problem["problem_name"]}
        </span>
        <span class="dsa-difficulty">
            {problem["difficulty"]}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f'{problem["category"]}  ·  {problem["pattern"]}'
    )

    # PROBLEM STATEMENT

    st.markdown("### Problem")

    st.markdown(problem["question"])

    # EXAMPLES

    st.markdown("### Examples")

    for i, example in enumerate(problem["examples"], 1):

        with st.container(border=True):

            st.markdown(f"**Example {i}**")

            st.code(
                f'Input: {example["input"]}\n'
                f'Output: {example["output"]}',
                language="text"
            )

            if example.get("explanation"):
                st.caption(example["explanation"])

    # CONSTRAINTS

    with st.expander("Constraints"):

        for constraint in problem["constraints"]:
            st.markdown(f"- {constraint}")

    st.divider()

    # LEARNING MATERIAL

    st.markdown("### Learn the Problem")

    with st.expander("01 · Theory & Key Concepts"):

        st.markdown(problem["theory"])

    with st.expander("02 · Approach & Algorithm"):

        st.markdown(problem["approach"])

        st.markdown("**Algorithm**")

        for step in problem["algorithm"]:
            st.markdown(f"- {step}")

    with st.expander("03 · Step-by-Step Walkthrough"):

        st.markdown(problem["solution"])

    with st.expander("04 · C++17 Solution"):

        st.code(
            problem["cpp_code"],
            language="cpp"
        )

    with st.expander("05 · Code Explanation"):

        st.markdown(problem["code_explanation"])

    with st.expander("06 · Complexity Analysis"):

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Time Complexity",
                problem["time_complexity"]
            )

        with col2:
            st.metric(
                "Space Complexity",
                problem["space_complexity"]
            )

        st.markdown(problem["complexity_explanation"])

    with st.expander("07 · Edge Cases"):

        for edge in problem["edge_cases"]:
            st.markdown(f"- {edge}")

    # EXTERNAL LINKS

    st.markdown("### Practice Further")

    col1, col2 = st.columns(2)

    with col1:
        st.link_button(
            "LeetCode ↗",
            problem["leetcode_link"],
            use_container_width=True
        )

    with col2:
        st.link_button(
            "NeetCode ↗",
            problem["neetcode_link"],
            use_container_width=True
        )
BASE_DIR = Path(__file__).resolve().parent

KALAS_PATH = BASE_DIR / "data_sources" / "skills.jsonl"
KALA_PROGRESS_PATH = BASE_DIR / "data_sources" / "kala_progress.json"
KALA_SCHEDULE_PATH = BASE_DIR / "data_sources" / "kala_schedule.json"
def get_progress():

    return load_json(KALA_PROGRESS_PATH, {})


def update_progress(skill_id, status):

    progress = get_progress()

    progress[skill_id] = status

    save_json(KALA_PROGRESS_PATH, progress)


def get_skill_status(skill):

    progress = get_progress()

    return progress.get(skill["id"], "Not started")

# REUSABLE CONTENT RENDERERS

def render_list(items):

    if not items:
        st.caption("No information available.")

    elif isinstance(items, list):

        for item in items:
            st.markdown(f"- {item}")

    else:
        st.write(items)


def render_content_section(title, content):

    if not content:
        return

    st.markdown(
        f"""
        <div class="kala-content-section">
            <div class="kala-detail-label">LEARNING MATERIAL</div>
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if isinstance(content, list):
        render_list(content)
    else:
        st.write(content)


def render_introduction(introduction):

    st.markdown("### Understanding the Skill")

    sections = [
        ("Overview", "overview"),
        ("What It Involves", "what_it_involves"),
        ("Why It Matters", "importance"),
        ("Modern Relevance", "modern_relevance")
    ]

    for title, key in sections:

        content = introduction.get(key)

        if content:

            st.markdown(f"#### {title}")
            st.write(content)

    applications = introduction.get("applications", [])

    if applications:

        st.markdown("#### Real-World Applications")

        render_list(applications)


def render_learning_objectives(objectives):

    st.markdown("### What You Will Learn")

    render_list(objectives)


def render_tutorial(tutorial):

    st.markdown("### The Learning Framework")

    sections = [
        ("01 · Foundations", "foundations"),
        ("02 · Essential Knowledge", "essential_knowledge"),
        ("03 · Practical Methods", "practical_methods"),
        ("04 · Common Mistakes", "common_mistakes"),
        ("05 · Intermediate Development", "intermediate_development"),
        ("06 · Advanced Exploration", "advanced_exploration")
    ]

    for title, key in sections:

        content = tutorial.get(key)

        if not content:
            continue

        with st.expander(title, expanded=(key == "foundations")):

            if isinstance(content, list):
                render_list(content)
            else:
                st.write(content)


def render_exercises(exercises):

    st.markdown("### Put the Skill into Practice")

    for index, exercise in enumerate(exercises, 1):

        with st.expander(
            f"{index:02d} · {exercise.get('title', 'Exercise')}"
        ):

            st.markdown("**Instructions**")
            st.write(exercise.get("instructions", ""))

            st.markdown("**Expected Output**")
            st.write(exercise.get("expected_output", ""))


def render_weekly_challenge(challenge):

    if not challenge:
        return

    st.markdown(
        f"""
        <div class="kala-challenge">
            <div class="kala-detail-label">YOUR WEEKLY CHALLENGE</div>
            <h2>{challenge.get('title', 'Weekly Challenge')}</h2>
            <p>{challenge.get('objective', '')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Estimated Time**")
        st.write(challenge.get("estimated_time", "Not specified"))

    with col2:
        st.markdown("**Difficulty**")
        st.write(challenge.get("difficulty", "Not specified"))

    st.markdown("#### Instructions")
    render_list(challenge.get("instructions", []))

    st.markdown("#### Tools Required")
    render_list(challenge.get("tools_required", []))

    st.markdown("#### Expected Output")
    st.write(challenge.get("expected_output", ""))

    st.markdown("#### Success Criteria")
    render_list(challenge.get("success_criteria", []))


def render_classical_connection(connection):

    if not connection:
        return

    st.markdown("### Classical Connection")

    st.write(f"**Text:** {connection.get('text_name', 'Not specified')}")

    st.write(
        f"**Reference:** {connection.get('verse_reference', 'Not specified')}"
    )

    verse = connection.get("verse")

    if verse:

        st.markdown(
            f"""
            <div class="kala-verse">
                <div class="kala-verse-text">{verse}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if connection.get("transliteration"):
        st.markdown("**Transliteration**")
        st.write(connection["transliteration"])

    if connection.get("translation"):
        st.markdown("**Translation**")
        st.write(connection["translation"])

    if connection.get("explanation"):
        st.markdown("**Interpretation**")
        st.write(connection["explanation"])


def render_traditional_connection(connection):

    if not connection:
        return

    st.markdown("### Traditional Kala Connection")

    st.write(f"**Reference:** {connection.get('reference', '')}")

    st.write(
        f"**Relationship:** {connection.get('relationship', '')}"
    )

    st.write(connection.get("explanation", ""))

    if connection.get("historical_source"):

        st.caption(
            f"Historical source: {connection['historical_source']}"
        )


def render_resources(resources):

    st.markdown("### Learning Resources")

    for resource in resources:

        name = resource.get("name", "Resource")
        url = resource.get("url", "")
        description = resource.get("description", "")

        st.markdown(
            f"""
            <div class="kala-resource">
                <a href="{url}" target="_blank">{name} ↗</a>
                <p>{description}</p>
                <small>
                    {resource.get('type', '')}
                    &nbsp; | &nbsp;
                    {resource.get('level', '')}
                    &nbsp; | &nbsp;
                    {resource.get('cost', '')}
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_further_exploration(exploration):

    if not exploration:
        return

    st.markdown("### Beyond the Fundamentals")

    if exploration.get("interdisciplinary_connection"):

        st.markdown("**Interdisciplinary Connection**")
        st.write(exploration["interdisciplinary_connection"])

    if exploration.get("advanced_project"):

        st.markdown("**Advanced Project**")
        st.write(exploration["advanced_project"])


def render_questions(questions):

    if questions:

        st.markdown("### Questions to Ponder")

        render_list(questions)

# COMPLETE SKILL EXPERIENCE

def render_skill_detail(skill, from_featured=False):

    if st.button("← BACK TO THE 128 KALAS", key="back_to_kalas"):

        st.session_state.pop("selected_kala_id", None)
        st.rerun()

    st.markdown(
        f"""
        <div class="kala-eyebrow">
            KALA {skill['number']:03} / {skill['category']}
        </div>

        <h1>{skill['name']}</h1>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        f"{skill['subcategory']} · {skill['difficulty']}"
    )

    # PROGRESS CONTROL

    current_status = get_skill_status(skill)

    status_options = [
        "Not started",
        "In progress",
        "Completed"
    ]

    selected_status = st.selectbox(
        "Learning progress",
        status_options,
        index=status_options.index(current_status),
        key=f"status_{skill['id']}"
    )

    if selected_status != current_status:
        update_progress(skill["id"], selected_status)
        st.rerun()

    # CONTENT

    st.divider()

    render_introduction(skill.get("introduction", {}))

    st.divider()

    render_learning_objectives(
        skill.get("learning_objectives", [])
    )

    st.divider()

    render_tutorial(skill.get("tutorial", {}))

    st.divider()

    render_exercises(
        skill.get("practical_exercises", [])
    )

    st.divider()

    render_weekly_challenge(
        skill.get("weekly_challenge", {})
    )

    st.divider()

    render_classical_connection(
        skill.get("classical_connection")
    )

    render_traditional_connection(
        skill.get("traditional_kala_connection")
    )

    st.divider()

    render_resources(
        skill.get("resources", [])
    )

    st.divider()

    render_questions(
        skill.get("questions_to_ponder", [])
    )

    render_further_exploration(
        skill.get("further_exploration", {})
    )

    # RELATED SKILLS

    related_ids = skill.get(
        "further_exploration", {}
    ).get("related_skills", [])

    if related_ids:

        all_skills = load_kalas()

        related = [
            s for s in all_skills
            if s["id"] in related_ids
        ]

        if related:

            st.divider()
            st.markdown("### Related Skills")

            cols = st.columns(min(3, len(related)))

            for col, related_skill in zip(cols, related):

                with col:

                    st.markdown(
                        f"**{related_skill['name']}**"
                    )

                    if st.button(
                        "EXPLORE →",
                        key=f"related_{related_skill['id']}"
                    ):

                        st.session_state["selected_kala_id"] = (
                            related_skill["id"]
                        )

                        st.rerun()

# CATEGORY DIRECTORY

def render_kala_categories(group):

    categories = {}

    for skill in group:

        name = skill["subcategory"]

        categories.setdefault(name, []).append(skill)

    category_items = list(categories.items())

    for start in range(0, len(category_items), 3):

        cols = st.columns(3)

        for col, (name, category_skills) in zip(
            cols, category_items[start:start + 3]
        ):

            first = category_skills[0]["number"]
            last = category_skills[-1]["number"]

            with col:

                st.markdown(
                    f"""
                    <div class="kala-card">
                        <div class="kala-card-number">
                            KALAS {first:03} — {last:03}
                        </div>
                        <h3>{name}</h3>
                        <p>
                            {len(category_skills)} capabilities
                            to explore
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "EXPLORE CATEGORY →",
                    key=f"category_{name}"
                ):

                    st.session_state["selected_category"] = name
                    st.rerun()

    selected = st.session_state.get("selected_category")

    if selected in categories:

        st.markdown(f"### {selected}")

        for skill in categories[selected]:

            col1, col2, col3 = st.columns([5, 2, 2])

            with col1:
                st.write(
                    f"**{skill['number']:03} · {skill['name']}**"
                )

            with col2:
                st.caption(skill["difficulty"])

            with col3:

                if st.button(
                    "OPEN →",
                    key=f"open_{skill['id']}"
                ):

                    st.session_state["selected_kala_id"] = skill["id"]
                    st.rerun()
# MAIN PAGE
def render_kalas():
    st.markdown(KALAS_CSS, unsafe_allow_html=True)

    skills = load_kalas()

    classical = [
        s for s in skills
        if s["category"] == "Classical Human Arts"
    ]

    modern = [
        s for s in skills
        if s["category"] == "Modern Life Mastery"
    ]

    progress = get_progress()

    completed = sum(
        1 for s in skills
        if progress.get(s["id"]) == "Completed"
    )

    in_progress = sum(
        1 for s in skills
        if progress.get(s["id"]) == "In progress"
    )

    overall_percentage = (
        completed / len(skills) * 100
        if skills else 0
    )

    # DETAIL VIEW

    selected_id = st.session_state.get("selected_kala_id")

    if selected_id:

        selected_skill = next(
            (s for s in skills if s["id"] == selected_id),
            None
        )

        if selected_skill:
            render_skill_detail(selected_skill)
            return

        st.session_state.pop("selected_kala_id", None)

    # HERO

    st.caption("UNROT / THE HUMAN DEVELOPMENT COLLECTION")

    with st.container(key="kala-overview-card"):

        st.markdown(
            "<div style='font-family:Georgia; font-size:76px; "
            "color:#80BDB4; line-height:1.1; margin-bottom:12px;'>१२८</div>",
            unsafe_allow_html=True
        )

        st.caption("A LIFETIME CURRICULUM")

        st.markdown("## The Modern 128 Kalas.")

        st.write(
            "An exploration of 128 capabilities that shape a capable, "
            "creative, thoughtful and self-reliant individual. "
            "From classical human arts to modern life mastery."
        )
    
    # STATISTICS

    cols = st.columns(4)

    stats = [
        (len(skills), "TOTAL KALAS"),
        (len(classical), "CLASSICAL ARTS"),
        (len(modern), "MODERN MASTERY"),
        (completed, "COMPLETED")
    ]

    for col, (number, label) in zip(cols, stats):

        with col:

            st.markdown(
                f"""
                <div class="kala-stat">
                    <div class="kala-stat-number">
                        {number:03}
                    </div>
                    <div class="kala-stat-label">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # OVERALL PROGRESS

    st.markdown("### Your Learning Journey")

    st.progress(overall_percentage / 100)

    col1, col2, col3 = st.columns(3)

    col1.metric("Completed", completed)
    col2.metric("In Progress", in_progress)
    col3.metric("Remaining", len(skills) - completed - in_progress)

    st.caption(f"{overall_percentage:.1f}% of the 128 Kalas completed.")

    st.divider()

    # FEATURED SKILL

    featured, current_week, next_week, continued = (
        get_featured_skill(skills)
    )

    featured_status = get_skill_status(featured)

    intro = featured.get("introduction", {})
    tutorial = featured.get("tutorial", {})

    st.markdown(
        '<div class="kala-eyebrow">YOUR CURRENT LEARNING FOCUS</div>',
        unsafe_allow_html=True
    )

    with st.container(key="kala-feature-card"):

        st.caption("KALA OF THE WEEK")

        st.markdown(
            f"## {featured['name']}"
        )

        st.write(intro.get("overview", ""))

        st.caption(
            f"KALA {featured['number']:03}  |  "
            f"{featured['category']}  |  "
            f"{featured['difficulty'].upper()}"
        )

    # FEATURED SKILL CONTENT

    st.markdown("## Explore This Week's Skill")

    # FIRST ROW

    feature_col1, feature_col2 = st.columns(2, gap="medium")

    with feature_col1:

        with st.container(key="kala-insight-importance"):

            st.markdown("#### Why It Matters")
            st.write(intro.get("importance", ""))

    with feature_col2:

        with st.container(key="kala-insight-involves"):

            st.markdown("#### What It Involves")
            st.write(intro.get("what_it_involves", ""))

    # SECOND ROW

    feature_col3, feature_col4 = st.columns(2, gap="medium")

    with feature_col3:

        with st.container(key="kala-insight-modern"):

            st.markdown("#### Modern Relevance")
            st.write(intro.get("modern_relevance", ""))

    with feature_col4:

        with st.container(key="kala-insight-mistakes"):

            st.markdown("#### Common Mistakes")
            render_list(tutorial.get("common_mistakes", []))

    # LEARNING OBJECTIVES

    with st.container(border=True):

        st.markdown("### Learning Objectives")
        render_list(featured.get("learning_objectives", []))


    # TUTORIAL MATERIAL

    st.markdown("### Learn the Skill")

    with st.expander("Foundations and Essential Knowledge", expanded=True):

        st.markdown("**Foundations**")
        st.write(tutorial.get("foundations", ""))

        st.markdown("**Essential Knowledge**")
        render_list(tutorial.get("essential_knowledge", []))

    with st.expander("Practical Methods"):

        render_list(tutorial.get("practical_methods", []))

    with st.expander("Intermediate Development"):

        st.write(tutorial.get("intermediate_development", ""))

    with st.expander("Advanced Exploration"):

        st.write(tutorial.get("advanced_exploration", ""))

    with st.expander("Weekly Challenge"):

        render_weekly_challenge(
            featured.get("weekly_challenge", {})
        )

    with st.expander("Practical Exercises"):

        render_exercises(
            featured.get("practical_exercises", [])
        )

    with st.expander("Learning Resources"):

        render_resources(
            featured.get("resources", [])
        )

    with st.expander("Classical and Traditional Connections"):

        render_classical_connection(
            featured.get("classical_connection")
        )

        render_traditional_connection(
            featured.get("traditional_kala_connection")
        )
    # FEATURED ACTIONS

    st.markdown("#### Your Next Step")

    st.caption(f"Current status: {featured_status}")

    if st.button(
        "OPEN FULL LEARNING EXPERIENCE →",
        key="open_featured"
    ):

        st.session_state["selected_kala_id"] = featured["id"]
        st.rerun()

    if st.button(
        "CONTINUE THIS SKILL FOR NEXT WEEK →",
        key="continue_featured"
    ):

        continue_featured_skill(featured, next_week)

        st.success(
            f"{featured['name']} is scheduled for next week."
        )

    st.caption(
        "Your current weekly selection remains unchanged. "
        "Continuing schedules the same skill for the following week."
    )

    st.divider()

    # SEARCH AND FILTERS


    st.markdown("## Discover Other Kalas")

    st.caption(
        "Search the collection or narrow it down by category, difficulty and progress."
    )

    search = st.text_input(
        "Search the 128 Kalas",
        placeholder="e.g. Research, Leadership, Linux, Communication..."
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        category_filter = st.selectbox(
            "Collection",
            [
                "All",
                "Classical Human Arts",
                "Modern Life Mastery"
            ],
            key="kala_category_filter"
        )

    with filter_col2:

        difficulty_filter = st.selectbox(
            "Difficulty",
            [
                "All",
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            key="kala_difficulty_filter"
        )

    with filter_col3:

        status_filter = st.selectbox(
            "Progress",
            [
                "All",
                "Not started",
                "In progress",
                "Completed"
            ],
            key="kala_status_filter"
        )

    # Only display results when the user actively searches
    # or changes a filter.

    search_active = (
        bool(search.strip())
        or category_filter != "All"
        or difficulty_filter != "All"
        or status_filter != "All"
    )

    if search_active:

        filtered = []

        for skill in skills:

            skill_status = get_skill_status(skill)

            searchable_text = " ".join([
                skill["name"],
                skill["category"],
                skill["subcategory"],
                skill["difficulty"]
            ]).lower()

            if search.strip().lower() not in searchable_text:
                continue

            if category_filter != "All":
                if skill["category"] != category_filter:
                    continue

            if difficulty_filter != "All":
                if skill["difficulty"] != difficulty_filter:
                    continue

            if status_filter != "All":
                if skill_status != status_filter:
                    continue

            filtered.append(skill)

        st.markdown(f"### {len(filtered)} matching Kalas")

        if not filtered:

            st.info("No matching skills found. Try different filters.")

        else:

            for start in range(0, len(filtered), 3):

                cols = st.columns(3)

                for col, skill in zip(cols, filtered[start:start + 3]):

                    with col:

                        with st.container(border=True):

                            st.caption(
                                f"KALA {skill['number']:03} · "
                                f"{skill['difficulty'].upper()}"
                            )

                            st.markdown(f"### {skill['name']}")

                            st.caption(skill["subcategory"])

                            st.write(
                                f"Progress: {get_skill_status(skill)}"
                            )

                            if st.button(
                                "OPEN SKILL →",
                                key=f"search_open_{skill['id']}"
                            ):

                                st.session_state["selected_kala_id"] = skill["id"]
                                st.rerun()

    # CATEGORY COLLECTIONS

    st.markdown("## The Collections")

    st.markdown("### I. Classical Human Arts")

    st.caption(
        "Creativity, intellect, expression, culture and character."
    )

    render_kala_categories(classical)

    st.divider()

    st.markdown("### II. Modern Life Mastery")

    st.caption(
        "Practical competence for navigating the modern world."
    )

    render_kala_categories(modern)

        

            
# ---------- BHAGAVAD GITA ----------

def render_gita():

    verse = get_daily_gita_verse()

    if not verse:
        st.warning("No Bhagavad Gita data available.")
        return

    chapter = verse.get("chapter", "?")
    verse_number = verse.get("verse", "?")

    # ---------- COLLECT TRANSLATION ----------

    translation_sources = [
        "prabhu", "siva", "purohit", "san",
        "adi", "gambir", "raman", "abhinav", "sankar"
    ]

    translation = None
    translation_author = None

    for source in translation_sources:
        data = verse.get(source, {})

        if isinstance(data, dict) and data.get("et"):
            translation = data["et"]
            translation_author = data.get("author", source)
            break

    # Hindi fallback
    if not translation:
        for source in ["tej", "rams"]:
            data = verse.get(source, {})

            if isinstance(data, dict) and data.get("ht"):
                translation = data["ht"]
                translation_author = data.get("author", source)
                break

    # ---------- STYLING ----------

    st.html("""
    <style>
    .gita-page {
        color: #233044;
        font-family: Georgia, 'Times New Roman', serif;
    }

    .gita-eyebrow {
        font-family: sans-serif;
        font-size: 0.72rem;
        letter-spacing: 3px;
        font-weight: 700;
        color: #B17A35;
        margin-bottom: 10px;
    }

    .gita-heading {
        font-size: 2.1rem;
        font-weight: 600;
        color: #182A43;
        margin: 0;
    }

    .gita-subheading {
        font-family: sans-serif;
        font-size: 0.88rem;
        color: #788394;
        margin-top: 7px;
        margin-bottom: 25px;
    }

    .gita-verse-card {
    background: linear-gradient(135deg, #073B4C, #087E8B);
    border-radius: 0px;
    padding: 35px 30px;
    text-align: center;
    margin: 18px 0 26px 0;
    border-bottom: 3px solid #35C6D0;
}

    .gita-reference {
        font-family: sans-serif;
        font-size: 0.72rem;
        letter-spacing: 2px;
        color: Goldenrod;
        font-weight: 700;
        margin-bottom: 24px;
    }

    .gita-sanskrit {
        font-family: 'Noto Serif Devanagari', Georgia, serif;
        font-size: 1.55rem;
        line-height: 2.15;
        color: #FFF9EF;
        font-weight: 500;
        white-space: pre-wrap;
    }

    .gita-transliteration {
        font-family: Georgia, serif;
        font-size: 0.94rem;
        font-style: italic;
        line-height: 1.8;
        color: #D5F3F2;
        margin-top: 22px;
    }

    .gita-section-label {
        font-family: sans-serif;
        font-size: 0.72rem;
        letter-spacing: 2px;
        color: #B17A35;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .gita-section-title {
        font-family: Georgia, serif;
        font-size: 1.45rem;
        color: #1D3049;
        margin-bottom: 14px;
    }

    .gita-translation-card {
        background: #F5F3ED;
        border: 1px solid #E8E2D6;
        border-radius: 0px;
        padding: 24px;
        margin-bottom: 25px;
    }

    .gita-translation-text {
        font-family: Georgia, serif;
        font-size: 1.08rem;
        line-height: 1.9;
        color: #344256;
    }

    .gita-attribution {
        font-family: sans-serif;
        font-size: 0.78rem;
        color: #8A775F;
        margin-top: 18px;
        letter-spacing: 0.3px;
    }

    .gita-commentary-card {
        background: #FFFFFF;
        border: 1px solid #E5E9EF;
        border-left: 3px solid #C99A55;
        border-radius: 0px;
        padding: 24px;
        margin-top: 12px;
    }

    .gita-commentary-text {
        font-family: Georgia, serif;
        font-size: 1rem;
        line-height: 2;
        color: #39485A;
        white-space: pre-wrap;
    }

    .gita-reflection-card {
        background: #F7F0E5;
        border: 1px solid #EBDCC4;
        border-radius: 0px;
        padding: 22px 24px;
        margin-top: 28px;
    }

    .gita-reflection-title {
        font-family: sans-serif;
        font-size: 0.72rem;
        letter-spacing: 2px;
        color: #A16F32;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .gita-reflection-text {
        font-family: Georgia, serif;
        font-size: 1.08rem;
        line-height: 1.7;
        color: #493B2C;
    }
    </style>
    """)

    # ---------- HEADER ----------

    st.html("""
    <div class="gita-page">
        <div class="gita-eyebrow">DAILY WISDOM</div>
        <div class="gita-heading">भगवद्गीता</div>
        <div class="gita-subheading">
            An ancient dialogue on duty, wisdom and the nature of life.
        </div>
    </div>
    """)

    # ---------- VERSE CARD ----------

    slok = html.escape(verse.get("slok", "Sanskrit text unavailable"))
    transliteration = html.escape(verse.get("transliteration", ""))

    st.html(f"""
    <div class="gita-verse-card">
        <div class="gita-reference">
            BHAGAVAD GITA &nbsp;·&nbsp; CHAPTER {chapter}
            &nbsp;·&nbsp; VERSE {verse_number}
        </div>
        <div class="gita-sanskrit">{slok}</div>
        <div class="gita-transliteration">{transliteration}</div>
    </div>
    """)

    # ---------- TRANSLATION ----------

    st.html("""
    <div class="gita-page">
        <div class="gita-section-label">01 · UNDERSTANDING THE VERSE</div>
        <div class="gita-section-title">Translation</div>
    </div>
    """)

    if translation:
        st.html(f"""
        <div class="gita-translation-card">
            <div class="gita-translation-text">
                {html.escape(translation)}
            </div>
            <div class="gita-attribution">
                TRANSLATION &nbsp;·&nbsp;
                {html.escape(translation_author)}
            </div>
        </div>
        """)
    else:
        st.info("Translation unavailable.")

    # ---------- COMMENTARY ----------

    st.html("""
<div class="gita-page">
    <div class="gita-section-label">02 · PERSPECTIVES</div>
    <div class="gita-section-title">Commentary & Interpretation</div>
</div>
""")

    # Automatically retrieve Swami Prabhupada's commentary
    prabhupada = verse.get("prabhu", {})

    commentary = prabhupada.get("ec", "")

    if commentary and commentary.strip():
        st.html(f"""
        <div class="gita-commentary-card">
        <div class="gita-attribution">
            A.C. BHAKTIVEDANTA SWAMI PRABHUPADA
        </div>
        <div class="gita-commentary-text">
            {html.escape(commentary.strip())}
        </div>
    </div>
    """)
    else:
        st.info("Swami Prabhupada's commentary is unavailable for this verse.")
    # ---------- REFLECTION ----------

    reflection_prompts = [
        "What does this verse teach you about your own actions?",
        "How could you apply this teaching to a situation in your life?",
        "What assumption or belief does this verse challenge?",
        "What is one practical lesson you can take from this verse?"
        "Which part of your life would benefit most from this teaching?",
        "Are you acting out of wisdom, fear, attachment, or expectation?",
        "What would change if you genuinely practised this teaching for a week?",
        "Does this verse challenge something you have always believed?",
        "What does this verse teach about controlling your reactions?",
        "How does this teaching redefine success?",
        "What is within your control, and what must you learn to accept?",
        "Are your daily actions aligned with the person you wish to become?",
        "What attachment might be preventing you from seeing things clearly?",
        "How can you apply this wisdom when facing uncertainty?",
        "What does this verse suggest about ego and self-awareness?",
        "When was the last time you acted without expecting something in return?",
        "What does this verse teach about patience and discipline?",
        "How might this teaching change the way you treat other people?",
        "What is one habit you should reconsider after reading this verse?",
        "Does true knowledge require experience, faith, or reflection?",
        "What does this verse teach about the difference between temporary and lasting happiness?",
        "If you had to summarise this verse in one principle, what would it be?",
        "What is one uncomfortable truth this verse asks you to confront?"

    ]

    prompt_index = (chapter + verse_number) % len(reflection_prompts)

    st.html(f"""
    <div class="gita-reflection-card">
        <div class="gita-reflection-title">
            03 · CONTEMPLATE
        </div>
        <div class="gita-reflection-text">
            {html.escape(reflection_prompts[prompt_index])}
        </div>
    </div>
    """)
def render_linux_commands():

    st.subheader("Linux Commands of the Day")
    st.caption("FIVE COMMANDS. FIVE NEW TOOLS. EVERY DAY.")

    if "daily_linux_commands" not in st.session_state:
        st.session_state.daily_linux_commands = get_daily_linux_commands()

    commands = st.session_state.daily_linux_commands

    for index, item in enumerate(commands, start=1):

        html_card = f"""
    <div style="
    background-color: #080d0d;
    border: 1px solid #263b35;
    padding: 16px 20px;
    margin-top: 16px;
    border-radius: 0px;
    ">
    <div style="
        color: #6c8c7e;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 10px;
    ">
        COMMAND {index:02d}
    </div>

    <div style="
        color: #39ff88;
        font-family: Consolas, monospace;
        font-size: 17px;
        font-weight: 600;
        overflow-wrap: anywhere;
    ">
        <span style="color: #8b949e;">$ </span>{item['output']}
    </div>
    </div>

    <div style="
    padding: 10px 2px 18px 2px;
    color: #425c59;
    font-size: 14px;
    ">
    {item['input']}
    </div>
    """

        st.html(html_card)

    if st.button("↻ Generate Another 5 Commands", key="new_linux_commands"):

        st.session_state.daily_linux_commands = get_daily_linux_commands()
        st.rerun()

# ----- AUTHENTICATION GATE -----

if not (
    st.session_state.get("authenticated", False)
    or st.session_state.get("guest_mode", False)
):
    render_auth()
    st.stop()
# ----- Initialise session state -----
if "completed" not in st.session_state:
    st.session_state.completed = set()

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"
# Handle navigation requests from activity cards
if "navigate_to" in st.session_state:
    st.session_state.navigation = st.session_state.pop("navigate_to")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

activities = load_activities()

# ----- Sidebar navigation -----
with st.sidebar:
    st.markdown("## 🪷 UNROT")
    st.caption("Your daily antidote to passive scrolling.")
    st.divider()

    pages = ["Home"] + [
        activity["page"] for activity in activities.values()
    ]

    selected_page = st.radio(
        "Navigate",
        pages,
        index=(
            pages.index(st.session_state.active_page)
            if st.session_state.active_page in pages
            else 0
        ),
        key="navigation",
    )

    st.session_state.active_page = selected_page

    st.divider()
    st.caption("Small sessions. Active learning. Real progress.")

    st.divider()

    if st.button("LOG OUT", use_container_width=True):
        logout()
# ----- Home dashboard -----
if selected_page == "Home":
    completed_count = get_completed_count(
        st.session_state.completed
    )
    total_count = len(activities)

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow" style="color:#A8F0ED">
                YOUR DAILY LEARNING SPACE
            </div>
            <h1>Make your mind move.</h1>
            <p>{get_daily_greeting()}.
            Learn something, solve something, remember something.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("\n\n\n\n\n\n")
    col1, col2, col3 = st.columns(3)
    col1.metric("Learning activities", total_count)
    col2.metric("Completed this session", completed_count)
    col3.metric("Remaining", total_count - completed_count)

    st.subheader("Today's learning menu")
    st.caption("Choose an activity. Start small; engage actively.")

    activity_items = list(activities.items())

    for start in range(0, len(activity_items), 2):
        cols = st.columns(2)

        for col, (key, activity) in zip(
            cols, activity_items[start:start + 2]
        ):
            with col:
                done = key in st.session_state.completed
                status = (
                    "✓ Completed"
                    if done
                    else activity["duration"]
                )

                st.markdown(
                    f"""
                    <div class="activity-card">
                        <div class="eyebrow">
                            {activity["category"]}
                        </div>
                        <h3>{activity["icon"]} {activity["title"]}</h3>
                        <p>{activity["description"]}</p>
                        <small>{status}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Open activity",
                    key=f"open_{key}",
                    use_container_width=True,
                ):
                    st.session_state.navigate_to = activity["page"]
                    st.rerun()

# ----- Activity placeholder pages -----
# ----- Activity pages -----

else:

    activity = next(
        (
            item for item in activities.values()
            if item["page"] == selected_page
        ),
        None,
    )

    st.title(selected_page)

    if activity:

        st.caption(activity["category"])
        st.write(activity["description"])

        # ----- INTEGRAL OF THE DAY -----

        if selected_page == "Integral":

            # Select the first integral when opening the activity
            if "current_integral_id" not in st.session_state:
                get_random_integral()

            integrals = load_integrals()

            integral = next(
                (
                    item for item in integrals
                    if item["id"] == st.session_state.current_integral_id
                ),
                None,
            )

            if integral:

                st.divider()

                st.subheader("Solve this integral")

                # Display the expression in its original format for now
                try:
                    expression = sp.sympify(integral["integrand"])

                    st.latex(
                    rf"\int {sp.latex(expression)}\, d{integral['variable']}"
                )

                except Exception:
                    st.code(
                        f"∫ {integral['integrand']} d{integral['variable']}"
                    )

                st.text_input(
                    "Your answer ~ ",
                    placeholder="Enter your antiderivative...",
                    key="integral_user_answer",
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Reveal solution",
                        key="reveal_integral",
                        use_container_width=True,
                    ):
                        st.session_state.show_integral_answer = True

                with col2:
                    if st.button(
                        "Different Integral",
                        key="different_integral",
                        use_container_width=True,
                    ):
                        st.session_state.show_integral_answer = False
                        st.session_state.pop("integral_user_answer", None)

                        get_random_integral()
                        st.rerun()

                if st.session_state.get("show_integral_answer", False):

                    st.markdown("### Reference answer")

                    try:
                        answer_expression = sp.sympify(integral["answer"])

                        st.latex(
                            sp.latex(answer_expression) + r" + C"
                        )

                    except Exception:
                        st.code(integral["answer"] + " + C")

            else:
                st.error("Unable to load the selected integral.")
            render_exam_integral()
            
        # ----- MENTAL MATHS -----

        elif selected_page == "Mental Maths":

            render_mental_maths()
            
        #------English Lab: Phrasal Verbs -----
        
        elif selected_page == "English Lab":

            render_phrasal_verb()
            st.markdown("")
    
            render_vocabulary()
            st.markdown("")
            
            render_figures_of_speech()
            
        #----- Linux Commands -----
        
        elif selected_page == "Linux":

            render_linux_commands()
            st.markdown("")
         
        #------Physics---------   
        elif selected_page == "Physics":
            render_physics()
            st.markdown("")
        elif selected_page == "DSA":
            render_dsa()
        
        #----- Bhagavad Gita -----    
        elif selected_page == "Gita":
            render_gita()
            
        elif selected_page == "Life Sciences":
            render_life_sciences()
        elif selected_page == "Wildcard":
            render_wildcard()
        elif selected_page == "CS Prep":
            render_cs_prep()
        elif selected_page == "To-do List":
            render_todo()
        elif selected_page == "Weekly Skill":
            render_kalas()
        # ----- OTHER ACTIVITY PLACEHOLDERS -----

        else:

            st.info(
                "This activity's learning engine will be implemented "
                "in its scheduled build."
            )

        # ----- COMPLETION TRACKING -----

        key = next(
            key for key, item in activities.items()
            if item["page"] == selected_page
        )

        st.divider()

        if key in st.session_state.completed:

            st.success("Completed in this session.")

            if st.button("Mark as incomplete"):
                st.session_state.completed.remove(key)
                st.rerun()

        else:

            if st.button("Mark as completed", type="primary"):
                st.session_state.completed.add(key)
                st.rerun()
