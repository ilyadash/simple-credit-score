import os
import ast
import json
import requests
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
placeholder = st.empty()
container = st.container()

if "credit_data_file" not in st.session_state:
    st.session_state.credit_data_file = None
if "credit_data_dict" not in st.session_state:
    st.session_state.credit_data_dict = {}
if "button_pressed" not in st.session_state:
    st.session_state.button_pressed = False

if not st.session_state.button_pressed:
    st.session_state.credit_data_file = st.file_uploader(label="Pick a file with credit data", type=["csv", "json", "txt"])
    with container.container():
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

        st.session_state.credit_data_dict = {
            "person_age": person_age, 
            "person_income": person_income,
            "person_home_ownership": person_home_ownership,
            "person_emp_length": person_emp_length,
            "loan_intent": loan_intent,
            "loan_grade": loan_grade,
            "loan_amnt": loan_amnt,
            "loan_int_rate": loan_int_rate,
            "loan_percent_income": loan_percent_income,
            "cb_person_default_on_file": "Y" if cb_person_default_on_file else "N",
            "cb_person_cred_hist_length": cb_person_cred_hist_length
        }

def predict_page_input(data):
    r = requests.post(
        'http://credit_scoring_api:8000/predict_one',
        json=data
    )
    if r.status_code == 200:
        answer = ast.literal_eval(r.text)
        probability = round(answer['default_probability']*100,2)
        will_be_default = (answer['expected_default'] == 1)
        decision_threshold = 50 #%
        if abs(probability - decision_threshold) < 20:
            st.write(f"Unsure result. Human supervision is required!")
        st.write(f"Default probability: {probability}%")
        st.write(f"Will loan be a default: {'Yes' if will_be_default else 'No'}")
    else:
        st.write(f"Error {r.status_code}:\n{r.reason}. Message:\n{r.content}")

def predict_file_input(credit_file):
    r = requests.post(
        "http://credit_scoring_api:8000/predict_file",
        files={"file": credit_file}
    )
    if r.status_code == 200:
        answer = r.text.encode('utf8')
        st.download_button(
            label="Download CSV with predictions",
            data=answer,
            file_name="answer.csv",
            mime="text/csv",
            icon=":material/download:",
        )
    else:
        st.write(f"Error {r.status_code}:\n{r.reason}. Message:\n{r.content}")

def update_button_state():
    st.session_state.value = "Pressed"

if st.session_state.button_pressed:
    if st.session_state.credit_data_file is None:
        predict_page_input(st.session_state.credit_data_dict)
    else:
        predict_file_input(st.session_state.credit_data_file)

if not st.session_state.button_pressed:
    if st.button("Predict default!", on_click=update_button_state):
        st.session_state.button_pressed = True
        st.rerun()
