import pandas as pd


def create_datasets(X: pd.DataFrame):
    Xt = add_lags(X)
    Xt = Xt.drop(index=X.index[-1], axis=0).copy()
    yt = X.shift(-1).drop(index=X.index[-1], axis=0).copy()
    return Xt, yt.iloc[2:]


def add_lags(X):
    orig_columns = X.columns.to_list()
    X = X.copy()

    # Add lag 1
    V = X.shift(1)
    V.columns = [f"{a}_lag1" for a in orig_columns]

    # Add lag 2
    V1 = X.shift(2)
    V1.columns = [f"{a}_lag2" for a in orig_columns]

    X = pd.merge(X, V, on=['date'], how='left')
    X = pd.merge(X, V1, on=['date'], how='left')

    return X.iloc[2:]
