import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Machine Downtime dashboard",layout="wide")
st.title("Machine Downtime % Analytics - By Ahmer Nadeem")
upload_file=st.file_uupload("Upload Machinne Log CSV file", type="csv")
if uploaded_file:

    df= pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(df.head())
    stop_time=df[df['Status']=='Stop']['Duration'].sum()
    total_time=df['Duration'].sum()
    downtime_perc=(stop_time/total_time)*100
    col1,col2=st.columns(2)
    col1.metric("Total Downtime %", f"{downtime_perc:.2f}%")
    col2.metric("Total stop hours",f"{stop_time:.1f} hrs")
    fig=px.pie(df, names='Status', values='Duration', title='Run time vs stop time')
    st.plotly_chart(fig, use_container_width=True)
 else:
     st.info("Please upload a csv with columns: Machine, Status, Duration")  
