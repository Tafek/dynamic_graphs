#https://matplotlib.org/stable/plot_types/index.html

import base64
import io

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def show_graph(type="line", cols_1=None, cols_2=None, filters=None, settings=None, df=None, method="mean"):

    if df is None:
        return "<p>Kein Dataset ausgewählt.</p>"

    if cols_1 is None or len(cols_1) == 0:
        return "<p>Keine Spalten für die Y-Achse ausgewählt.</p>"

    if type in ["line", "scatter", "bar", "pie"] and (len(cols_2) == 0 or len(cols_1) == 0):
        return "<p>Diese Visualisierung benötigt zwei Spalten.</p>"

    fig, ax = plt.subplots()

    match type:

        case "line":
            df.groupby(cols_2[0])[cols_1[0]].agg(method).plot.line(ax=ax)

        case "scatter":
            #df.groupby(cols_2[0])[cols_1[0]].agg(method).plot.scatter(x=cols_2[0], y=cols_1[0], ax=ax)
            ax.scatter(df[cols_2[0]], df[cols_1[0]])

        case "bar":
            df.groupby(cols_2[0])[cols_1[0]].agg(method).plot.bar(ax=ax)

        case "hist":
            #ax.hist(df[cols_1[0]])
            df[cols_1[0]].plot.hist(ax=ax)

        case "boxplot":
            #ax.boxplot(df[cols_1[0]])
            df.boxplot(column=cols_1[0], by=cols_2[0], ax=ax)

        case "pie":
            #ax.pie(df[cols_1[0]])
            #df.groupby(cols_2[0])[cols_1[0]].agg(method).plot.pie(y=cols_1[0], ax=ax)
            #ax.pie(df[cols_1[0]], labels=df[cols_2[0]], autopct='%1.1f%%', startangle=90)
            data = df.groupby(cols_2[0])[cols_1[0]].agg(method)
            ax.pie(data,labels=data.index,autopct="%1.1f%%",startangle=90)

    # Figure in PNG umwandeln
    image = io.BytesIO()
    fig.savefig(image, format="png", bbox_inches="tight")
    image.seek(0)

    # PNG in Base64 umwandeln
    graph_base64 = base64.b64encode(image.getvalue()).decode("utf-8")

    plt.close(fig)

    return f'<img src="data:image/png;base64,{graph_base64}">'