import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder

class MyDataPreprocessor(TransformerMixin):
    def __init__(self, max_age:int, max_years_of_employment:int, min_age_of_employment:int):
        """
        :param columns_to_remove: if not None select remove these columns from the dataframe
        """
        self.continuous_columns = ['person_income', 'person_emp_length', 'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'cred_hist_to_age']
        self.categorial_columns = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        self.scaler = RobustScaler() # StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.maximum_age = max_age
        self.max_years_of_employment = max_years_of_employment
        self.min_age_of_employment = min_age_of_employment
        self.person_emp_length_median = 0
        self.person_age_median = 1
        self.loan_int_rate_mean = 0

    def preprocess_train_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop_duplicates()
        data['person_emp_length'] = data['person_emp_length'].fillna(self.person_emp_length_median)
        data['loan_int_rate'] = data['loan_int_rate'].fillna(self.loan_int_rate_mean)
        if 'person_age' in data.columns:
            data = data[data['person_age'] <= self.maximum_age] 
        if 'person_emp_length' in data.columns:
            data = data[data['person_emp_length'] <= self.max_years_of_employment]
        if ('person_age' in data.columns) and ('person_emp_length' in data.columns):
            data = data[data['person_age'] > (data['person_emp_length'] + self.min_age_of_employment)]
        data["cred_hist_to_age"] = data['cb_person_cred_hist_length']/data['person_age']
        data = data.drop('cb_person_cred_hist_length', axis=1)
        data = data.drop('person_age', axis=1)
        data = data.reindex(sorted(data.columns), axis='columns')
        return data
    
    def preprocess_test_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop_duplicates()
        data['person_emp_length'] = data['person_emp_length'].fillna(self.person_emp_length_median)
        data['loan_int_rate'] = data['loan_int_rate'].fillna(self.loan_int_rate_mean)
        data['person_age'].fillna(self.person_age_median)
        data["cred_hist_to_age"] = data['cb_person_cred_hist_length']/data['person_age']
        data = data.drop('cb_person_cred_hist_length', axis=1)
        data = data.drop('person_age', axis=1)
        data = data.reindex(sorted(data.columns), axis='columns')
        return data

    def fit(self, data: pd.DataFrame, *args):
        """
        Prepares the class for future transformations
        :param data: pd.DataFrame with all available columns
        :return: self
        """
        data = data.drop_duplicates()
        self.person_age_median = int(data['person_age'].median(skipna=True))
        self.person_emp_length_median = int(data['person_emp_length'].median(skipna=True))
        self.loan_int_rate_mean = data['loan_int_rate'].mean(skipna=True)
        data = self.preprocess_train_data(data)
        self.con_data = (data[self.continuous_columns]).to_numpy()
        self.scaler = self.scaler.fit(self.con_data)
        self.cat_data = (data[self.categorial_columns]).to_numpy()
        self.encoder = self.encoder.fit(self.cat_data)
        return self

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        """
        Transforms features so that they can be fed into the regressors
        :param data: pd.DataFrame with all available columns
        :return: np.array with preprocessed features
        """
        data = self.preprocess_test_data(data)
        continuous_features = data[self.continuous_columns].to_numpy()
        continuous_processed_features = np.array(self.scaler.transform(continuous_features))
        categorial_features = data[self.categorial_columns].to_numpy()
        categorial_processed_features = self.encoder.transform(categorial_features).toarray()
        processed_features = np.concatenate((continuous_processed_features, categorial_processed_features), axis=1)

        return processed_features