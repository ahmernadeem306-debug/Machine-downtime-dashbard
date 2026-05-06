import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Machine Downtime dashboard",layout="wide")
st.title("Machine Downtime % Analytics - By Ahmer Nadeem")
upload_file=st.file_uploader("Upload Machine Log CSV file", type="csv")
if upload_file:

    df= pd.read_csv(upload_file)
    st.subheader("Raw Data")
    st.dataframe(df.head())
    stop_time=df[df['Status']=='Stop']['Duration'].sum()
    total_time=df['Duration'].sum()
    run_time=df[df['Status']=='Run']['Duration'].sum()
    downtime_perc=(stop_time/total_time)*100 if total_time>0 else 0
    col1,col2,col3=st.columns(3)
    col1.metric("Total Downtime %", f"{downtime_perc:.2f}%")
    col2.metric("Total stop hours",f"{stop_time:.1f} hrs")
    col3.metric("Total Production Hours", f"{run_time:.1f} hrs")
    fig=px.pie(df, names='Status', values='Duration', title='Run time vs stop time')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Machine Wise production summary")
    summary=df.groupby(['Machine','Status'])['Duration'].sum().unstack().fillna(0)
    summary['Total Hours']=summary.sum(axis=1)
    summary['Downtime %']=(summary.get('Stop',0)/summary['Total Hours'])*100
    summary=summary.round(2)
    st.dataframe(summary)
    st.subheader(f"Graph: { worst_machine}-highest problem")
    worst_df=df[df['Machine']==worst_machine]
    fig_worst=px.pie(worst_df,names='Status',values='Duration',
                     title=f'{worst_machine} Run vs Stop Breakdown',
                     color='Status',color_discrete_map={'Run':'green','Stop':'red'})
    st.plotly_chart(fig_worst,use_container_width=True)
    st.header("All Machines Downtime Comparison")
    fig_bar=px.bar(summary.reset_index(),x='Machine',y='Downtime %',
                   title='Machine Wise Downtime %',
                   color='Downtime %', color_continuous_scale='Reds',
                   text='Downtime %')
    fig_bar.update_traces(texttemplate='%{text:.1f}%',textposition='outside')
    st.plotly_chart(fig_bar,use_container_width=True)

else:
      st.info("Please upload a csv with columns: Machine, Status, Duration")  
