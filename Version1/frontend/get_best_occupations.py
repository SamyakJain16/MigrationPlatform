import pandas as pd


def find_max_per_row(similarity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Find the maximum value and corresponding column for each row in a similarity DataFrame.

    Parameters:
    similarity_df (pd.DataFrame): A DataFrame where rows represent `sentences1` and columns represent `sentences2`.

    Returns:
    pd.DataFrame: A new DataFrame containing the index (sentences1), the maximum value in each row,
                  and the corresponding column name.
    """
    # Check if DataFrame is empty
    if similarity_df.empty:
        raise ValueError("The input DataFrame is empty.")

    # Initialize lists to store results
    max_values = []
    max_columns = []

    # Iterate through each row in the DataFrame
    for index, row in similarity_df.iterrows():
        # Find the maximum value in the current row
        max_value = row.max()

        # Find the column corresponding to the maximum value
        max_column = row.idxmax()

        # Append the results to the lists
        max_values.append(max_value)
        max_columns.append(max_column)

    # Create a new DataFrame to store the results
    result_df = pd.DataFrame({
        'suggested_from_cv': similarity_df.index,  # Row index, which is sentences1
        'max_value': max_values,
        'final_matched_suggestion': max_columns
    })

    return result_df


# final_df = find_max_per_row(similarity_results_df)


# Apply this function to the desired column (e.g., 'YourColumn')
# final_df['suggested_from_cv'] = final_df['suggested_from_cv'].apply(remove_digits)

# final_mapped_occupations = final_df['final_matched_suggestion'].to_list()
