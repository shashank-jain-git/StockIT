adx_df = calculate_adx(data, 14)

data['ADX'] = adx_df['ADX']
data['PLUS_DI'] = adx_df['+DI']
data['MINUS_DI'] = adx_df['-DI']

indicators_data['adx'] = []

for idx, row in data.iterrows():

            indicators_data['adx'].append({
                'time': int(idx.timestamp()),
                'adx': None if pd.isna(row['ADX']) else float(row['ADX']),
                'plus_di': None if pd.isna(row['PLUS_DI']) else float(row['PLUS_DI']),
                'minus_di': None if pd.isna(row['MINUS_DI']) else float(row['MINUS_DI'])
            })