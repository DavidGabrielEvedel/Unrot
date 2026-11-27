
import json
import random
import streamlit as st
from datetime import date, datetime
from pathlib import Path


# ---------- CONTENT PATHS ----------

BASE_DIR = Path(__file__).parent

CONTENT_PATH = BASE_DIR / "content" / "activities.json"
INTEGRAL_FILE = BASE_DIR / "content" / "integrals" / "integrals.jsonl"


# ---------- ACTIVITY CATALOGUE ----------

def load_activities():
    """Load and validate the activity catalogue."""

    with CONTENT_PATH.open("r", encoding="utf-8") as file:
        activities = json.load(file)

    if not isinstance(activities, dict):
        raise ValueError("Activity catalogue must be a JSON object.")

    required_fields = {
        "title",
        "icon",
        "category",
        "description",
        "duration",
        "page",
    }

    for key, activity in activities.items():
        if not isinstance(activity, dict):
            raise ValueError(f"Activity '{key}' must be an object.")

        missing = required_fields - activity.keys()

        if missing:
            raise ValueError(
                f"Activity '{key}' is missing: {sorted(missing)}"
            )

    return activities


# ---------- GENERAL HELPERS ----------

def get_daily_seed():
    return int(date.today().strftime("%Y%m%d"))


def get_daily_greeting():

    hour = datetime.now().hour

    if hour < 12:
        return "Good morning"

    if hour < 17:
        return "Good afternoon"

    return "Good evening"


def get_completed_count(completed):
    return len(completed)


# ---------- INTEGRAL OF THE DAY ----------

@st.cache_data
def load_integrals():
    """Load the compiled integral collection."""

    integrals = []

    with INTEGRAL_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                integrals.append(json.loads(line))

    return integrals


def get_random_integral():
    """Select a random integral without immediately repeating one."""

    integrals = load_integrals()

    if not integrals:
        return None

    previous_id = st.session_state.get("current_integral_id")

    available = [
        item for item in integrals
        if item["id"] != previous_id
    ]

    selected = random.choice(available or integrals)

    st.session_state.current_integral_id = selected["id"]

    return selected

EXAM_INTEGRAL_FILE = BASE_DIR / "data_sources" / "exam_integrals.jsonl"


@st.cache_data
def load_exam_integrals():
    integrals = []

    with EXAM_INTEGRAL_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                integrals.append(json.loads(line))

    return integrals


def get_random_exam_integral():
    integrals = load_exam_integrals()

    if not integrals:
        return None

    previous_id = st.session_state.get("current_exam_integral_id")
    available = [item for item in integrals if item["id"] != previous_id]

    selected = random.choice(available or integrals)
    st.session_state.current_exam_integral_id = selected["id"]

    return selected

# ----- ENGLISH LAB -----

PHRASAL_VERB_FILE = BASE_DIR / "data_sources" / "phrasal_verbs.jsonl"


@st.cache_data
def load_phrasal_verbs():
    entries = []

    with PHRASAL_VERB_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                entries.append(json.loads(line))

    return entries


def get_daily_phrasal_verb():
    entries = load_phrasal_verbs()

    if not entries:
        return None

    previous_id = st.session_state.get("current_phrasal_verb_id")

    available = [
        entry for entry in entries
        if entry["id"] != previous_id
    ]

    selected = random.choice(available or entries)

    st.session_state.current_phrasal_verb_id = selected["id"]

    return selected

# ----- ENGLISH LAB: VOCABULARY -----

VOCABULARY_FILE = BASE_DIR / "data_sources" / "vocabulary.jsonl"


@st.cache_data
def load_vocabulary():

    entries = []

    with VOCABULARY_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                entries.append(json.loads(line))

    return entries


def get_daily_vocabulary():

    entries = load_vocabulary()

    if len(entries) < 3:
        return entries

    today = date.today().isoformat()

    daily_random = random.Random(today)

    return daily_random.sample(entries, 3)

# FIGURES OF SPEECH

FIGURES_OF_SPEECH_FILE = BASE_DIR / "data_sources" / "figures_of_speech.jsonl"


@st.cache_data
def load_figures_of_speech():
    entries = []

    with FIGURES_OF_SPEECH_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                entries.append(json.loads(line))

    return entries


def get_daily_figure_of_speech():
    entries = load_figures_of_speech()

    if not entries:
        return None

    previous_id = st.session_state.get("current_figure_id")

    available = [
        entry for entry in entries
        if entry["id"] != previous_id
    ]

    selected = random.choice(available or entries)

    st.session_state.current_figure_id = selected["id"]

    return selected

# LINUX COMMANDS

LINUX_COMMANDS_FILE = BASE_DIR / "data_sources" / "linuxcommands.json"


@st.cache_data
def load_linux_commands():
    with LINUX_COMMANDS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_daily_linux_commands():
    commands = load_linux_commands()

    if len(commands) <= 5:
        return commands

    return random.sample(commands, 5)

# ---------- PHYSICS QUESTION BANK ----------

