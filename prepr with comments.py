import numpy as np
import pandas as pd

"""
1) готово: Заполняет пропуски 
2) готово: Удаляет высокоскорреллированные фичи
3) готово: Считает среднее по каждой числовой фиче
4) готово: Обрабатывает категориальные фичи. Важно: и не только те, которые представлены типом
object, но и числовые, у которых менее 25 уникальных значений
5) готово: Разбивает колонку со временем (create_dttm) на год, месяц и день
"""

# обращение к колонке
# 1. df['col'] — основной способ
#    - Используется всегда, безопасен
#    - col — строка с названием колонки
#    Пример:
#        df['age']        # колонка 'age'
#        df[col]          # если col = 'age'

# 2. df.columns — список всех имён колонок (тип Index[str])
#    - Используется в циклах, например:
#
#        for col in df.columns:
#            print(col)       # печатает имя колонки (строка)
#            print(df[col])   # выводит саму колонку (Series)

# Пояснение:
# - col — это строка, имя колонки 'name'
# - df[col] — сам столбец данных (тип Series) 'Liza Katya Masha'
# - df.col — красивый синтаксис, но менее универсальный

# UNIQUE
# Это метод, который возвращает массив всех уникальных значений в колонке:
# df['city'].unique()
# # → array(['Moscow', 'Paris', 'London'], dtype=object)
#
# NUNIQUE
# Это метод, который возвращает количество уникальных значений:
# df['city'].nunique()
# # → 3
# 📌 n = number → “number of unique values”

# df.loc[строка, колонка]
# df.loc['Alice', 'Age'] → Возьмёт значение из строки с именем 'Alice' и колонки 'Age'
# df.loc['Alice', ['Age', 'City']] → Возьмёт у Alice возраст и город

# 	•	df.loc — по именам (label-based)
# 	•	df.iloc — по номерам (integer-based)

# Используешь
# df.loc[] Когда знаешь имена
# df.iloc[]  Когда знаешь номера


class Preprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # self.num_features и self.cat_features
        # лежат именно названия колонок (то есть строки),
        # а не сами колонки и не значения внутри них
        self.num_features = [col for col in df.columns if self.df[col].dtype != 'object']
        self.cat_features = [col for col in df.columns if col not in self.num_features]
        # col это не колонка а ее имя, df[col] сама колонка, df.columns список всех имён колонок
        self.num_features_less_25 = [col for col in self.num_features if self.df[col].nunique() < 25]
        self.df.columns = self.df.columns.str.strip() # очищаем, strip() удаляет лишние пробелы в начале и в конце строки

    def fill_gaps(self):
        # self.df.columns это обращение к названиям колонок, а не к самим данным
        for col in self.df.columns:
            if col in self.cat_features:
                self.df[col] = self.df[col].fillna('Unknown')
            else:
                self.df[col] = self.df[col].fillna(self.df[col].median()) # лучше не нулем а медианой

    def del_features(self, thresold = 0.8):
        corr_matrix = self.df.corr().abs()
        to_drop = set()
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                if corr_matrix.loc[col1, col2] > thresold:
                    if col2 not in to_drop:
                        to_drop.add(col2)
        self.df.drop(columns=to_drop, inplace=True)

    def mean_numerical_features(self):
        return self.df[self.num_features].mean()

    # обрабатывать кат фичи это преобразовать кат столбцы в числовые, чтобы их понимала модель машинного обучения
    # если задача просто обработать данные без обучения модели или мы не знаем, что будет таргетом, то:
    # OHE безопасен: просто превращает категорию в цифры (но дублирует память)
    # MTE нельзя делать — тк у нас нет таргета, от которого брать среднее
    def process_categorical_features(self):
        cols_to_encode = self.num_features_less_25 + self.cat_features
        self.df = pd.get_dummies(self.df, columns=cols_to_encode)


    def split_columns(self):
        try:
            self.df['Date'] = pd.to_datetime(self.df['Date']) # возбми колонку дейт и преврати ее в тип даты
            self.df['Year'] = self.df['Date'].dt.year # достаём год и сохраняем его в новую колонку Year
            self.df['Month'] = self.df['Date'].dt.month
            self.df['Day'] = self.df['Date'].dt.day
        except: KeyError('колонка не найдена')

    def __str__(self):
        return str(self.df)
