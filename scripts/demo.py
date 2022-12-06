import bme
import pandas as pd
from ml_project.tools import create_datasets
from ml_project.gbdt_regressor import GBDTRegressor
from config import data_dir
from pathlib import Path

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# df = bme.BME().get_underlyings_history_data()
# df.to_csv(Path(data_dir) / 'ibex35_30days.csv', index=False)

df = pd.read_csv(Path(data_dir) / 'ibex35_30days.csv')
tmp = df[['Fecha','Cierre','symbol']].copy()
tmp['Fecha'] = pd.to_datetime(tmp['Fecha'], format='%d/%m/%Y')
tmp['Cierre'] = tmp['Cierre'].apply(lambda x: float(str(x).replace(',', '.')))
tmp = tmp.rename(columns={'Fecha': 'date', 'Cierre': 'close'})
aux = tmp.pivot(index=['date'], columns=['symbol'], values=['close'])
aux.columns = aux.columns.get_level_values('symbol').to_list()


df_features, df_target = create_datasets(aux)
x_train, y_train = df_features.loc[:'2022-11-30'], df_target.loc[:'2022-11-30']
x_test, y_test = df_features.loc['2022-12-01':], df_target.loc['2022-12-01':]


m = GBDTRegressor()
m.fit(X=x_train, y=y_train)
df_pred = m.predict(X=x_test)

