import os

from flask import Flask, render_template, request

from functions.get_cols import (
    col_rules_info,
    get_amount_cols,
    get_amount_rows,
    get_cols,
    get_dataframe,
    get_filtered_df,
)
from functions.get_data import get_data_dropdown
from functions.get_filters import get_filters
from functions.show_graph import display_head, show_graph

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    # Set Standard Values
    spec_dataset = None
    visual_type = None
    columns_1 = []
    columns_2 = []
    generated_graph = None
    df_num_filters = {}

    old_dataset = request.form.get("old_dataset")

    if request.method == "POST":

        # Fetch current Dataset from Form
        spec_dataset = request.form.get("dataset")

        # Fetch current Visualization type from the Form
        visual_type = request.form.get("visual_type")
        if visual_type is None:
            visual_type = "line"

        # Fetch selected columns
        columns_1 = request.form.getlist("columns_1")
        columns_2 = request.form.getlist("columns_2")
        if old_dataset == spec_dataset:
            columns_1 = request.form.getlist("columns_1")
            columns_2 = request.form.getlist("columns_2")
            if request.method == "POST":
                for key, value in request.form.items():
                    if key.startswith("filter_") and value != "":
                        parts = key.rsplit("_", 1)
                        col = parts[0][7:]
                        filter_type = parts[1]
                        if col not in df_num_filters:
                            df_num_filters[col] = {}
                        df_num_filters[col][filter_type] = float(value)
        else:
            columns_1 = []
            columns_2 = []

    # --------------------------------
    # Dataset / Columns / Head
    # --------------------------------
    if not os.path.exists(f"data/{spec_dataset}"):
        spec_dataset = None
        columns_1 = []
        columns_2 = []

    if spec_dataset:
        df = get_dataframe(f"data/{spec_dataset}")
        filtered_df = get_filtered_df(df, df_num_filters)
        dropdown_html = get_data_dropdown(spec_dataset)
        columns_html = get_cols(spec_dataset, graph_type=visual_type, cols_1=columns_1, cols_2=columns_2, active_aggregation=request.form.get("aggregation"))
        html_filters = get_filters(spec_dataset, form_data=request.form)
        test_header = display_head(df)
        df_cols = get_amount_cols(df)
        df_rows = get_amount_rows(df)
        df_filtered_rows = get_amount_rows(filtered_df)
    else:
        df = None
        dropdown_html = get_data_dropdown()
        columns_html = get_cols(graph_type=visual_type, cols_1=columns_1, cols_2=columns_2, active_aggregation=request.form.get("aggregation"))
        html_filters = get_filters()
        test_header = display_head()
        df_cols = get_amount_cols(df)
        df_rows = get_amount_rows(df)
        df_filtered_rows = df_rows

    # --------------------------------
    # Generate Graph
    # --------------------------------
    active_tab = request.form.get("tabs", "table")
    if active_tab not in ["table", "graph"]:
        active_tab = "table"

    tab_box = f"<div class='tabbox'> \
                <!-- Tabs --> \
                <input type='radio' name='tabs' id='tab1' value='table' {'checked' if active_tab == 'table' else ''}> \
                <label for='tab1'>Show first 15 table rows</label> \
                <input type='radio' name='tabs' id='tab2' value='graph' {'checked' if active_tab == 'graph' else ''}> \
                <label for='tab2'>Show Graph and Options</label>\
                <!-- Inhalte -->"
                        


    generated_graph = '<div class="graph_container_full">'
    if spec_dataset and visual_type:
        generated_graph += '<div class="graph_container_left">'
        if visual_type in ["line", "scatter", "bar", "pie","boxplot"] and (len(columns_2) == 0 or len(columns_1) == 0):
            generated_graph += "<p>For this visualization, two columns must be selected.</p>"
            

        elif visual_type in ["hist"] and len(columns_1) < 1:
            generated_graph += "<p>Please select at least one column.</p>"
            generated_graph += display_head(df)

        else:
            generated_graph += show_graph(  type=visual_type,
                                            cols_1=columns_1,
                                            cols_2=columns_2,
                                            df=filtered_df,
                                            method=request.form.get("aggregation"))
            generated_graph += "</div>"
            #generated_graph += show_graph_settings( type=visual_type,
            #                                        cols_1=columns_1,
            #                                        cols_2=columns_2,
            #                                        df=df)
            generated_graph += '<div class="graph_container_right">Placeholder for further Visual Settings (Avg. etc.)</div>'
        #generated_graph += '</div>'
    else:
        generated_graph += "<p>Please select a dataset and a visualization type.</p></div>"

    if not spec_dataset:
        generated_table_head = "<p>No dataset selected.</p>"
    else:
        generated_table_head = display_head(df)
    tab_box +=  f"<div class='tab-content content1'> \
                {generated_table_head} \
                </div>"

    
    
    tab_box += f"<div class='tab-content content2'> \
                {generated_graph} \
                </div> \
                </div>"
    # --------------------------------
    # No Datasets Available?
    # --------------------------------

    if dropdown_html:
        message_no_datasets = ""
    else:
        message_no_datasets = ("Add some data to your project in the Data folder.")

    return render_template(
        "index.html",
        dropdown_html=dropdown_html,
        message_no_datasets=message_no_datasets,
        columns_html=columns_html,
        test_header=test_header,
        generated_graph=tab_box,
        spec_dataset=spec_dataset,
        visual_type=visual_type,
        columns_info = col_rules_info(visual_type),
        columns_1=columns_1,
        columns_2=columns_2,
        html_filters = html_filters,
        df_cols = df_cols,
        df_rows = df_rows,
        df_filtered_rows = df_filtered_rows
        
    )


if __name__ == "__main__":
    app.run(debug=True)