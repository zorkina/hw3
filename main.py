import numpy as np
import pandas as pd

from prepr import Preprocessor

df = pd.read_csv('any_data.csv')
p = Preprocessor(df)
p.fill_gaps()
p.del_features()
p.split_columns()
print(p.df.head())