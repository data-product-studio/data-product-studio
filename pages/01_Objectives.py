import streamlit as st
import pandas as pd
from datetime import datetime
import math
st.title("Objectives")



status = st.selectbox("\n\nObjective:", ["Calculate Employee Tenure"])


# open Existing Objectives file and display
df = pd.read_csv("data/objectives.csv")
sldf = st.table(df)

# form to collect new data
with st.form("objectives_form",clear_on_submit = True ):
    # slider_val = st.slider("Form slider")
    key_res = st.text_input(label='Enter Key Result')
    status = st.selectbox('Select Status', ['Not Yet Started', 'Started', "Complete"])
    created_date = st.date_input('Enter Created Date', datetime.today().date())
    # button to submit
    submitted = st.form_submit_button("Add Key Result")
    # on button submit
    if submitted:
        if not key_res:
            st.error("Key Result may not be empty.")
        elif created_date > datetime.today().date():
            st.error("Created date must not be in the future")
        else:
            # caclulate next ID
            id = 1 if math.isnan(df["ID"].max()) else df["ID"].max()+1
            new_data = {'Key Results':key_res, "Status":status, "Created":created_date, "ID": id}
            # append new data to df
            df = df.append(new_data, ignore_index = True)

            df.to_csv("data/objectives.csv", index=False)
            # reruns the script to result form and update table
            st.experimental_rerun()
