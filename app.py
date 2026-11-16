
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
