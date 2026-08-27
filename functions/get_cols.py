import csv

import pandas as pd

from functions.get_data import get_data


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


def clean_df(df):
    df = df.dropna(how="all")  # Drop rows where all elements are NaN
    df = df.dropna(axis=1, how="all")  # Drop columns where all elements are NaN
    for col in df.columns:
        unique_values = df[col].unique()
        if pd.api.types.is_numeric_dtype(df[col]) and len(unique_values) == 2:
            df[col] = df[col].astype('bool')  # Convert to bool if exactly two unique values
        elif pd.api.types.is_string_dtype(df[col]):

            # Nur für die Prüfungen in String umwandeln
            values = df[col].dropna().astype(str)

            # Zahlen mit Komma
            if values.str.fullmatch(r"[0-9,]+").all():
                df[col] = df[col].str.replace(",", ".").astype(float)

            # YYYY-MM-DD
            elif values.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
                df[col] = pd.to_datetime(df[col])

            # DD.MM.YYYY
            elif values.str.fullmatch(r"\d{2}\.\d{2}\.\d{4}").all():
                df[col] = pd.to_datetime(
                    df[col],
                    format="%d.%m.%Y"
                )

            # Wenige verschiedene Werte
            elif len(unique_values) <= 5:
                df[col] = df[col].astype("category")
        elif pd.api.types.is_float_dtype(df[col]) and df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype(int)
    return df


def get_dataframe(file):
    separator = get_separator(file)
    df_step_1 = pd.read_csv(file, sep=separator, header=None,skip_blank_lines=False)
    not_na_df = df_step_1.notna().sum(axis=1)
    max_cols = not_na_df.max()
    header_row = df_step_1[not_na_df == max_cols].index[0]
    df = pd.read_csv(file, sep=separator, header=header_row)
    df = clean_df(df)
    return df

def get_col_type(df, col):
    if pd.api.types.is_numeric_dtype(col):
        return "numeric"
    elif pd.api.types.is_bool_dtype(col):
        return "boolean"
    elif pd.api.types.is_categorical_dtype(col):
        return "categorical"
    elif pd.api.types.is_string_dtype(col):
        return "string"
    elif pd.api.types.is_datetime64_any_dtype(col):
        return "datetime"
    else:
        return "other"

def get_aggregation_options(graph_type):
    # Für das Pie-Chart machen manche Aggregationen nur bedingt viel Sinn, aber theoretisch kann man auch die Minimalwerte zweier Kategorien in Verhältnis setzen wollen
    if graph_type in ["bar","line","pie"]:
        aggregation_html =  'Please select an aggregation method:<br>' \
                            '<select name="aggregation">' \
                            '<option value="count">Count</option>' \
                            '<option value="sum">Sum</option>' \
                            '<option value="mean">Mean</option>' \
                            '<option value="median">Median</option>' \
                            '<option value="max">Max</option>' \
                            '<option value="min">Min</option>' \
                            '</select>'
    else:
        aggregation_html = ""
    
    return aggregation_html

def get_cols(spec_dataset=None, graph_type="line", cols_1=None, cols_2=None):
    import config
    datasets = get_data()
    no_x_col_types = config.no_x_col_types

    col_selector_html = "<p>Please select columns for the Y-axis.</p><div class='col_selector'><div class='col_item_container'>"

    if spec_dataset is None:
        if datasets:
            selected_dataset = f"data/{datasets[0]}"
    else:
        selected_dataset = f"data/{spec_dataset}"

    if not selected_dataset:
        return "An Error occurred: No dataset selected."

    df = get_dataframe(selected_dataset)
    aggregation_options = get_aggregation_options(graph_type)
    for col in df.columns:
        col_selector_html += f'<div class="col_item">' \
                            f'<div class="col_checkbox"><input type="checkbox" onchange="this.form.submit()" name="columns_1" value="{col}" {"checked" if cols_1 and col in cols_1 else ""}>{col}</div>' \
                            f'<div class="col_type"><i>({get_col_type(df,df[col])})</i></div>' \
                            f'</div>'
    col_selector_html += f'</div><div class="agg_selector">{aggregation_options}</div>' \
                         f'</div>'

    if graph_type not in no_x_col_types:
        col_selector_html += "<br><p>Please select a column for the X-axis.</p><div class='col_selector_x'><div class='col_item_container'>"
        for col in df.columns:
            col_selector_html += f'<div class="col_item">' \
                                f'<div class="col_checkbox"><input type="checkbox" onchange="this.form.submit()" name="columns_2" value="{col}" {"checked" if cols_2 and col in cols_2 else ""}>{col}</div>' \
                                f'<div class="col_type"><i>({get_col_type(df,df[col])})</i></div>' \
                                f'</div>'
        col_selector_html += '</div></div>'
    return col_selector_html

def col_rules_info(graph_type):
    import config
    single_x_col_types_obligatory = config.single_x_col_types_obligatory
    single_x_col_types_optional   = config.single_x_col_types_optional
    multi_y_col_types_optional  = config.multi_y_col_types_optional

    if graph_type in single_x_col_types_obligatory:
        return "<p>For this visualization, one column must be selected for the X-axis.</p>"
    elif graph_type in single_x_col_types_optional:
        return "<p>For this visualization, one column can optionally be selected for the X-axis.</p>"
    elif graph_type in multi_y_col_types_optional:
        return "<p>For this visualization, one or more columns can be selected for the Y-axis.</p>"
    else:
        return "<p>No specific rules for column selection for this visualization.</p>"