import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import lightgbm as lgbm
from sklearn.preprocessing import StandardScaler


class GBDTRegressor:

    def __init__(self, n_estimators=100, n_jobs=7, seed=42, verbose=False):
        self.n_estimators = n_estimators
        self.n_jobs = n_jobs
        self.seed = seed
        self.verbose = verbose
        self.model = None
        self.symbols = None
        self.xvars = None

    def fit(self, X, y):

        self.xvars = X.columns.to_list()

        num_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
                                          ('scaler', StandardScaler())])
        preprocessor = ColumnTransformer(transformers=[('num', num_transformer, self.xvars)])
        base_estimator = lgbm.LGBMRegressor(random_state=self.seed,
                                            objective='quantile',
                                            metric='quantile',
                                            alpha=0.5,
                                            boosting_type='gbdt',
                                            n_estimators=self.n_estimators,
                                            reg_alpha=0.90,  # Hard L1 regularization
                                            reg_lambda=0.90,
                                            n_jobs=1)
        model = MultiOutputRegressor(estimator=base_estimator, n_jobs=self.n_jobs)
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                         ('classifier', model)], verbose=self.verbose)

        model_pipeline.fit(X=X, y=y)

        self.model = model_pipeline
        self.symbols = y.columns.to_list()

        return self

    def predict(self, X):
        assert isinstance(X, pd.DataFrame), "X must be a dataframe"
        assert not (self.model is None), "The model is empty. Please run fit first!"
        y_columns = self.symbols or [str(a).replace('_close', '') for a in X.columns]

        return pd.DataFrame(data=self.model.predict(X), index=X.index, columns=y_columns)


