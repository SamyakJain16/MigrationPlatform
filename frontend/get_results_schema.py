import pandas as pd
# from get_best_occupations import final_mapped_occupations


def generate_occupation_data(csv_path, final_mapped_occupations):
    """
    Function to generate occupation data based on a CSV file and a list of occupations.

    Args:
        csv_path (str): Path to the CSV file containing the occupation details.
        final_mapped_occupations (list): A list of occupations to be matched in the CSV.

    Returns:
        tuple: A tuple containing:
            - occupation_columns_dict: A dictionary with occupation names and their relevant columns.
            - results: A list of dictionaries (schemas) containing occupation details.
    """

    # Read the CSV file
    df = pd.read_csv(csv_path)
    anzsco_code_column = 'ANZSCO\nCode'
    caveats_column = 'Caveats'
    assessing_authority_column = 'Assessing authority\n'
    occupation_name_column = 'Occupations'

    occupation_columns_dict = {}
    results = []

    # Loop through each occupation in your list
    for index, occupation in enumerate(final_mapped_occupations):
        # Initialize the schema

        schema = {
            "occupation_id": "",
            "Occupation Name": "",
            "ANZSCO Code": "",
            "Caveats": "",
            "Assessing Authority": "",
            "Australian Government Migration Lists": {
                "MLTSSL": "",
                "STSOL": "",
                "ROL": "",
                "PMSOL": ""
            },
            "Visa Type": {
                "TSS": "",
                "ENS-SC186": "",
                "RSMS - SC187 Transition": "",
                "SC 189": "",
                "SC 190": "",
                "SC 491 S/T Nominated": "",
                "SC 491 Family Sponsored": "",
                "SC 494": "",
                "SC 485": "",
                "SC 407": "",
            },
            "States": {
                "ACT": {"190": "", "491": ""},
                "NSW": {
                    "190": "", "491*": "",
                    "NSW Central Coast": {"190": "", "491": ""},
                    "NSW Central West": {"190": "", "491": ""},
                    "NSW Far South Coast": {"190": "", "491": ""},
                    "NSW Far West": {"190": "", "491": ""},
                    "NSW Hunter": {"190": "", "491": ""},
                    "NSW Illawara": {"190": "", "491": ""},
                    "NSW Mid North Coast": {"190": "", "491": ""},
                    "NSW Northern Inland": {"190": "", "491": ""},
                    "NSW Northern Rivers": {"190": "", "491": ""},
                    "NSW Northern Orana": {"190": "", "491": ""},
                    "NSW Rivarina": {"190": "", "491": ""},
                    "NSW Southern Inland": {"190": "", "491": ""},
                    "NSW Sydney": {"190": "", "491": ""}
                },
                "NT": {"190": "", "491": ""},
                "QLD": {"190": "", "491": ""},
                "SA": {"190": "", "491": ""},
                "TAS": {"190": "", "491": ""},
                "VIC": {"190": "", "491": ""},
                "WA": {"190": "", "491": ""}
            }
        }

        # Find the row that matches the occupation name in the CSV file
        matched_row = df[df[occupation_name_column] == occupation]

        if not matched_row.empty:
            # Get all the column names where the value is 1 for the matched occupation
            columns_with_1 = matched_row.loc[:,
                                             (matched_row == 1).any()].columns.tolist()
            occupation_columns_dict[occupation] = columns_with_1

            def get_column_value(column_name):
                if column_name in matched_row.columns:
                    return matched_row[column_name].values[0]
                return "Column not found"

            # Extract column values
            occupation_name = get_column_value(occupation_name_column)
            caveats = get_column_value(caveats_column)
            anzsco_code = get_column_value(anzsco_code_column)
            assessing_authority = get_column_value(assessing_authority_column)

            # Update schema with data
            schema['occupation_id'] = int(anzsco_code)
            schema['Occupation Name'] = occupation_name
            schema['ANZSCO Code'] = int(anzsco_code)
            schema['Assessing Authority'] = assessing_authority
            schema['Caveats'] = caveats

            # Append the schema to results
            results.append(schema)

        else:
            print(f"No match found for occupation: {occupation}")

    return occupation_columns_dict, results

# Example usage
# csv_path = '/path/to/occupation_list_main.csv'
# final_results = generate_occupation_data(csv_path, final_mapped_occupations)
# print(final_results)
