import json
import requests
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

credit_file = st.file_uploader("Pick a file with credit data")

home_ownerships = ['RENT','MORTGAGE','OWN','OTHER']
loan_intents = ['EDUCATION','MEDICAL','VENTURE','PERSONAL','DEBTCONSOLIDATION','HOMEIMPROVEMENT']
loan_grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

MINIMUM_OF_AGE = int(os.getenv('MINIMUM_OF_AGE', default=14))
MAXIMUM_OF_AGE = int(os.getenv('MAXIMUM_OF_AGE', default=90))
MINIMUM_AGE_OF_WORK_STARTED = int(os.getenv('MINIMUM_AGE_OF_WORK_STARTED', default=14))
MAXIMUM_OF_EMPLOYEMENT_YEARS = os.getenv('MAXIMUM_OF_EMPLOYEMENT_YEARS', default=(MAXIMUM_OF_AGE - MINIMUM_AGE_OF_WORK_STARTED))

person_age = st.slider(label="Person's age", min_value=MINIMUM_OF_AGE, max_value=MAXIMUM_OF_AGE, step=1)
person_emp_length = st.slider(label="Person's employment length in years", min_value=0, max_value=MAXIMUM_OF_EMPLOYEMENT_YEARS, step=1)
person_home_ownership = st.radio("Person's home ownership type", home_ownerships)
person_income = st.number_input(label="Person's income", min_value=0, max_value=pow(10,8), step=1)
cb_person_default_on_file = st.checkbox("Did person ever have a default?")
cb_person_cred_hist_length = st.slider(label="Person's credit history length", min_value=0, max_value=100, step=1)
loan_amnt = st.number_input(label="Loan amount", min_value=1, max_value=pow(10,8), step=1)
loan_intent = st.radio("Person's home ownership type", loan_intents)
loan_int_rate = st.slider(label="Loan interest rate", min_value=0, max_value=100, step=1)
loan_grade = st.radio("Loan grade", loan_grades)
loan_percent_income = st.slider(label="Loan percent income", min_value=0.00, max_value=1.00, step=0.01)

credit_data_dict = {
    "person_age": person_age, 
    "person_income": person_income,
    "person_home_ownership": person_home_ownership,
    "person_emp_length": person_emp_length,
    "loan_intent": loan_intent,
    "loan_grade": loan_grade,
    "loan_amnt": loan_amnt,
    "loan_int_rate": loan_int_rate,
    "loan_percent_income": loan_percent_income,
    "cb_person_default_on_file": cb_person_default_on_file,
    "cb_person_cred_hist_length": cb_person_cred_hist_length
}
credit_data = json.dumps(credit_data_dict)

if st.button("Predict default!"):
    headers = {
        'Content-Type': 'application/json'
    }
    if credit_file is None:
        data = credit_data
    else:
        data = credit_file

    r = requests.post('http://credit_scoring_frontend:8000/predict', headers=headers, json=data)
    if r.status_code == 200:
        st.write("Success")