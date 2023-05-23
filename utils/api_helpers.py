import requests
import pandas as pd
import json
import csv
import psycopg2 as ps


#### Database directly 

def connect_public():    
#
# Create connection and cursor
#
    conn = ps.connect("host=gbadske-database-public-data.cp73fx22weet.ca-central-1.rds.amazonaws.com dbname=publicData_1 user=reader password=readonly")
# 
# Return connection information
#
    return conn

def get_dataframe(table_name):
    
	# Connect to db
    conn = connect_public()
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM {table_name}""")
    
	# Get column names 
    cols = [x[0] for x in cur.description]
    
	# Read in result as dataframe 
    df = pd.DataFrame(cur.fetchall())
    
    df.columns = [x for x in cols]

    conn.close()
    
    return df

#### API helpers
def get_content_size(url):

	# Get response from url
	r = requests.get(url)

	# Get size of response 
	content_size = len(r.content)
	
	return(content_size)


def construct_api_call(table_name): 

    base_url = 'https://gbadske.org/api/GBADsPublicQuery/'
    query = '?fields=*&query=&format=text'
    url = '%s%s%s' % (base_url, table_name, query)

    return(url)

def test_call(url): 

	# Test to see if call is successful
	r = requests.get(url)
	if r.status_code == 404:
		return(0)
	else: 
		return(1)

def make_call(url): 

	with requests.Session() as s:

		download = s.get(url)

		decoded_content = download.content.decode('utf-8')

		cr = csv.reader(decoded_content.splitlines(), delimiter=',')

		my_list = list(cr)

		df = pd.DataFrame(my_list)
		df.columns = df.iloc[0]
		df = df[1:]

	return(df)