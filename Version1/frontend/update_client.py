import streamlit as st
import requests

st.title("Update Client")

client_id = st.text_input("Client ID")
new_name = st.text_input("New Client Name (optional)")
new_email = st.text_input("New Client Email (optional)")
new_status = st.selectbox(
    "New Status", ["Pending", "In Progress", "Approved", "Rejected"])

if st.button("Update Client"):
    data = {"client_id": client_id}
    if new_name:
        data["name"] = new_name
    if new_email:
        data["email"] = new_email
    if new_status:
        data["status"] = new_status

    response = requests.put("http://127.0.0.1:5000/update_client", json=data)
    if response.status_code == 200:
        st.success("Client updated successfully!")
    else:
        st.error("Failed to update client.")
