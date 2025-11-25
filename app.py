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
    box_contents = [
        ("Total rows:", f"{len(df)}"),
        ("NAs:", f"{df.isna().all().sum()}"),
        ("Count of Columns:", len(df.columns)),
    ]

    # Loop over columns and content to keep uniformity
    for col, (title, value) in zip(cols, box_contents):
        with col:
            box = st.container(border=True, horizontal=True, horizontal_alignment='center')
            box.write(f"### {title}")
            if value:
                box.write(f"### {value}")

    ### SECTION XX: ###
    # Create 2 Cols 
    st.write("## Data Preview")   
    selector, selector2 = st.columns([1,1])
    with selector:    
        selected_col = st.selectbox("Select a column to plot", df.columns)
    with selector2:    
        count_n = st.select_slider("Count of Categories to Display", options=[x for x in range(0,50,5)])
      

    col1, col2 = st.columns([1, 1]) 
    # Col 1
    with col1:
        st.dataframe(df.head(10))

    ### Column 2    
    with col2:
        if selected_col:
            if count_n == 0: 
                count_n = 1
            # Detect numeric vs categorical
            if pd.api.types.is_numeric_dtype(df[selected_col]):
                fig, ax = plt.subplots(figsize=(12,4.5))
                histData = df[selected_col].dropna().sort_values(ascending=False)
                ax.hist(histData, color='skyblue')
                ax.tick_params(axis='x', labelrotation=30) 
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')
            else:
                fig, ax = plt.subplots(figsize=(12,4.5))
                df[selected_col].value_counts(ascending=False, normalize=True)[:count_n].plot(
                    kind="bar", ax=ax, color='skyblue'
                )
                ax.tick_params(axis='x', labelrotation=30) 
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Percent")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')

    ### Next Section    
    st.write("## Feature Interactions")   
    cola, colb = st.columns([1,1])
    with cola:    
        cola = st.selectbox("Column A", df.columns)
    with colb:    
        colb = st.selectbox("Column B", df.columns)    

    # Assuming cola and colb are selected columns
    if pd.api.types.is_numeric_dtype(df[cola]) and pd.api.types.is_numeric_dtype(df[colb]):
        # Both numeric -> maybe a 2D histogram or scatter, but here we'll do a binned bar plot
        fig, ax = plt.subplots(figsize=(12,4.5))
        bins = 10  # you can adjust
        hist2d, xedges, yedges = np.histogram2d(df[cola].dropna(), df[colb].dropna(), bins=bins)
        im = ax.imshow(hist2d.T, origin='lower', cmap='Blues', aspect='auto')
        ax.set_xticks(range(bins))
        ax.set_xticklabels([f"{xedges[i]:.1f}-{xedges[i+1]:.1f}" for i in range(bins)], rotation=30)
        ax.set_yticks(range(bins))
        ax.set_yticklabels([f"{yedges[i]:.1f}-{yedges[i+1]:.1f}" for i in range(bins)])
        ax.set_xlabel(cola)
        ax.set_ylabel(colb)
        ax.set_title(f"2D Histogram of {cola} vs {colb}")
        fig.colorbar(im, ax=ax, label='Frequency')
        st.pyplot(fig, width='content')

    else:
        # Treat both as categorical (or convert numeric to categorical bins)
        # Create cross-tabulation
        cross_tab = pd.crosstab(
            df[cola].astype(str),
            df[colb].astype(str),
            normalize='index'  
        )

        fig, ax = plt.subplots(figsize=(12,4.5))
        cross_tab.plot(kind='bar', stacked=True, ax=ax, colormap='Blues')
        ax.tick_params(axis='x', labelrotation=30)
        ax.set_xlabel(cola)
        ax.set_ylabel("Percent")
        ax.set_title(f"Interaction between {cola} and {colb}")
        ax.legend(title=colb, bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig, width='content')
    










else:
    st.info("Please upload a CSV file to begin.")