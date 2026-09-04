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
            values = df[col].dropna().astype(str)
            sample = values.head(min(1000, len(values)))

            if sample.str.fullmatch(r"[0-9,]+").all() and values.str.fullmatch(r"[0-9,]+").all():
                df[col] = df[col].str.replace(",", ".").astype(float)
            elif sample.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all() and values.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
                df[col] = pd.to_datetime(df[col])
            elif sample.str.fullmatch(r"\d{2}\.\d{2}\.\d{4}").all() and values.str.fullmatch(r"\d{2}\.\d{2}\.\d{4}").all():
                df[col] = pd.to_datetime(df[col], format="%d.%m.%Y")
            elif len(unique_values) <= 5:
                df[col] = df[col].astype("category")
        elif pd.api.types.is_float_dtype(df[col]) and df[col].dropna().apply(float.is_integer).all():
            df[col] = df[col].astype(int)
    return df


def get_dataframe(file):
    if not file:
        return pd.DataFrame()  # Return an empty DataFrame if no file is provided
    else:
        separator = get_separator(file)
        df_step_1 = pd.read_csv(file, sep=separator, header=None, skip_blank_lines=False, nrows=50)
        not_na_df = df_step_1.notna().sum(axis=1)
        max_cols = not_na_df.max()
        header_row = df_step_1[not_na_df == max_cols].index[0]
        df = pd.read_csv(file, sep=separator, header=header_row)
        df = clean_df(df)
        return df

def get_col_type(col):
    if pd.api.types.is_bool_dtype(col):
        return "boolean"
    elif pd.api.types.is_numeric_dtype(col):
        return "numeric"
    elif pd.api.types.is_categorical_dtype(col):
        return "categorical"
    elif pd.api.types.is_string_dtype(col):
        return "string"
    elif pd.api.types.is_datetime64_any_dtype(col):
        return "datetime"
    else:
        return "other"

def get_numeric_col_type(col):
    if pd.api.types.is_integer_dtype(col):
        return "integer"
    elif pd.api.types.is_float_dtype(col):
        return "float"
    else:
        return "other"

def get_aggregation_options(graph_type,active_aggregation=None):
    # Für das Pie-Chart machen manche Aggregationen nur bedingt viel Sinn, aber theoretisch kann man auch die Minimalwerte zweier Kategorien in Verhältnis setzen wollen
    if graph_type in ["bar","line","pie"]:
        aggregation_html =  'Please select an aggregation method:<br>' \
                            '<select name="aggregation" onchange="this.form.submit()">' \
                            f'<option value="count" {"selected" if active_aggregation == "count" else ""}>Count</option>' \
                            f'<option value="sum" {"selected" if active_aggregation == "sum" else ""}>Sum</option>' \
                            f'<option value="mean" {"selected" if active_aggregation == "mean" else ""}>Mean</option>' \
                            f'<option value="median" {"selected" if active_aggregation == "median" else ""}>Median</option>' \
                            f'<option value="max" {"selected" if active_aggregation == "max" else ""}>Max</option>' \
                            f'<option value="min" {"selected" if active_aggregation == "min" else ""}>Min</option>' \
                            '</select>'
    else:
        aggregation_html = ""
    
    return aggregation_html

def get_cols(spec_dataset=None, graph_type="line", cols_1=None, cols_2=None, active_aggregation=None):
    import config
    datasets = get_data()
    no_x_col_types = config.no_x_col_types
    single_y_col_types = config.single_y_col_types_mandatory

    if graph_type in single_y_col_types:
        col_selector_html = "<p>Please select a column for the Y-axis.</p><div class='col_selector'><div class='col_item_container'>"
    else:
        col_selector_html = "<p>Please select columns for the Y-axis.</p><div class='col_selector'><div class='col_item_container'>"

    if spec_dataset is None:
        if datasets:
            selected_dataset = f"data/{datasets[0]}"
        else:
            selected_dataset = None
    else:
        selected_dataset = f"data/{spec_dataset}"

    if not selected_dataset:
        return "No dataset selected."

    if graph_type in single_y_col_types:
        input_type = "radio"
    else:
        input_type = "checkbox"

    df = get_dataframe(selected_dataset)
    aggregation_options = get_aggregation_options(graph_type, active_aggregation=active_aggregation)
    for col in df.columns:
        col_type = get_col_type(df[col])
        if ((graph_type == "hist" or graph_type=="boxplot") and col_type!="numeric") \
            or (active_aggregation in ["sum", "mean", "median", "max", "min"] and col_type!="numeric"):
            active_checkbox = "disabled"
        else:
            active_checkbox = ""
        col_selector_html += f'<div class="col_item">' \
                            f'<div class="col_checkbox"><input type="{input_type}" onchange="this.form.submit()" name="columns_1" value="{col}" {active_checkbox} {"checked" if cols_1 and col in cols_1 else ""}>{col}</div>' \
                            f'<div class="col_type"><i>({col_type})</i></div>' \
                            f'</div>'
    col_selector_html += f'</div><div class="agg_selector">{aggregation_options}</div>' \
                         f'</div>'

    if graph_type not in no_x_col_types:
        col_selector_html += "<br><p>Please select a column for the X-axis.</p><div class='col_selector_x'><div class='col_item_container'>"
        for col in df.columns:
            col_type = get_col_type(df[col])
            col_selector_html += f'<div class="col_item">' \
                                f'<div class="col_checkbox"><input type="radio" onchange="this.form.submit()" name="columns_2" value="{col}" {"checked" if cols_2 and col in cols_2 else ""}>{col}</div>' \
                                f'<div class="col_type"><i>({col_type})</i></div>' \
                                f'</div>'
        col_selector_html += '</div></div>'
    return col_selector_html

def col_rules_info(graph_type):

    import config
    no_x_col_types = config.no_x_col_types
    single_y_col_types   = config.single_y_col_types_mandatory

    if graph_type == "":
        info_box = "<div class='info_box'><div class='info_box_left'>Select the columns to be visualized<br><br></div><div class='info_box_right'>"
        info_box += "<p>Please select a graph type to see the rules for column selection.</p>"
        info_box += "</div></div>"
        return info_box

    info_box = "<div class='info_box'><div class='info_box_left'>Select the columns to be visualized<br><br></div><div class='info_box_right'>"
    info_box += "<p>Please note the following for your selected graph type:</p><ul>"

    if graph_type in single_y_col_types:
        info_box += "<li>This Graph accepts exactly one Y-axis.</li>"
    else:   
        info_box += "<li>This Graph accepts one or more columns for the Y-axis.</li>"
        
    if graph_type in no_x_col_types:
        info_box += "<li>This Graph does not accept a column for the X-axis.</li>"
    else:
        info_box += "<li>This Graph requires a column for the X-axis.</li>"

    info_box += "</ul></div></div>"
    return info_box

def get_amount_rows(df=None):
    if df is None:
        return 0
    return df.shape[0]

def get_amount_cols(df=None):
    if df is None:
        return 0
    return df.shape[1]