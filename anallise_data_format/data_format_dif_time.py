import time
import pandas as pd
import numpy as np
from pyarrow import feather

file_ftr = "serverpings.ftr"
file_hf = 'dataset.h5'
file_csv = 'dataset.csv'
file_exel = 'dataset.xlsx'
file_json = 'dataset.json'
file_parquet = 'dataset.parquet'
n_rows = 100000

dataset = pd.DataFrame(
    data={
        'string': np.random.choice(('apple', 'banana', 'carrot'), size=n_rows),
        'timestamp': pd.date_range("20130101", periods=n_rows, freq="s"),
        'integer': np.random.choice(range(0, 10), size=n_rows),
        'float': np.random.uniform(size=n_rows),
    },
)


def time_human_read_file(file_exc, file_name):
    start_time = time.time()
    file_exc(file_name)
    return time.time() - start_time

# csv time calculate
time_to_csv = time_human_read_file(dataset.to_csv,file_csv)
time_from_csv = time_human_read_file(pd.read_csv,file_csv)

# exel time calculate
time_to_exel = time_human_read_file(dataset.to_excel,file_exel)
time_from_exel = time_human_read_file(pd.read_excel, file_exel)

# json time calculate
time_to_json = time_human_read_file(dataset.to_json,file_json)
time_from_json = time_human_read_file(dataset.to_json,file_json)
# ftr time calculation
time_to_ftr = time_human_read_file(dataset.to_feather,file_ftr)
time_from_ftr = time_human_read_file(pd.read_feather,file_ftr)

# parquet time calculation
time_to_parquet = time_human_read_file(dataset.to_parquet,file_parquet)
time_from_parquet = time_human_read_file(pd.read_parquet,file_parquet)




#feather_format
# hdf time calculate
start_time = time.time()
dataset.to_hdf('dataset.h5', key='dataset', mode='w')
time_to_hdf =  time.time() - start_time

start_time = time.time()
pd.read_hdf('dataset.h5')
time_from_hdf = time.time() - start_time

# create plot
time_compare_format = pd.DataFrame({
     'load_time': [time_to_hdf, time_to_json,time_to_csv,time_to_exel, time_to_ftr, time_to_parquet],
     'download_time': [time_from_hdf, time_from_json,time_from_csv, time_to_exel, time_from_ftr, time_from_parquet],
     'time_format': ['hdf','json','csv','exel','ftr', 'parquet']})

fig = time_compare_format.plot(kind='bar',x='time_format',y=['download_time','load_time']).get_figure()
fig.savefig('time_compare_format.png')