import streamlit as st
import requests


def display_view_clients():
    st.title("View Clients")

    # Ensure the user is logged in
    if 'token' not in st.session_state or st.session_state.token is None:
        st.error("Please log in first.")
        st.stop()
    print("Access Token View Client")
    try:

        response = requests.get(
            "http://127.0.0.1:5000/clients",
            headers={"Authorization": f"Bearer {
                st.session_state['token']}"}
        )
        if response.status_code == 200:
            clients = response.json()
            st.subheader("Client List")
            for i, client in enumerate(clients):
                st.write(f"Name: {client['name']}, Email: {
                    client['email']}, Status: {client['status']}")
        else:
            st.error("Failed to retrieve clients.")
    except Exception as e:
        st.error(f"Error fetching clients: {str(e)}")
