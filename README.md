# autoDs

Automated data science dashboard: upload any CSV and get an instant exploratory dashboard, with no code to write.

Built with Streamlit, pandas and matplotlib.

## What it shows

- **Data at a glance:** row count, column count and the share of missing values
- **Data preview:** the first 10 rows
- **Features at a glance:** pick any column to see a histogram (numeric) or its most common categories (categorical)
- **Categorical feature interactions:** pick two columns to see a stacked bar chart of how one breaks down by the other, with percentage labels and the long tail grouped into "Other"

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints and upload a CSV.
