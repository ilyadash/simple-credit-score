import json
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

credit_file = st.file_uploader("Pick a file with credit data")

person_age = st.slider("Pick a number", 0, 100)
st.radio("Pick a pet", pets)


credit_data_dict = {"person_age": 22, "person_income": 59000,"person_home_ownership": "RENT","person_emp_length": 30.0,"loan_intent": "PERSONAL","loan_grade": "D","loan_amnt": 35000,"loan_int_rate": 16.02,"loan_percent_income": 0.59,"cb_person_default_on_file": "Y","cb_person_cred_hist_length": 3}
credit_data = json.dumps(credit_data_dict)

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
