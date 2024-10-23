import openai
import os
import json
# from get_results_schema import occupation_columns_dict, results


# Function to make OpenAI API call


# Main function to generate and update results


def generate_new_results(occupation_columns_dict, results):
    # Initialize OpenAI API client
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def call_openai_api(prompt):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a highly intelligent assistant tasked with mapping elements from a list to the most related keys in a dictionary."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    new_results = []

    # Loop through occupation_columns_dict and results
    for index, (occupation, obtained_list) in enumerate(occupation_columns_dict.items()):
        # Prepare the prompt for the OpenAI API
        prompt = f"""
        Prompt:
        I have an obtained_list of migration lists, visa types, and state nominations, and I want to update a results dictionary.

        Output Format: Json
        Only output the updated results in exactly the same structure as provided. Only the values should be updated to "1" for matched elements and "0" for unmatched elements. Do not output anything else.
        obtained_list = {obtained_list}
        results = {results[index]}
        """

        # Make the API call
        api_response = call_openai_api(prompt)

        # Append the response to new_results
        new_results.append(api_response)

    return new_results


# Generate the new results
# result_openai = generate_new_results(occupation_columns_dict, results)

#
# Optionally, you can load the file in another script to reuse new_results
