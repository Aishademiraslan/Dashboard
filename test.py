import requests

import pandas as pd

file_paths = [
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.28.2.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.28.3.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.29.2.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.30.2.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.30.3.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.31.2.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.32.2.csv',
    'C:\\Users\\aide\\OneDrive - "x"\\Documents\\"x"\\Raitan\\192.168.33.2.csv' "x" used because original credentials were removed due to confidentiality
]

def get_merged_data(file_paths):
    data_frames = []

    for file in file_paths:
        df = pd.read_csv(file, delimiter=';', header=0)
        data_frames.append(df)

    merged_df = pd.concat(data_frames).reset_index(drop=True)
    return merged_df

df1 = get_merged_data(file_paths)
df1['timestamp'] = pd.to_datetime(df1['timestamp']).dt.floor('h')
# print(df1)
filter = '{"PriceArea":"DK2"}'
response = requests.get(f'https://api.energidataservice.dk/dataset/CO2EmisProg?start=2024-10-17&end=2025-02-08&columns=Minutes5DK,CO2Emission&filter={filter}&sort=Minutes5UTC%20ASC').json()['records']
df2 = pd.DataFrame(response)
df2['Minutes5DK'] = pd.to_datetime(df2['Minutes5DK'])
df2_resampled = df2.resample('h', on='Minutes5DK').mean().reset_index()
df2['Minutes5DK'] = pd.to_datetime(df2['Minutes5DK']).dt.floor('h')
# print(df2_resampled)

merged = pd.merge(df1, df2_resampled, left_on='timestamp', right_on='Minutes5DK')
merged['CO2Emission'] = round(merged['CO2Emission'], 2)
merged['Our_CO2_Emissions_In_Grams'] = round(merged['CO2Emission'] * merged['VA'] / 1000, 2)

final_df = merged[['endpoint', 'timestamp', 'VA', 'CO2Emission', 'Our_CO2_Emissions_In_Grams']]
final_df.rename(columns={'timestamp': 'Timestamp'}, inplace=True)
final_df.sort_values(by='Timestamp', ascending=True, inplace=True)
print(final_df)

final_df.to_csv('2024-10-17 - 2025-02-07 CO2Emissions.csv', sep=',', decimal='.', index=False, float_format='%.2f')
