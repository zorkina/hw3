import pandas as pd


class Preprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.num_features = [col for col in df.columns if self.df[col].dtype != 'object']
        self.cat_features = [col for col in df.columns if col not in self.num_features]
        self.num_features_less_25 = [col for col in self.num_features if self.df[col].nunique() < 25]
        self.df.columns = self.df.columns.str.strip()

    def fill_gaps(self):
        for col in self.df.columns:
            if col in self.cat_features:
                self.df[col] = self.df[col].fillna('Unknown')
            else:
                self.df[col] = self.df[col].fillna(self.df[col].median())

    def del_features(self, thresold=0.8):
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

    def process_categorical_features(self):
        cols_to_encode = self.num_features_less_25 + self.cat_features
        self.df = pd.get_dummies(self.df, columns=cols_to_encode)

    def split_columns(self):
        try:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Year'] = self.df['Date'].dt.year
            self.df['Month'] = self.df['Date'].dt.month
            self.df['Day'] = self.df['Date'].dt.day
        except:
            KeyError('колонка не найдена')

    def __str__(self):
        return str(self.df)
