import streamlit as st
import AddClient
import ViewClients
from OccupationAnalyzer import display_cv_analysis

# Callback functions for page navigation


def show_dashboard():
    st.session_state.page = "dashboard"


def show_add_client():
    st.session_state.page = "add_client"


def show_view_clients():
    st.session_state.page = "view_clients"


def show_settings():
    st.session_state.page = "settings"


def show_cv_analysis():
    st.session_state.page = "cv_analysis"


def logout():
    # Clear all session state related to the user
    for key in st.session_state.keys():
        del st.session_state[key]

    # Optionally, you can set a page redirect to the login page
    st.session_state.page = "login"
    st.rerun()


# Main function for displaying the dashboard with spinners during navigation
def display_dashboard():

    # Sidebar for navigation
    with st.sidebar:

        # Use callbacks instead of rerun for navigation
        st.button("Dashboard", on_click=show_dashboard,
                  use_container_width=True, icon=":material/dashboard:")
        st.button("Add Client", on_click=show_add_client,
                  use_container_width=True, icon=":material/add_circle:")
        st.button("View Clients", on_click=show_view_clients,
                  use_container_width=True, icon=":material/list:")
        st.button("Settings", on_click=show_settings,
                  use_container_width=True, icon=":material/settings:")
        st.button("Analyze CV", on_click=show_cv_analysis,
                  use_container_width=True, icon=":material/query_stats:")
        st.button("Logout", on_click=logout,
                  use_container_width=True, icon=":material/logout:")

    # Main content area based on the selected page
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

    # Displaying spinner during navigation to each page
    if st.session_state.page == "dashboard":
        # Simulate loading delay
        display_dashboard_content()
    elif st.session_state.page == "add_client":
        AddClient.display_add_client()
    elif st.session_state.page == "view_clients":
        ViewClients.display_view_clients()
    elif st.session_state.page == "settings":
        st.write("Settings page coming soon!")
    elif st.session_state.page == "cv_analysis":
        display_cv_analysis()

# Display the main dashboard content with spinners


def display_dashboard_content():
    st.title("Migration Agent Dashboard")
    st.write("Welcome to your dashboard!")

    # Using a container to dynamically update charts and statistics
    container = st.container()

    # Example statistics and metrics with spinner for loading charts
    with st.spinner("Loading statistics and charts..."):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Clients", "128")
        with col2:
            st.metric("Pending Applications", "35")

    # Dynamically update progress and charts
    if st.button("Update Progress"):
        with container:
            st.write("### Progress Overview")
            st.progress(85)  # Dynamically updated progress
            st.subheader("Monthly Applications")
            st.bar_chart({"Applications": [50, 70, 90, 110, 130, 140]})
    else:
        with container:
            st.write("### Progress Overview")
            st.progress(75)
            st.subheader("Monthly Applications")
            st.bar_chart({"Applications": [50, 60, 80, 70, 90, 100]})
