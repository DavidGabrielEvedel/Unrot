import streamlit as st
from supabase_client import get_supabase_client


def render_auth():

    st.markdown("# UNROT.")
    st.caption("A PERSONAL LEARNING SPACE")

    login_tab, signup_tab = st.tabs(["LOG IN", "CREATE ACCOUNT"])

    # ---------- LOGIN ----------

    with login_tab:

        st.subheader("Welcome back.")

        with st.form("login_form"):

            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")

            login = st.form_submit_button(
                "LOG IN",
                use_container_width=True,
                key="auth_login"
            )

        if login:

            try:
                supabase = get_supabase_client()

                response = supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password
                })

                st.session_state.authenticated = True
                st.session_state.guest_mode = False
                st.session_state.user = response.user

                st.success("Login successful.")
                st.rerun()

            except Exception as e:
                st.error(f"Login failed: {e}")

    # ---------- SIGNUP ----------

    with signup_tab:

        st.subheader("Create your account.")

        with st.form("signup_form"):

            name = st.text_input("Your name")
            email = st.text_input("Email address", key="signup_email")

            password = st.text_input(
                "Create password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )

            signup = st.form_submit_button(
                "CREATE ACCOUNT",
                use_container_width=True,
                key="auth_signup"
            )

        if signup:

            if not name.strip() or not email.strip() or not password:
                st.warning("Please complete all fields.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")

            else:

                try:
                    supabase = get_supabase_client()

                    response = supabase.auth.sign_up({
                        "email": email.strip(),
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": name.strip()
                            }
                        }
                    })

                    if response.session:

                        st.session_state.authenticated = True
                        st.session_state.guest_mode = False
                        st.session_state.user = response.user

                        st.success("Account created successfully.")
                        st.rerun()

                    else:
                        st.success(
                            "Account created! Check your email "
                            "to verify your account before logging in."
                        )

                except Exception as e:
                    st.error(f"Signup failed: {e}")

    # ---------- GUEST ACCESS ----------

    st.divider()
    st.markdown("### Just exploring?")

    if st.button("CONTINUE AS GUEST", use_container_width=True, key="auth_guest"):

        st.session_state.authenticated = False
        st.session_state.guest_mode = True

        st.rerun()


def logout():

    if st.session_state.get("authenticated", False):

        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()

        except Exception:
            pass

    for key in [
        "authenticated",
        "guest_mode",
        "user",
        "supabase_client"
    ]:
        st.session_state.pop(key, None)

    st.rerun()