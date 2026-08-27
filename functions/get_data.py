import os


def get_data():
    datasets = []

    for file in os.listdir("data"):
        if file.endswith(".csv"):
            datasets.append(file)

    return datasets

def get_data_dropdown(active=None):
    datasets = get_data()
    dropdown_html = ""

    for dataset in datasets:
        if active and dataset == active:
            dropdown_html += f'<option value="{dataset}" selected>{dataset}</option>'
        else:
            dropdown_html += f'<option value="{dataset}">{dataset}</option>'

    return dropdown_html