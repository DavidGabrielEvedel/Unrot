import random
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
)

apply_styles()

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
        "title": "Alphabetical mental maths",
        "numbers": letters,
        "answer": str(answer),
    })
    # 10: 30-line single-digit addition and subtraction
    numbers, answer = generate_single_digit_chain()

    questions.append({
        "type": "sum",
        "title": "Single-digit addition & subtraction · 30 lines",
        "numbers": numbers,
        "answer": str(answer),
    })
    return questions


def render_mental_maths():

    st.caption("ABACUS MENTAL CALCULATION")

    if "mental_maths_questions" not in st.session_state:
        st.session_state.mental_maths_questions = generate_mental_maths_set()

    questions = st.session_state.mental_maths_questions

    st.markdown(
        """
        <div style="
            background: #E7F3F1;
            padding: 16px 20px;
            margin: 15px 0 25px 0;
            border-left: 3px solid #087F8C;
        ">
            <span style="font-family: Georgia, serif; color: #18343A;">
                Calculate mentally. No calculator. No written working.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    alphabet_values = {
        chr(65 + i): i + 1 for i in range(26)
    }

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
            st.markdown(
                f"### {question['question']}"
            )

        st.text_input(
            "Your answer",
            key=f"mental_answer_{index}",
            placeholder=(
                "Quotient, remainder"
                if question["type"] == "division"
                else "Enter your answer"
            ),
        )

    st.markdown("---")

    if st.button(
        "Check all answers",
        type="primary",
        use_container_width=True,
    ):

        score = 0

        for index, question in enumerate(questions):

            user_answer = st.session_state.get(
                f"mental_answer_{index}", ""
            ).strip().replace(" ", "")

            correct_answer = question["answer"]

            if question["type"] == "division":
                is_correct = user_answer == correct_answer

            else:
                try:
                    is_correct = int(user_answer) == int(correct_answer)
                except ValueError:
                    is_correct = False

            if is_correct:
                score += 1
                st.success(f"Question {index + 1}: Correct!")

            else:
                st.error(
                    f"Question {index + 1}: Incorrect. "
                    f"Correct answer: {correct_answer}"
                )

        st.session_state.mental_maths_score = score

        st.markdown(f"## Your score: {score}/10")

        if score == 10:
            st.balloons()
            st.success("Perfect calculation!")

        elif score >= 6:
            st.success("Good work. Keep practising!")

        else:
            st.info("Keep practising. Speed comes with consistency.")

    if st.button(
        "Generate Different Set",
        use_container_width=True,
    ):

        st.session_state.mental_maths_questions = generate_mental_maths_set()

        for index in range(10):
            st.session_state.pop(f"mental_answer_{index}", None)

        st.session_state.pop("mental_maths_score", None)

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
