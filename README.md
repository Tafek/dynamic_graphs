# Dataset Visualizer

A small web-based tool for exploring and visualizing datasets.

The **Dataset Visualizer** allows users to load a CSV dataset, inspect its contents, filter the data, and create different types of visualizations without having to write plotting code themselves.

The project was created as a learning project to practice working with **Python, Pandas, Flask, and Matplotlib** while building something that can be used to explore real datasets.

## Features

### Dataset Overview

* Load CSV datasets
* Display the first 15 rows of the dataset in a table
* Inspect columns and their detected data types
* Automatically detect different types of data, including:
  * Numeric values
  * Categories (Everything up to 6 unique string values is considered a category here)
  * Boolean values
  * Dates
  * Strings

### Data Filtering

The dataset can be filtered while creating a visualization.

Available filters include:

* **Numeric filters**

  * Minimum and maximum values
  * Range sliders
  * Numeric input fields

* **Categorical filters**

  * Select individual categories using checkboxes

* **Boolean filters**

  * Filter `True` / `False` values

* **Date filters**

  * Filter data based on date ranges

* **String filters**

  * Filter text values using RegEx

Filters are applied to the dataset everytime a change is being made.

### Visualizations

The project currently supports several visualization types:

* Line plots
* Scatter plots
* Bar charts
* Pie charts
* Box plots
* Histograms

Depending on the selected visualization, additional settings can be configured.

### Visualization Settings

The visualization settings allow users to customize their graphs without directly interacting with Matplotlib code.

Depending on the graph type, available options can include:

* Columns used for the visualization
* Graph style
* Labels
* Titles
* X-Axis and Y-Axis limits and ticks
* Other visualization-specific settings

When switching to a different visualization type, incompatible settings are reset to prevent invalid configurations.

## Technologies

The project is built with:

* **Python**
* **Flask** – Web application framework
* **Pandas** – Dataset handling and data manipulation
* **Matplotlib** – Data visualization
* **HTML / CSS** – User interface

The project uses a virtual environment for managing its Python dependencies.



## Installation

This project uses [uv](https://docs.astral.sh/uv/) for Python project and dependency management.

### 1. Clone the repository

```bash
git clone <repository-url>
cd dynamic_graphs
```

### 2. Install the dependencies

Make sure `uv` is installed, then run:

```bash
uv sync
```

This creates the virtual environment and installs the dependencies defined in `pyproject.toml`.

### 3. Start the application

Run the Flask application with:

```bash
uv run python main.py
```

The application will then be available at the local address shown by Flask, usually:

```
http://127.0.0.1:5000
```

Open the address in a web browser to use the Dataset Visualizer.

### Running the project again

Once the project has been set up, you can start it at any time with:

```bash
uv run python main.py
```

There is no need to manually activate the virtual environment when using `uv run`.


## Using the Visualizer

A typical workflow looks like this:

1. Add .csv-File(s) to the data folder
2. Select a dataset.
3. Select a visualization type.
4. Inspect and select the available and desired columns.
5. Apply filters if necessary.
6. Adjust the visualization settings.
7. Inspect the resulting graph.

The goal is to make basic data exploration possible without requiring the user to manually write Pandas or Matplotlib code.


## Current Status

This project is still under development.

The main functionality for loading, filtering, and visualizing datasets is implemented, but additional features and improvements may be added over time.

Possible future improvements include:

* More visualization types
* More customization options
* Improved error handling
* Better dataset management
* Additional filtering options
* Exporting generated visualizations
* Improved UI and usability
* Improved performance on huge datasets
* Option to handle Database Tables
