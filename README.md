# ml_project


Summary of the project

## Getting started

Install
```commandline
pip install git+https://github.com/jorivero83/ml_project.git
```

Example of code

```Python
import bme
import pandas as pd
from ml_project.tools import create_datasets
from ml_project.gbdt_regressor import GBDTRegressor
from config import data_dir
from pathlib import Path

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Load data and preprocessing data
df = pd.read_csv(Path(data_dir) / 'ibex35_30days.csv')
tmp = df[['Fecha','Cierre','symbol']].copy()
tmp['Fecha'] = pd.to_datetime(tmp['Fecha'], format='%d/%m/%Y')
tmp['Cierre'] = tmp['Cierre'].apply(lambda x: float(str(x).replace(',', '.')))
tmp = tmp.rename(columns={'Fecha': 'date', 'Cierre': 'close'})
aux = tmp.pivot(index=['date'], columns=['symbol'], values=['close'])
aux.columns = aux.columns.get_level_values('symbol').to_list()

# Create datasets and split into train / test
df_features, df_target = create_datasets(aux)
x_train, y_train = df_features.loc[:'2022-11-30'], df_target.loc[:'2022-11-30']
x_test, y_test = df_features.loc['2022-12-01':], df_target.loc['2022-12-01':]

# Create instance of the model and predict
m = GBDTRegressor()
m.fit(X=x_train, y=y_train)

# Get predictions
df_pred = m.predict(X=x_test)
```

Results
```commandline
              ACS    ACX        AENA        AMS         ANA    ANE   BBVA   BKT   CABK       CLNX    COL        ELE     ENG    FDR        FER    GRF     IAG     IBE    IDR        ITX    MAP    MEL    MRL        MTS       NTGY        PHM        RED     REP       ROVI     SAB    SAN   SCYR   SGRE     SLR    TEF
date                                                                                                                                                                                                                                                                                                                  
2022-12-01  26.58  9.404  123.199997  51.259998  186.600006  37.98  5.519  6.14  3.419  33.540001  5.875  18.139999  17.375  14.16  25.450001  10.18  1.5505  10.655  9.795  24.639999  1.826  5.025  9.065  25.469999  26.780001  65.139999  17.290001  14.295  38.880001  0.8558  2.774  2.564  18.02  16.885  3.592
2022-12-02  26.58  9.404  123.199997  51.259998  186.600006  37.98  5.519  6.14  3.419  33.540001  5.875  18.139999  17.375  14.16  25.450001  10.18  1.5505  10.655  9.795  24.639999  1.826  5.025  9.065  25.469999  26.780001  65.139999  17.290001  14.295  38.880001  0.8558  2.774  2.564  18.02  16.885  3.592

```