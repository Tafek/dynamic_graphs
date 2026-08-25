from flask import Flask, render_template, request
from functions.get_data import get_data_dropdown
from functions.get_cols import get_cols

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        dropdown_html = get_data_dropdown(request.form["dataset"])
        spec_dataset = request.form["dataset"]
        columns_html = get_cols(spec_dataset)
    else:
        dropdown_html = get_data_dropdown()
        columns_html = get_cols()


    if dropdown_html:
        message_no_datasets = ""
    else:
        message_no_datasets = "Füge deinem Projekt noch Daten im Data-Folder hinzu."

    return render_template(
        "index.html",
        dropdown_html= dropdown_html, # HTML für das Dropdown-Menü der Datasets
        message_no_datasets=message_no_datasets, # Fehlermeldung, falls keine Datasets vorhanden sind
        columns_html= columns_html # HTML für die Spaltenauswahl des ersten Datasets
    )


if __name__ == "__main__":
    app.run(debug=True)