PHYSICS_QUESTIONS_FILE = BASE_DIR / "data_sources" / "high_school_physics.json"


@st.cache_data
def load_physics_questions():
    with PHYSICS_QUESTIONS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_random_physics_question():
    questions = load_physics_questions()
    return random.choice(questions)

# ---------- BHAGAVAD GITA ----------

GITA_FILE = BASE_DIR / "data_sources" / "gita.jsonl"


@st.cache_data
def load_gita_verses():
    verses = []

    with GITA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                verses.append(json.loads(line))

    return verses


def get_daily_gita_verse():
    verses = load_gita_verses()

    if not verses:
        return None

    # Same verse throughout the day
    today = date.today().toordinal()
    return verses[today % len(verses)]

# LIFE SCIENCES — BIOLOGY & CHEMISTRY MCQ BANK


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data_sources"


@st.cache_data
def load_mcq_dataset(filename):

    filepath = DATA_DIR / filename

    questions = []

    with open(filepath, "r", encoding="utf-8") as file:

        for line in file:

            if not line.strip():
                continue

            try:
                question = json.loads(line)

                options = question.get("options", {})
                answer = question.get("correct_answer")

                if (
                    question.get("question")
                    and isinstance(options, dict)
                    and all(options.get(k) for k in ["A", "B", "C", "D"])
                    and answer in ["A", "B", "C", "D"]
                    and question.get("explanation")
                ):

                    # Exclude questions requiring unavailable images.
                    if question.get("question_images"):
                        continue

                    questions.append(question)

            except json.JSONDecodeError:
                continue

    return questions


def get_daily_mcqs(filename, subject, count=5):

    questions = load_mcq_dataset(filename)

    if len(questions) < count:
        raise ValueError(
            f"{subject}: Only {len(questions)} valid questions found. "
            f"At least {count} are required."
        )

    today = date.today().isoformat()

    rng = random.Random(f"{today}-{subject}")

    return rng.sample(questions, count)


def get_daily_life_sciences_questions():

    biology = get_daily_mcqs(
        "biology_mcqs_400.jsonl",
        "biology",
        5
    )

    chemistry = get_daily_mcqs(
        "chemistry_mcqs_700.jsonl",
        "chemistry",
        5
    )

    return biology, chemistry

def load_wildcard_questions():
    path = Path(__file__).resolve().parent / "data_sources" / "wildcard.jsonl"

    questions = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            try:
                q = json.loads(line)

                if all(k in q for k in ("id", "cat", "q", "opts", "ans", "why", "extra", "level")):
                    if isinstance(q["opts"], list) and len(q["opts"]) >= 2:
                        questions.append(q)

            except json.JSONDecodeError:
                continue

    return questions


def get_daily_wildcard_questions(questions, count=5):
    if len(questions) < count:
        raise ValueError(f"Wildcard needs at least {count} valid questions.")

    seed = int(date.today().strftime("%Y%m%d"))
    return random.Random(seed).sample(questions, count)

@st.cache_data
def load_cs_questions():
    questions = []

    path = Path(__file__).resolve().parent / "data_sources" / "tech_prep.jsonl"

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))

    return questions

def get_daily_cs_questions(questions, count=7):
    today = date.today().isoformat()

    rng = random.Random(f"cs_prep_{today}")

    return rng.sample(questions, min(count, len(questions)))

BASE_DIR = Path(__file__).resolve().parent
from datetime import date, timedelta
KALAS_PATH = BASE_DIR / "data_sources" / "skills.jsonl"
KALA_PROGRESS_PATH = BASE_DIR / "data_sources" / "kala_progress.json"
KALA_SCHEDULE_PATH = BASE_DIR / "data_sources" / "kala_schedule.json"
@st.cache_data
def load_kalas():

    skills = []

    with open(KALAS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                skills.append(json.loads(line))

    return sorted(skills, key=lambda x: x["number"])


def load_json(path, default):

    if path.exists():
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    return default


def save_json(path, data):

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_week_key(day):

    iso = day.isocalendar()

    return f"{iso.year}-W{iso.week:02d}"


def get_featured_skill(skills):

    schedule = load_json(KALA_SCHEDULE_PATH, {})

    today = date.today()

    current_week = get_week_key(today)
    next_week = get_week_key(today + timedelta(days=7))

    # Previously scheduled skill takes priority.
    if current_week in schedule:

        skill_number = schedule[current_week]

        featured = next(
            (s for s in skills if s["number"] == skill_number),
            None
        )

        if featured:
            return featured, current_week, next_week, True

    # Otherwise use the deterministic weekly rotation.
    week_number = today.isocalendar().week

    featured = skills[(week_number - 1) % len(skills)]

    schedule[current_week] = featured["number"]

    save_json(KALA_SCHEDULE_PATH, schedule)

    return featured, current_week, next_week, False


def continue_featured_skill(featured, next_week):

    schedule = load_json(KALA_SCHEDULE_PATH, {})

    schedule[next_week] = featured["number"]

    save_json(KALA_SCHEDULE_PATH, schedule)