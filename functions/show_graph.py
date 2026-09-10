#https://matplotlib.org/stable/plot_types/index.html

import base64
import io

import matplotlib
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype

matplotlib.use("Agg")


def setting_to_float(settings, key):
    value = settings.get(key)

    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def setting_to_int(settings, key):
    value = settings.get(key)

    if value in (None, ""):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def show_graph(type="line", cols_1=None, cols_2=None, filters=None,
               settings=None, df=None, method="count"):

    if df is None:
        return "<p>Kein Dataset ausgewählt.</p>"

    if cols_1 is None or len(cols_1) == 0:
        return "<p>Keine Spalten für die Y-Achse ausgewählt.</p>"

    if type in ["line", "scatter", "bar", "pie"] and (len(cols_2) == 0 or len(cols_1) == 0):
        return "<p>Diese Visualisierung benötigt zwei Spalten.</p>"

    if settings is None:
        settings = {}
    if settings.get("styling_graph_style"):
        plt.style.use(settings["styling_graph_style"])

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
            bins = settings.get("styling_bins", 10)

            try:
                bins = max(1, int(bins))
            except (TypeError, ValueError):
                bins = 10

            df[cols_1].plot.hist(ax=ax, bins=bins)

        case "boxplot":
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

    # Allgemeine Diagramm-Einstellungen
    x_min = setting_to_float(settings, "styling_x_min")
    x_max = setting_to_float(settings, "styling_x_max")
    y_min = setting_to_float(settings, "styling_y_min")
    y_max = setting_to_float(settings, "styling_y_max")

    if x_min is not None or x_max is not None:
        ax.set_xlim(left=x_min, right=x_max)

    if y_min is not None or y_max is not None:
        ax.set_ylim(bottom=y_min, top=y_max)

    if settings.get("styling_title"):
        ax.set_title(settings["styling_title"])

    if settings.get("styling_x_label"):
        ax.set_xlabel(settings["styling_x_label"])

    if settings.get("styling_y_label"):
        ax.set_ylabel(settings["styling_y_label"])

    x_ticks = setting_to_int(settings, "styling_x_ticks")
    y_ticks = setting_to_int(settings, "styling_y_ticks")
    x_tick_rotation = setting_to_int(settings, "styling_x_tick_rotation")

    if x_ticks is not None:
        ax.locator_params(axis="x", nbins=x_ticks)

    if y_ticks is not None:
        ax.locator_params(axis="y", nbins=y_ticks)

    if x_tick_rotation is not None:
        ax.tick_params(axis="x", labelrotation=x_tick_rotation)

    ax.grid(settings.get("styling_grid", False))

    if settings.get("styling_legend", True):
        ax.legend()
    else:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()

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


def show_graph_settings(type, cols_1, cols_2, df,
                        visual_type_switched, settings):

    graph_setting_html = '<div class="graph_container_right">'
    graph_setting_html += "Select further settings for your visualization.<br><br>"

    if visual_type_switched:
        settings = {}

    selected_style = settings.get("styling_graph_style", "default")

    graph_setting_html += "Style:"
    graph_setting_html += "<select name='styling_graph_style' id='styling_graph_style_select' onchange='this.form.submit()'>"

    for style in ["default", *plt.style.available]:
        selected = " selected" if style == selected_style else ""
        graph_setting_html += (
            f"<option value='{style}'{selected}>{style}</option>"
        )

    graph_setting_html += "</select><br><br>"

    settings_title = settings.get("styling_title", "")
    x_label = settings.get("styling_x_label", "")
    y_label = settings.get("styling_y_label", "")
    x_min = settings.get("styling_x_min", "")
    x_max = settings.get("styling_x_max", "")
    y_min = settings.get("styling_y_min", "")
    y_max = settings.get("styling_y_max", "")
    bins = settings.get("styling_bins", "")
    x_ticks = settings.get("styling_x_ticks", "")
    y_ticks = settings.get("styling_y_ticks", "")
    x_tick_rotation = settings.get("styling_x_tick_rotation", 0)
    styling_show_grid = settings.get("styling_grid", False)
    styling_show_legend = settings.get("styling_legend", True)

    if styling_show_grid:
        grid_checked = "checked"
    else:
        grid_checked = ""

    if styling_show_legend:
        legend_checked = "checked"
    else:
        legend_checked = ""

    graph_setting_html += f"""
        <div class="graph_settings_form">
            <label for="styling_title">Title:</label>
            <input type="text" id="styling_title" name="styling_title" class="settings_text" value="{settings_title}" onchange="this.form.submit()">

            <label for="styling_x_label">X-axis label:</label>
            <input type="text" id="styling_x_label" name="styling_x_label" class="settings_text" value="{x_label}" onchange="this.form.submit()">

            <label for="styling_y_label">Y-axis label:</label>
            <input type="text" id="styling_y_label" name="styling_y_label" class="settings_text" value="{y_label}" onchange="this.form.submit()">

            <div class="axis_range_row">
                <label for="styling_y_min">Y minimum:</label>
                <input type="number" step="any" id="styling_y_min" class="settings_number" name="styling_y_min" value="{y_min}" onchange="this.form.submit()">

                <label for="styling_y_max">Y maximum:</label>
                <input type="number" step="any" id="styling_y_max" class="settings_number" name="styling_y_max" value="{y_max}" onchange="this.form.submit()">
            </div>

            <div class="axis_range_row">
                <label for="styling_x_min">X minimum:</label>
                <input type="number" step="any" id="styling_x_min" class="settings_number" name="styling_x_min" value="{x_min}" onchange="this.form.submit()">

                <label for="styling_x_max">X maximum:</label>
                <input type="number" step="any" id="styling_x_max" class="settings_number" name="styling_x_max" value="{x_max}" onchange="this.form.submit()">
            </div>"""

    if type == "hist":
        graph_setting_html += f"""
            <label for="styling_bins">Histogram bins:</label>
            <input type="number" min="1" step="1" id="styling_bins" class="settings_number" name="styling_bins" value="{bins}" onchange="this.form.submit()">
            """
        
    graph_setting_html += f"""        
            <label for="styling_y_ticks">Amount of Y-Ticks:</label>
            <input type="number" min="1" step="1" id="styling_y_ticks" class="settings_number" name="styling_y_ticks" value="{y_ticks}" onchange="this.form.submit()">

            <label for="styling_x_ticks">Amount of X-Ticks:</label>
            <input type="number" min="1" step="1" id="styling_x_ticks" class="settings_number" name="styling_x_ticks" value="{x_ticks}" onchange="this.form.submit()">

            <label for="styling_x_tick_rotation">X-Tick-Rotation:</label>
            <input type="number" min="0" max="90" step="1" id="styling_x_tick_rotation" class="settings_number" name="styling_x_tick_rotation" value="{x_tick_rotation}" onchange="this.form.submit()">

            <div class="checkbox_row">
                <input type="checkbox" id="styling_grid" name="styling_grid" {grid_checked} onchange="this.form.submit()">
                <label for="styling_grid">Show grid</label>
            </div>

            <div class="checkbox_row">
                <input type="checkbox" id="styling_legend" name="styling_legend" {legend_checked} onchange="this.form.submit()">
                <label for="styling_legend">Show legend</label>
            </div>
        </div>
    """

    graph_setting_html += "</div>"
    return graph_setting_html