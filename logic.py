
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
