import streamlit as st
import requests


def display_add_client():
    st.title("Add New Client")

    # Ensure the user is logged in
    if 'token' not in st.session_state or st.session_state.token is None:
        st.error("Please log in first.")
        st.stop()
    print("Access Token Add Client")
    # Input fields for adding client details
    name = st.text_input("Client Name", key="client_name")
    email = st.text_input("Client Email", key="client_email")
    status = st.selectbox(
        "Status", ["Pending", "Active", "Inactive"], key="client_status")

    if st.button("Add Client", key="add_client_button"):
        try:
            # Send POST request to add client
            response = requests.post(
                "http://127.0.0.1:5000/add_client",
                json={"name": name, "email": email, "status": status},
                headers={"Authorization": f"Bearer {
                    st.session_state['token']}"}
            )

            if response.status_code == 201:
                st.success("Client added successfully!")
            else:
                st.error(f"Failed to add client: {response.text}")
        except Exception as e:
            st.error(f"Error adding client: {str(e)}")
