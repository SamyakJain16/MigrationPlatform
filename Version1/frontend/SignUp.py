import streamlit as st
import requests


def dispay_signup():
    st.title("Migration Agent Sign-Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            # Send a POST request to the Flask API
            response = requests.post(
                "http://127.0.0.1:5000/signup",  # Ensure this URL matches your Flask server
                json={"email": email, "password": password}
            )
            # Handle the response from the Flask API
            if response.status_code == 201:
                st.success("Sign-up successful! Please log in.")
            elif response.status_code == 400:
                st.error("Sign-up failed: Agent could not be registered.")
            else:
                st.error(f"Sign-up failed: {response.status_code}")
                st.error(response.text)
        except Exception as e:
            st.error(f"Error during sign-up: {str(e)}")
