import streamlit as st
import Login
import SignUp
import Dashboard  # Your dashboard.py file
# Place this CSS at the top of your script (Home.py or Dashboard.py)


def main():

    # Check if user is logged in or not
    if 'token' not in st.session_state:
        st.session_state['token'] = None

    # Display the appropriate page based on login status
    if st.session_state['token']:
        print("Accesss Token \n")
        Dashboard.display_dashboard()  # Show the dashboard if logged in
    else:
        login_page = st.sidebar.selectbox("Choose Page", ["Login", "Sign Up"])
        if login_page == "Login":
            Login.display_login()
        elif login_page == "Sign Up":
            SignUp.dispay_signup()


main()
