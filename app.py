# Create the Streamlit app to dashboard 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initial Page Configurations
st.set_page_config(
    page_title="Interactive Dashboard", 
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://example.com/help",
        "Report a bug": "https://example.com/bug",
        "About": "This is an interactive dashboard."
    }
)

# Load Data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Create 2 Cols 
    col1, col2 = st.columns([1, 1])   
    
    ### Column 1
    with col1:
        label, selector, selector2 = st.columns([1,1,1])
        with label:
            st.write("### Preview of Data") 
        with selector:    
            selected_col = st.selectbox("Select a column to plot", df.columns)
        with selector2:    
            count_n = st.selectbox("Count of Categories to Disply", [x for x in range(1,20)])
        st.dataframe(df.head(10))


    ### Column 2    
    with col2:
        if selected_col:
            st.write(f"### Distribution of (Top {count_n} Values): {selected_col}")

            # Detect numeric vs categorical
            if pd.api.types.is_numeric_dtype(df[selected_col]):
                fig, ax = plt.subplots(figsize=(15,6))
                ax.hist(df[selected_col].dropna().sort_values(ascending=False),
                        color='skyblue')
                plt.xticks(rotation=90)
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')
            else:
                fig, ax = plt.subplots(figsize=(15,6))
                df[selected_col].value_counts(ascending=False)[:count_n].plot(
                    kind="bar", ax=ax, color='skyblue'
                )
                plt.xticks(rotation=90)
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Count")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')

else:
    st.info("Please upload a CSV file to begin.")