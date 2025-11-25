# Create the Streamlit app to dashboard 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initial Page Configurations
st.set_page_config(
    page_title="Interactive Dashboard", 
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Data
st.write("### To Get Started Upload Your Data Below")         

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Create 2 Cols 
    col1, col2 = st.columns([1, 1])   
    
    ### Column 1
    with col1:
        st.write("### Preview of Data")         
        st.dataframe(df.head(10))


    ### Column 2    
    with col2:
        selector, selector2 = st.columns([1,1])
        with selector:    
            selected_col = st.selectbox("Select a column to plot", df.columns)
        with selector2:    
            count_n = st.select_slider("Count of Categories to Display", options=[x for x in range(0,50,5)])
        if selected_col:
            if count_n == 0: 
                count_n = 1
            # Detect numeric vs categorical
            if pd.api.types.is_numeric_dtype(df[selected_col]):
                fig, ax = plt.subplots(figsize=(15,6))
                histData = df[selected_col].dropna().sort_values(ascending=False)
                ax.hist(histData, color='skyblue')
                ax.tick_params(axis='x', labelrotation=30) 
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')
            else:
                fig, ax = plt.subplots(figsize=(15,6))
                df[selected_col].value_counts(ascending=False)[:count_n].plot(
                    kind="bar", ax=ax, color='skyblue'
                )
                ax.tick_params(axis='x', labelrotation=30) 
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Count")
                ax.set_title(f"Frequency of {selected_col} Feature")
                st.pyplot(fig, width='content')

else:
    st.info("Please upload a CSV file to begin.")



### Next Section 
    
st.write("### Interaction Between Columns")   
cola, colb = st.columns([1,1])
with cola:    
    cola = st.selectbox("Column A", df.columns)
with colb:    
    colb = st.selectbox("Column B", df.columns)    
