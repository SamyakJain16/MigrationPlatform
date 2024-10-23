import re
# from get_best_occupations import final_df
# Define a function to remove digits at the start of the text


def remove_digits(text):
    # Remove any non-letter characters from the start
    return re.sub(r'^[^a-zA-Z]+', '', str(text))


# Apply this function to the desired column (e.g., 'YourColumn')
