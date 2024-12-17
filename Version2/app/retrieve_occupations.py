import pandas as pd


def get_occupation_list(file_path, column_name):
    migration_df = pd.read_csv(file_path)
    occupation_list = migration_df[column_name].to_list()
    return occupation_list


