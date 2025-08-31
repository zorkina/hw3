import numpy as np
import pandas as pd

"""
1) Заполняет пропуски 
2) Удаляет высокоскорреллированные фичи
3) Считает среднее по каждой числовой фиче
4) Обрабатывает категориальные фичи. Важно: и не только те, которые представлены типом
object, но и числовые, у которых менее 25 уникальных значений
5) Разбивает колонку со временем (create_dttm) на год, месяц и день
"""

class Preprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.num_features = [col for col in df.columns if self.df[col].dtype != 'object']
        self.cat_features = [col for col in df.columns if col not in self.num_features]
        self.num_features_less_25 = [col for col in self.num_features if len(col.unique()) < 25]

    def fill_gaps(self):
        for col in self.df.columns:
            if self.df[col] in self.cat_features:
                self.df[col] = self.df[col].fillna('Unknown')
            else:
                self.df[col] = self.df[col].fillna(self.df[col].median()) # лучше не нулем а медианой

    def del_features(self, thresold = 0.8):
        corr_matrix = self.df.corr().abs()


    def mean_numerical_features(self):
        return self.df[self.num_features].mean()

    def process_categorical_features(self):
        for col in self.cat_features:
            # MTE

        for col in self.num_features_less_25:
            # OHE


    def split_columns(self):
        self.df['Date'] = pd.to_datetime(self.df['Date']) # возбми колонку дейт и преврати ее в тип даты

        self.df['Year'] = self.df['Date'].dt.year # достаём год и сохраняем его в новую колонку Year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Day'] = self.df['Date'].dt.day

