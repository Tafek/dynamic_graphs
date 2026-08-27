def display_head(df=None):
    if df is None:
        return "<p>Kein Dataset ausgewählt.</p>"
    else:
        return df.head(15).to_html(classes='dataframe table table-striped table-bordered', index=False)  