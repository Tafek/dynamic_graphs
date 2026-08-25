from functions.get_data import get_data
import pandas as pd
import csv


def get_separator(file):
    with open(file, "r", encoding="utf-8") as f:
        sample = f.read(5000)

    try:
        dialect = csv.Sniffer().sniff(
            sample,
            delimiters=";,|\t,"
        )

        return dialect.delimiter

    except csv.Error:
        return "," #Fallback to comma if no delimiter is detected


def get_dataframe(file):
    separator = get_separator(file)
    df_step_1 = pd.read_csv(file, sep=separator, header=None,skip_blank_lines=False)
    not_na_df = df_step_1.notna().sum(axis=1)
    max_cols = not_na_df.max()
    header_row = df_step_1[not_na_df == max_cols].index[0]
    df = pd.read_csv(file, sep=separator, header=header_row)
    return df

def get_cols(spec_dataset=None):
    datasets = get_data()
    col_selector_html = "<div class='col_selector'>"

    if spec_dataset is None:
        if datasets:
            selected_dataset = f"data/{datasets[0]}"
    else:
        selected_dataset = f"data/{spec_dataset}"

    if not selected_dataset:
        return "An Error occurred: No dataset selected."

    df = get_dataframe(selected_dataset)


    for col in df.columns:
        col_selector_html += f'<div class="col_item"><input type="checkbox" name="columns" value="{col}">{col}</div>'

    col_selector_html += "</div>"
    return col_selector_html
    