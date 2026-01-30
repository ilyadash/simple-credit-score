import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler, RobustScaler

class MyDataPreprocessor(TransformerMixin):
    def __init__(self, max_age:int, max_years_of_employment:int, min_age_of_employment:int):
        """
        :param columns_to_remove: if not None select remove these columns from the dataframe
        """
        self.scaler = RobustScaler() # StandardScaler()
        self.maximum_age = max_age
        self.max_years_of_employment = max_years_of_employment
        self.min_age_of_employment = min_age_of_employment
        self.person_emp_length_median = 0
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
            data = data[data['person_age'] > data['person_emp_length'] + self.min_age_of_employment]
        data["cred_hist_to_age"] = data['cb_person_cred_hist_length']/data['person_age']
        data = data.drop('cb_person_cred_hist_length', axis=1)
        data = data.drop('person_age', axis=1)
        data = pd.get_dummies(data, drop_first=True)
        data = data.reindex(sorted(data.columns), axis=1)
        return data
    
    def preprocess_test_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop_duplicates()
        data['person_emp_length'] = data['person_emp_length'].fillna(self.person_emp_length_median)
        data['loan_int_rate'] = data['loan_int_rate'].fillna(self.loan_int_rate_mean)
        data["cred_hist_to_age"] = data['cb_person_cred_hist_length']/data['person_age']
        data = data.drop('cb_person_cred_hist_length', axis=1)
        data = data.drop('person_age', axis=1)
        data = pd.get_dummies(data, drop_first=True)
        data = data.reindex(sorted(data.columns), axis=1)
        return data

    def fit(self, data: pd.DataFrame, *args):
        """
        Prepares the class for future transformations
        :param data: pd.DataFrame with all available columns
        :return: self
        """
        data = data.drop_duplicates()
        self.person_emp_length_median = data['person_emp_length'].median()
        self.loan_int_rate_mean = data['loan_int_rate'].mean()
        data = self.preprocess_train_data(data)
        self.scaler = self.scaler.fit(data.to_numpy())
        return self

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        """
        Transforms features so that they can be fed into the regressors
        :param data: pd.DataFrame with all available columns
        :return: np.array with preprocessed features
        """
        features = self.preprocess_test_data(data)
        processed_features = np.array(self.scaler.transform(features.to_numpy()))
        return processed_features