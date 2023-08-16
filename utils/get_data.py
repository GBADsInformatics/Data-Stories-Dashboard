import pandas as pd
import api_helpers as ah
import os


## ISO Mappings 
## At the time of writing, all datasources except for fao do not have the iso codes in the table. 
## We add them in here.
def map_to_iso3(df):
    
    iso_code_file_path = "../data/FAOSTAT_mappings.csv"
    iso_code_df = pd.read_csv(iso_code_file_path)
    merged_df = pd.merge(df, iso_code_df, how='inner', left_on='country', right_on='Short name', left_index=False, right_index=False)

    return(merged_df)

### Get data for the dashboard and store it in /data
###--------------Get data------------------------------------

tables = ['livestock_countries_population_eurostat','livestock_countries_population_faostat','livestock_countries_population_faotier1','livestock_countries_population_oie','livestock_countries_population_unfccc']

wd = os.getcwd()

for i in tables: 
    df = ah.get_dataframe(i)
    source = str.split(i, '_')[-1:]
    out_name = '../data/%s.csv' % source[0]
    df = map_to_iso3(df)
    df = df[['country', 'species', 'year', 'population', 'ISO3']]
    df.to_csv(out_name, index=False)