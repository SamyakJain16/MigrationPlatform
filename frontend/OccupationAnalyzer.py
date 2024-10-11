import streamlit as st
import time
import json
import pandas as pd
from extract_pdf import extract_text_from_pdf
from cv_analyzer import get_top_occupations_from_resume
from retrieve_occupations import get_occupation_list
from get_similarityscores import compute_similarity
from get_best_occupations import find_max_per_row
from preprocessor import remove_digits
from get_results_schema import generate_occupation_data
from get_results_openai import generate_new_results
from llm_response_parser import parse_llm_response


def display_cv_analysis():
    st.title("CV Analysis")

    # First, let the user upload a PDF file
    uploaded_file = st.file_uploader("Upload CV", type=["pdf"])

    # Specify the path to the occupation list CSV (update this path as needed)
    csv_path = '/Users/mayankjain/Downloads/migration_crewai/project-resh/occupation_finder/knowledge_base/occupation_list_main.csv'

    if uploaded_file is not None:

        # Clear previous results if any

        # Once the file is uploaded, allow the user to click "Submit" to analyze
        if st.button("Submit"):

            with st.spinner("Starting analysis... This might take a while."):
                time.sleep(2)
                from sentence_transformers import SentenceTransformer

            overall_start_time = time.time()

            # 1. Extract text from uploaded PDF
            with st.spinner("Extracting PDF..."):
                cv_resume_text = extract_text_from_pdf(uploaded_file)

            # 2. Get suggested occupations from CV text
            suggested_occupations = get_top_occupations_from_resume(
                cv_resume_text)
            st.write("Suggested Occupations Generated")

            # 3. Retrieve occupation list from CSV
            occupation_lists = get_occupation_list(csv_path, 'Occupations')
            st.write("Occupation List Generated")

            with st.spinner("Getting Similarity Scores..."):
                # 4. Compute similarity scores
                similarity_results_df = compute_similarity(
                    suggested_occupations, occupation_lists, model_name='all-mpnet-base-v2')

            # 5. Find best occupations
            final_df = find_max_per_row(similarity_results_df)
            st.write("Best Occupations Generated")

            # Remove digits from final matched suggestions
            final_df['suggested_from_cv'] = final_df['suggested_from_cv'].apply(
                remove_digits)

            # 6. Generate occupation data
            final_mapped_occupations = list(
                set(final_df['final_matched_suggestion'].to_list()))
            occupation_columns_dict, results = generate_occupation_data(
                csv_path, final_mapped_occupations)
            st.write("Occupation Data Generated")

            # 7. Generate results using OpenAI or LLM
            with st.spinner("Getting results from openai..."):
                result_openai = generate_new_results(
                    occupation_columns_dict, results)
                st.write("Results Generated")

            # 8. Parse LLM response
            final_result = parse_llm_response(result_openai)
            st.write("Results Parsed")

            # 9. Store new results in session state and display
            st.session_state.final_result = final_result

            overall_end_time = time.time()
            total_time = overall_end_time - overall_start_time
            st.write(f"Total time taken: {total_time} seconds")

    # If results are already stored in session state, display the details
    if "final_result" in st.session_state:
        display_occupation_details(st.session_state.final_result)


# Modular function to display the occupation results
def display_occupation_details(occupations):
    # Occupation selection dropdown
    occupation_names = [occupation['Occupation Name']
                        for occupation in occupations]

    selected_occupation = st.selectbox("Select Occupation", occupation_names)

    # Get the selected occupation details
    for occupation in occupations:
        if occupation['Occupation Name'] == selected_occupation:
            st.title(f"Occupation Details: {occupation['Occupation Name']}")

            st.write(f"**Occupation ID:** {occupation['occupation_id']}")
            st.write(f"**Occupation Name:** {occupation['Occupation Name']}")
            st.write(f"**ANZSCO Code:** {occupation['ANZSCO Code']}")
            st.write(f"**Caveats:** {occupation['Caveats']}")
            st.write(
                f"**Assessing Authority:** {occupation['Assessing Authority']}")

            # Displaying Migration Lists (only where value is "1")
            st.subheader("Australian Government Migration Lists")
            migration_filtered = [
                k for k, v in occupation['Australian Government Migration Lists'].items() if v == "1"]
            if migration_filtered:
                st.table(pd.DataFrame(migration_filtered, columns=['List']))

            # Displaying Visa Types (only where value is "1")
            st.subheader("Visa Type Availability")
            visa_filtered = [
                k for k, v in occupation['Visa Type'].items() if v == "1"]
            if visa_filtered:
                st.table(pd.DataFrame(visa_filtered, columns=['Visa Type']))

            # Displaying State and Subregion details (only where value is "1")
            st.subheader("State and Subregion Visa Availability")
            state_data = []
            for state, details in occupation['States'].items():
                if isinstance(details, dict):
                    for key, value in details.items():
                        if isinstance(value, dict):  # For subregions
                            for sub_key, sub_value in value.items():
                                if sub_value == "1":
                                    state_data.append([f"{key}", sub_key])
                        elif value == "1":  # For main regions
                            state_data.append([state, key])

            if state_data:
                state_df = pd.DataFrame(state_data, columns=[
                                        "State", "Category"])
                st.table(state_df)
