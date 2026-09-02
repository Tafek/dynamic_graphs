#https://matplotlib.org/stable/plot_types/index.html

import base64
import io

import matplotlib
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype

matplotlib.use("Agg")


def show_graph(type="line", cols_1=None, cols_2=None, filters=None, settings=None, df=None, method="count"):

    if df is None:
        return "<p>Kein Dataset ausgewählt.</p>"

    if cols_1 is None or len(cols_1) == 0:
        return "<p>Keine Spalten für die Y-Achse ausgewählt.</p>"

    if type in ["line", "scatter", "bar", "pie"] and (len(cols_2) == 0 or len(cols_1) == 0):
        return "<p>Diese Visualisierung benötigt zwei Spalten.</p>"

    #if cols_2 and len(cols_2) > 0:
    #    n_groups = df[cols_2[0]].nunique()
    #    if type in ["bar", "pie"] and n_groups > 50:
    #        return f"<p>Too many (>50) unique values in '{cols_2[0]}' ({n_groups}). Please select another column or apply filters.</p>"

    fig, ax = plt.subplots()
    if method == "" or method is None:
        method = "count"

    match type:
        case "line":
            if method=="count" or all(is_numeric_dtype(df[col]) for col in cols_1):
                df.groupby(cols_2[0])[cols_1].agg(method).plot.line(ax=ax)
            else:
                return "<p>For this combination of visualization and aggregation method, the selected Y-axis column must be numeric.</p>"

        case "scatter":
            ax.scatter(df[cols_2[0]], df[cols_1[0]])

        case "bar":
            if method=="count" or all(is_numeric_dtype(df[col]) for col in cols_1):
                df.groupby(cols_2[0])[cols_1].agg(method).plot.bar(ax=ax)
            else:
                return "<p>For this combination of visualization and aggregation method, the selected Y-axis column must be numeric.</p>"

        case "hist":
            df[cols_1].plot.hist(ax=ax)

        case "":
            if all(is_numeric_dtype(df[col]) for col in cols_1):
                df.boxplot(column=cols_1, by=cols_2[0], ax=ax)
            else:
                return "<p>For this visualization, the selected Y-axis column must be numeric.</p>"

        case "pie":
            if method=="count" or is_numeric_dtype(df[cols_1[0]]):
                data = df.groupby(cols_2[0])[cols_1[0]].agg(method)
                ax.pie(data,labels=data.index,autopct="%1.1f%%",startangle=90)
            else:
                return "<p>For this combination of visualization and aggregation method, the selected Y-axis column must be numeric.</p>"

    # Figure in PNG umwandeln
    image = io.BytesIO()
    fig.savefig(image, format="png", bbox_inches="tight")
    image.seek(0)

    # PNG in Base64 umwandeln
    graph_base64 = base64.b64encode(image.getvalue()).decode("utf-8")

    plt.close(fig)

    return f'<img src="data:image/png;base64,{graph_base64}">'


def display_head(df=None):
    if df is None:
        return "<p>Kein Dataset ausgewählt.</p>"
    else:
        table = df.head(15).to_html(classes='dataframe table table-striped table-bordered',index=False)
        return f'<div class="table_container">{table}</div>'