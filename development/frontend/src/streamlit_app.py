import os
import ast
import json
import requests
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from io import StringIO

load_dotenv()
placeholder = st.empty()
container = st.container()

MINIMUM_OF_AGE = int(os.getenv('MINIMUM_OF_AGE', default=14))
MAXIMUM_OF_AGE = int(os.getenv('MAXIMUM_OF_AGE', default=90))
MINIMUM_AGE_OF_WORK_STARTED = int(os.getenv('MINIMUM_AGE_OF_WORK_STARTED', default=14))
MAXIMUM_OF_EMPLOYEMENT_YEARS = os.getenv('MAXIMUM_OF_EMPLOYEMENT_YEARS', default=(MAXIMUM_OF_AGE - MINIMUM_AGE_OF_WORK_STARTED))

if "credit_data_file" not in st.session_state:
    st.session_state.credit_data_file = None
if "credit_data_dict" not in st.session_state:
    st.session_state.credit_data_dict = {}
if "step" not in st.session_state:
    st.session_state.step = "input_start"
if "got_file" not in st.session_state:
    st.session_state.got_file = False
if "answer_text" not in st.session_state:
    st.session_state.answer_text = ""
if "answer_dict" not in st.session_state:
    st.session_state.answer_dict = {}

def update_step(step:str):
    st.session_state.step = step

def loan_data_filling_page():
    home_ownerships = ['RENT','MORTGAGE','OWN','OTHER']
    loan_intents = ['EDUCATION','MEDICAL','VENTURE','PERSONAL','DEBTCONSOLIDATION','HOMEIMPROVEMENT']
    loan_grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

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

if st.session_state.step == "input_start":
    st.session_state.credit_data_file = st.file_uploader(label="Pick a file with credit data", type=["csv", "json"])
    if st.session_state.credit_data_file is not None:
        st.session_state.got_file = True
        if st.session_state.credit_data_file.type == 'text/csv':
            st.session_state.credit_data_file_df = pd.read_csv(st.session_state.credit_data_file, sep=',') # Can be used wherever a "file-like" object is accepted
            st.write(st.session_state.credit_data_file_df)
        elif st.session_state.credit_data_file.type == 'text/json' or st.session_state.credit_data_file.type == 'application/json': 
            st.session_state.credit_data_file_df = pd.read_json(st.session_state.credit_data_file)
            st.write(st.session_state.credit_data_file_df)

    else:
        loan_data_filling_page()

def predict_page_input(data) -> bool:
    r = requests.post(
        'http://credit_scoring_api:8000/predict_one',
        json=data
    )
    if r.status_code == 200:
        st.session_state.answer_dict = ast.literal_eval(r.text)
        return True
    else:
        st.write(f"Error {r.status_code}:\n{r.reason}. Message:\n{r.content}")
        return False

def predict_file_input(credit_file: pd.DataFrame) -> bool:
    #bytes_data = credit_file.getvalue() # To read file as bytes
    #stringio = StringIO(st.session_state.credit_data_file.getvalue().decode("utf-8")) # To convert to a string based IO
    #st.session_state.credit_data_file_string = stringio.read() # To read file as string
    url = "http://credit_scoring_api:8000/predict_file"
    csv_buffer = StringIO()
    credit_file.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0) # Перематываем буфер в начало (важно для чтения)
    bytes_data = csv_buffer
    files = {"file": (os.path.splitext(st.session_state.credit_data_file.name)[0]+'.csv', bytes_data, "text/csv")}

    r = requests.post(url,files=files)
    if r.status_code == 200:
        st.session_state.answer_text = r.text.encode('utf8')
        return True
    else:
        st.write(f"Error {r.status_code}:\n{r.reason}. Message:\n{r.content}")
        return False

if st.session_state.step == "input_start" or st.session_state.step == "input_set":
    if st.button("Predict default!"):
        update_step("predict")
        st.rerun()

if st.session_state.step == "output":
    if st.session_state.got_file:
        if st.session_state.answer_text != '':
            answer_df = pd.read_csv(st.session_state.answer_text, sep=',')
            st.write(answer_df)
            st.download_button(
                label="Download CSV with predictions",
                data=st.session_state.answer_text,
                file_name="answer.csv",
                mime="text/csv",
                icon=":material/download:",
            )
    else:
        probability = round(st.session_state.answer_dict['default_probability']*100,2)
        will_be_default = (st.session_state.answer_dict['expected_default'] == 1)
        decision_threshold = 50 #%
        if abs(probability - decision_threshold) < 20:
            st.write(f"Unsure result. Human supervision is required!")
        st.write(f"Default probability: {probability}%")
        st.write(f"Will loan be a default: {'Yes' if will_be_default else 'No'}")
    update_step("output_is_showed")

def show_restart_button():
    if st.button("Restart"):
        update_step("input_start")
        st.session_state.credit_data_file = None
        st.session_state.got_file = False
        st.rerun()

if st.session_state.step == "output_is_showed":
    show_restart_button()

if st.session_state.step == "predict":
    ok_result = False
    if st.session_state.got_file:
        ok_result = predict_file_input(st.session_state.credit_data_file_df)
    else:
        ok_result = predict_page_input(st.session_state.credit_data_dict)
    if ok_result:
        update_step("output")
        st.rerun()
    else:
        update_step("output_is_showed")
        show_restart_button()

