import random
import time
import streamlit as st
import sympy as sp
from styles import apply_styles
from logic import (
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
    get_daily_life_sciences_questions
)
apply_styles()
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
        questions = load_physics_questions()
        st.session_state.physics_question = questions[0]

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
            import random

            st.session_state.physics_question = random.choice(available)
            st.session_state.physics_checked = False

            st.rerun() 
            
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
    st.markdown("## 🌊 UNROT")
    st.caption("Your daily antidote to passive scrolling.")
    st.divider()

    pages = ["Home"] + [
        activity["page"] for activity in activities.values()
    ] + ["To-do List"]

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

# ----- To-do list -----
elif selected_page == "To-do List":
    st.title("Your to-do list")
    st.caption("Tasks are temporary in this first version.")

    with st.form("add_task_form", clear_on_submit=True):
        task = st.text_input("What do you want to get done?")
        submitted = st.form_submit_button("Add task")

        if submitted:
            if task.strip():
                st.session_state.tasks.append({
                    "text": task.strip(),
                    "done": False,
                })
                st.rerun()
            else:
                st.warning("Enter a task first.")

    for index, item in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([5, 1])

        with col1:
            checked = st.checkbox(
                item["text"],
                value=item["done"],
                key=f"task_{index}",
            )

            if checked != item["done"]:
                item["done"] = checked
                st.rerun()

        with col2:
            if st.button("Delete", key=f"delete_{index}"):
                st.session_state.tasks.pop(index)
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
        
        #----- Bhagavad Gita -----    
        elif selected_page == "Gita":
            render_gita()
            
        elif selected_page == "Life Sciences":
            render_life_sciences()

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
