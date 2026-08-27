from flask import Flask, render_template, request
from functions.get_data import get_data_dropdown
from functions.get_cols import get_cols
from functions.get_cols import get_dataframe
from functions.test_function import display_head
from functions.show_graph import show_graph

import config


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    # Set Standard Values
    spec_dataset = None
    visual_type = None
    columns_1 = []
    columns_2 = []
    generated_graph = None

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

    # --------------------------------
    # Dataset / Columns / Head
    # --------------------------------

    if spec_dataset:
        dropdown_html = get_data_dropdown(spec_dataset)
        columns_html = get_cols(spec_dataset, graph_type=visual_type, cols_1=columns_1, cols_2=columns_2)
        test_header = display_head(
            get_dataframe(f"data/{spec_dataset}")
        )
    else:
        dropdown_html = get_data_dropdown()
        columns_html = get_cols(graph_type=visual_type, cols_1=columns_1, cols_2=columns_2)
        test_header = display_head()

    # --------------------------------
    # Generate Graph
    # --------------------------------

    if spec_dataset and visual_type:

        if visual_type in ["line", "hist", "bar", "pie"] and (len(columns_2) == 0 or len(columns_1) == 0):
            generated_graph = "<p>For this visualization, two columns must be selected.</p>"
            # Fallback to display the head of the dataset if no graph is shown
            generated_graph += display_head(get_dataframe(f"data/{spec_dataset}"))

        elif visual_type in ["pie","scatter"] and len(columns_1) < 1:
            generated_graph = "<p>Please select at least one column.</p>"
            # Fallback to display the head of the dataset if no graph is shown
            generated_graph += display_head(get_dataframe(f"data/{spec_dataset}"))

        else:
            generated_graph = show_graph(
                type=visual_type,
                cols_1=columns_1,
                cols_2=columns_2,
                df=get_dataframe(f"data/{spec_dataset}")
            )
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
        generated_graph=generated_graph,
        spec_dataset=spec_dataset,
        visual_type=visual_type,
        columns_1=columns_1,
        columns_2=columns_2
    )


if __name__ == "__main__":
    app.run(debug=True)