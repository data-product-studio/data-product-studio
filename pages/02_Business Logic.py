import streamlit as st
import pandas as pd
st.title("Business Logic")
"### This page is in progress."

df = pd.read_csv("data/businesslogic.csv")
# radio buttons to choose logic type
lan_choice = st.radio( "Choose Format:", ('Written Logic', 'Pseudo Code'))

if lan_choice == "Written Logic":
    st.table(df[["Step", "Written Logic", "TaxonomyLink"]])
elif lan_choice == "Pseudo Code":
    st.table(df[["Step", "Pseudo Code", "TaxonomyLink"]])
