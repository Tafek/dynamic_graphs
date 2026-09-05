from functions.get_cols import get_col_type, get_dataframe, get_numeric_col_type


def get_filters(spec_dataset=None, form_data=None):
    if spec_dataset is None:
        return "<p>No dataset selected.</p>"
    else:
        filter_html = "<div class='filter_container'>"
        df = get_dataframe(f"data/{spec_dataset}")
        for col in df.columns:
            col_type = get_col_type(df[col])
            if col_type == "numeric":
                min_val = df[col].min()
                max_val = df[col].max()
                selected_min = form_data.get(f"filter_{col}_min", min_val)
                selected_max = form_data.get(f"filter_{col}_max", max_val)
                numeric_col_type = get_numeric_col_type(df[col])
                if numeric_col_type == "integer":
                    step_size = 1
                else:
                    step_size = "any"

                filter_html += "<div class='filter_item'>"
                filter_html += f"<label>{col} (Numeric - {numeric_col_type}):</label>"
                filter_html += "<div class='range_inputs'>"
                filter_html += f"<input type='number' name='filter_{col}_min' value='{selected_min}' min='{min_val}' max='{max_val}' step='{step_size}' onchange='this.form.submit()'>"
                filter_html += f"<input type='number' name='filter_{col}_max' value='{selected_max}' min='{min_val}' max='{max_val}' step='{step_size}' onchange='this.form.submit()'></div>"
                filter_html += "<div class='range_slider'>"
                filter_html += f"<input type='range' id='{col}_slider_min' min='{min_val}' max='{max_val}' value='{selected_min}' step='{step_size}' onchange=\"document.querySelector('[name=filter_{col}_min]').value = this.value; this.form.submit()\">"
                filter_html += f"<input type='range' id='{col}_slider_max' min='{min_val}' max='{max_val}' value='{selected_max}' step='{step_size}' onchange=\"document.querySelector('[name=filter_{col}_max]').value = this.value; this.form.submit()\"></div></div>"
        filter_html += "</div>"
    return filter_html