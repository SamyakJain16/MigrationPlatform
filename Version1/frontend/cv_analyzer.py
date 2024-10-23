import os
import openai


def get_top_occupations_from_resume(cv_text):

    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    """
    Function to analyze a CV/resume and return the top three occupations based on experience, education, and skills.

    Args:
        cv_text (str): The text content of the CV/resume.

    Returns:
        list: A list of the top three suggested occupation names.
    """

    # Craft the prompt
    prompt = f"""
    Please analyze the following CV/resume and provide the top three best occupations.
    Just provide the occupation names as a list and nothing else.
    Here is the CV/resume:

    {cv_text}
    """

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a career advisor and resume expert."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and clean the response
    suggested_occupations = response.choices[0].message.content.split("\n")

    return suggested_occupations

# Example usage
# top_occupations = get_top_occupa
