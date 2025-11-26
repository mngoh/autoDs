# Create the Streamlit app to dashboard 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initial Page Configurations
st.set_page_config(
    page_title="Interactive Dashboard", 
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Plot Sizes
figSize = (18,8)

### SECTION 1: ###
# Load Data
st.write("# To Get Started Upload Your Data Below")         

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
      
    
    # Title 
    st.write('## Data at a Glace')
    
    # Create a single row with 5 evenly sized columns
    cols = st.columns(3)

    # Define the content for each box
    # Define the content for each box
    box_contents = [
        ("Total rows", f"{len(df)}"),
        ("Percent NAs", f"{df.isna().sum().sum() / df.size:.2%}"),
        ("Count of Columns", f"{len(df.columns)}")
    ]

    # Loop over columns to display metrics
    for col, (title, value) in zip(cols, box_contents):
        with col:
            st.metric(label=title, value=value)

    ##### NEXT SECTION ####### 
    # Create 2 Cols 
    st.write("## Data Preview")   
    # Col 1
    st.dataframe(df.head(10))

    ##### NEXT SECTION ####### 
    st.write("## Features at a Glance")   
    selector, selector2 = st.columns([1,1])
    with selector:    
        selected_col = st.selectbox("Select a column to plot", df.columns)
    with selector2:    
        count_n = st.select_slider("Count of Categories to Display", options=[x for x in range(0,50,5)])     
    col1, col2 = st.columns([1, 1]) 
    if selected_col:
        if count_n == 0: 
            count_n = 1
        # Detect numeric vs categorical
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            fig, ax = plt.subplots(figsize=(figSize))
            histData = df[selected_col].dropna().sort_values(ascending=False)
            ax.hist(histData, color='skyblue')
            ax.tick_params(axis='x', labelrotation=30) 
            ax.set_xlabel(selected_col)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Frequency of {selected_col} Feature")
            st.pyplot(fig, width='content')
        else:
            fig, ax = plt.subplots(figsize=(figSize))
            df[selected_col].value_counts(ascending=False, normalize=True)[:count_n].plot(
                kind="bar", ax=ax, color='skyblue'
            )
            ax.tick_params(axis='x', labelrotation=30) 
            ax.set_xlabel(selected_col)
            ax.set_ylabel("Percent")
            ax.set_title(f"Frequency of {selected_col} Feature")
            st.pyplot(fig, width='content')

    ##### NEXT SECTION ####### 
    st.write("## Categorical Feature Interactions")   
    catCols = [col for col in df.columns 
            if df[col].dtype == "object" or pd.api.types.is_categorical_dtype(df[col])]    
    cola, colb = st.columns([1,1])
    with cola:    
        cola = st.selectbox("Column A", catCols)
    with colb:    
        colb = st.selectbox("Column B", catCols)   
    
    # Slider
    slider1, slider2 = st.columns([1,1])
    with slider1:    
        count_n_cat = st.select_slider("Number of A Categories (Bars) to Display", options=list(range(0,10,1)))
    with slider2:    
        N = st.select_slider("Number of B Categories (Colors) to Display", options=list(range(0,50,1)), value=5)

    # 1 if 0
    if count_n_cat == 0 or N == 0:
        count_n_cat=N=1

    a = df[cola].astype(str)
    b = df[colb].astype(str)
    top_categories = b.value_counts().nlargest(N).index
    b_filtered = b.where(b.isin(top_categories), other="Other")

    cross_tab = pd.crosstab(a, b_filtered)
    cross_tab["__total__"] = cross_tab.sum(axis=1)
    cross_tab = cross_tab.sort_values("__total__", ascending=False).head(count_n_cat)
    cross_tab = cross_tab.drop(columns="__total__")

    fig, ax = plt.subplots(figsize=(figSize))
    cross_tab.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    # ---- ADD % LABELS ----
    for i, (index, row) in enumerate(cross_tab.iterrows()):
        total = row.sum()
        cumulative = 0
        for cat in cross_tab.columns:
            value = row[cat]
            if value > 0:
                cumulative += value
                percent = value / total * 100
                if percent > 1:  # avoids labels on very tiny slices
                    ax.text(
                        i,                       # x position
                        cumulative - value/2,    # y position (middle of the segment)
                        f"{percent:.1f}%",       # label text
                        ha="center", va="center",
                        color="white", fontsize=7, fontweight="bold"
                    )

    ax.set_xlabel(cola)
    ax.set_ylabel("Count")
    ax.set_title(f"Stacked Bar Plot of {colb} (Top {N} Categories + 'Other') grouped by {cola}")
    ax.legend(title=colb)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig, width="content")

else:
    st.info("Please upload a CSV file to begin.")