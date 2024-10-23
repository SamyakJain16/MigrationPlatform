import streamlit as st
import requests


import streamlit as st
import requests


def display_login():
    st.title("Migration Agent Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json={"email": email, "password": password}
            )

            # Check if the login was successful
            if response.status_code == 200:
                data = response.json()  # Use .json() to get the response data
                st.session_state['token'] = data.get('access_token')
                # Optional: track the logged-in user
                st.session_state['logged_in_user'] = email
                st.success("Login successful! Redirecting to dashboard...")
                st.rerun()  # Rerun to load the dashboard
            else:
                st.error(f"Login failed. Please check your credentials. (Status: {
                         response.status_code})")
        except Exception as e:
            st.error(f"Error: {str(e)}")
