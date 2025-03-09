import pandas as pd


file_path = 'cleaned_coingecko_data.csv'
data = pd.read_csv(file_path)

# Pivot the data
pivoted_data = data.melt(  
    id_vars=['Name', 'Symbol', 'Price Category'],  
    value_vars=['1h', '24h', '7d'],  
    var_name='Performance Metric',  
    value_name='Performance Value' 
)


pivoted_data.to_csv('2_pivoted_data.csv', index=False)