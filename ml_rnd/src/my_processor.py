import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler, RobustScaler

class MyDataPreprocessor(TransformerMixin):
    def __init__(self, max_age:int, max_years_of_employment:int):
        """
        :param columns_to_remove: if not None select remove these columns from the dataframe
        """
        self.scaler = RobustScaler() # StandardScaler()
        self.maximum_age = max_age
        self.max_years_of_employment = max_years_of_employment

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data['person_emp_length'] = data['person_emp_length'].fillna(data['person_emp_length'].median())
        data['loan_int_rate'] = data['loan_int_rate'].fillna(data['loan_int_rate'].mean())
        data = data.drop_duplicates()
        if 'person_age' in data.columns:
            data = data[data['person_age'] <= self.maximum_age] 
        if 'person_emp_length' in data.columns:
            data = data[data['person_emp_length'] <= self.max_years_of_employment]
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
        data = self.preprocess_data(data)
        self.scaler = self.scaler.fit(data.to_numpy())
        return self

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        """
        Transforms features so that they can be fed into the regressors
        :param data: pd.DataFrame with all available columns
        :return: np.array with preprocessed features
        """
        features = self.preprocess_data(data)
        processed_features = np.array(self.scaler.transform(features.to_numpy()))
        return processed_features