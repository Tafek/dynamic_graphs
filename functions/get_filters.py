from functions.get_cols import get_col_type, get_dataframe, get_numeric_col_type


def get_filters(spec_dataset=None, form_data=None, dataset_switched=False):
    if spec_dataset is None:
        return "<p>No dataset selected.</p>"
    else:
        contains_numeric_filter = False
        contains_other_filters = False
        filter_html = "<div class='filter_container'>"
        filter_html_numeric = ""
        filter_html_string = ""
        filter_html_categorial = ""
        filter_html_bool = ""
        filter_html_date = ""
        df = get_dataframe(f"data/{spec_dataset}")
        for col in df.columns:
            col_type = get_col_type(df[col])
            if col_type == "numeric":
                contains_numeric_filter = True
                min_val = df[col].min()
                max_val = df[col].max()
                selected_min = form_data.get(f"filter_numeric_{col}_min", min_val)
                selected_max = form_data.get(f"filter_numeric_{col}_max", max_val)
                min_val_max = max(min_val, float(selected_min))
                max_val_min = min(max_val, float(selected_max))
                numeric_col_type = get_numeric_col_type(df[col])
                if numeric_col_type == "integer":
                    step_size = 1
                else:
                    step_size = "any"

                filter_html_numeric += "<div class='filter_item'>"
                filter_html_numeric += f"<label>{col} (Numeric - {numeric_col_type}):</label>"
                filter_html_numeric += "<div class='range_inputs'>"
                filter_html_numeric += f"<input type='number' id='filter_numeric_{col}_min' name='filter_numeric_{col}_min' value='{selected_min}' min='{min_val}' max='{max_val_min}' step='{step_size}' onchange='this.form.submit()'>"
                filter_html_numeric += f"<input type='number' id='filter_numeric_{col}_max' name='filter_numeric_{col}_max' value='{selected_max}' min='{min_val_max}' max='{max_val}' step='{step_size}' onchange='this.form.submit()'>"
                filter_html_numeric += "<div class='range_slider'>"
                filter_html_numeric += f"<input type='range' id='{col}_slider_min' min='{min_val}' max='{max_val_min}' value='{selected_min}' step='{step_size}' onchange=\"document.getElementById('filter_numeric_{col}_min').value = this.value; this.form.submit()\">"
                filter_html_numeric += f"<input type='range' id='{col}_slider_max' min='{min_val_max}' max='{max_val}' value='{selected_max}' step='{step_size}' onchange=\"document.getElementById('filter_numeric_{col}_max').value = this.value; this.form.submit()\">"
                filter_html_numeric += "</div></div></div>"
                filter_html_numeric += "<br>"
            elif col_type == "categorical":
                contains_other_filters = True
                unique_values = df[col].unique()
                selected_values = form_data.getlist(f"filter_category_{col}")
                filter_html_categorial += "<div class='filter_item'>"
                filter_html_categorial += f"<label>{col} (Categorical):</label>"
                filter_html_categorial += "<div class='checkbox_group'>"
                categorial_counter = 0
                for value in unique_values:
                    if value in selected_values or dataset_switched == True:
                        checked = "checked" 
                    else:
                        checked = "" 
                    if categorial_counter >= 3:
                        filter_html_categorial += "<br>"
                        categorial_counter = 0
                    filter_html_categorial += f"<label><input type='checkbox' name='filter_category_{col}' value='{value}' {checked} onchange='this.form.submit()'>{value}</label>"
                    categorial_counter += 1
                    
                filter_html_categorial += f"<input type='hidden' name='filter_category_active_{col}' value='1'>"
                filter_html_categorial += "</div></div>"
                filter_html_categorial += "<br>"
            elif col_type == "boolean":
                contains_other_filters = True
                selected_values = form_data.getlist(f"filter_bool_{col}")
                filter_html_bool += "<div class='filter_item'>"
                filter_html_bool += f"<label>{col} (Boolean):</label>"
                filter_html_bool += "<div class='checkbox_group'>"
                for value in ["True", "False"]:
                    if dataset_switched == True or (not form_data and value in ["True", "False"]) or value in selected_values:
                        checked = "checked" 
                    else:
                        checked = "" 
                    filter_html_bool += f"<label><input type='checkbox' name='filter_bool_{col}' value='{value}' {checked} onchange='this.form.submit()'>{value}</label>"
                filter_html_bool += f"<input type='hidden' name='filter_bool_active_{col}' value='1'>"
                filter_html_bool += "</div></div>"
                filter_html_bool += "<br>"
            elif col_type == "string":
                contains_other_filters = True
                filter_html_string += "<div class='filter_item'>"
                filter_html_string += f"<label>{col} (String):</label>"
                filter_html_string += "<div class='regex_input'>"
                filter_html_string += f"<input type='text' name='filter_string_regex_{col}' value='{form_data.get(f'filter_string_regex_{col}', '')}' placeholder='Enter regex' onchange='this.form.submit()'>"
                filter_html_string += "<option value=''></option>"
                filter_html_string += f"<select name='filter_string_inclexcl_{col}' onchange='this.form.submit()'>"
                filter_html_string += f"<option value='include' {'selected' if form_data.get(f'filter_string_inclexcl_{col}', '') == 'include' else ''}>Include</option>"
                filter_html_string += f"<option value='exclude' {'selected' if form_data.get(f'filter_string_inclexcl_{col}', '') == 'exclude' else ''}>Exclude</option>"
                filter_html_string += "</select>"
                filter_html_string += "</div></div>"
                filter_html_string += "<br>"
            elif col_type == "datetime":
                min_val = df[col].min()
                max_val = df[col].max()
                selected_min = form_data.get(f"filter_datetime_{col}_min", min_val)
                selected_max = form_data.get(f"filter_datetime_{col}_max", max_val)

                filter_html_date += "<div class='filter_item'>"
                filter_html_date += f"<label>{col} (Datetime):</label>"
                filter_html_date += "<div class='date_range_inputs'>"
                filter_html_date += f"<input type='datetime-local' name='filter_datetime_{col}_min' value='{selected_min}' min='{min_val}' max='{max_val}' onchange='this.form.submit()'>"
                filter_html_date += f"<input type='datetime-local' name='filter_datetime_{col}_max' value='{selected_max}' min='{min_val}' max='{max_val}' onchange='this.form.submit()'></div></div>"
                filter_html_date += "<br>"
        if contains_numeric_filter:
            filter_html += "<div class='filters_left'>"
            filter_html += filter_html_numeric
            filter_html += "</div>"
        if contains_other_filters:
            filter_html += "<div class='filters_right'>"
            filter_html += filter_html_bool
            filter_html += filter_html_date
            filter_html += filter_html_categorial
            filter_html += filter_html_string
            filter_html += "</div>"
        filter_html += "</div>"
    return filter_html