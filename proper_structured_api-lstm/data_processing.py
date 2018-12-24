import json
import pandas as pd
import arrow
import urllib.parse as urlparse
from urllib.request import urlopen
import sys
def data_preprocessing(start_time , end_time):
	#start_time= sys.argv[1]
	#end_time = sys.argv[2]
	b_start_time=int(start_time)
	b_end_time=int(end_time)
	request = urlopen("http://api.faclon.com:4000/getData?device=GHEM_A1&sensor=APR&sTime=%d&eTime=%d"%(b_start_time,b_end_time))
	#request=urlopen(url)
	response=request.read()
	data = json.loads(response)
	#print (data)

	stringe = json.dumps(data[0])
	o=json.loads(stringe)

	#print (str)

	#sk=pd.read_json(sf)
	#gf=pd.DataFrame(sf)
	#print (gf.head())
	#print (type(o))

	#print (o['value'])
	#df = pd.read_csv(sf , sep=";")
	#gf = pd.DataFrame(df)
	#print (gf.head())
	df = pd.io.json.json_normalize(o)
	df.columns = df.columns.map(lambda x: x.split(".")[-1])

	#print (df.shape)
	#print (df.head())

	new_date = df['time']
	#print (new_date)
	fg=[]
	for i in range(0,len(new_date)):
		local=arrow.get(new_date[i])
		hj=local.timestamp
		fg.append(hj)

	#print (fg[0])
	#print (len(fg))

	df['time']=fg
	dfr=df.reindex(index=df.index[::-1])
	dfr = dfr.reset_index(drop=True)
	#print (dfr.head())
	n_dfr=dfr['time']
	df.sort_values('time')
	dfg =[]
	def difference_of_iitb(dfl):
		dfg.append(0)
		for i in range(1,len(df)):
			 dfg.append(dfl[i]-dfl[i-1])
	difference_of_iitb(n_dfr)
	#print (len(dfg))
	df['diff_interval']=dfg
	#print  (df['diff_interval'])
	cumm =[]
	def cummulative_of_iitb(dfl):
		cumm.append(0)
		for i in range(1,len(df)):
			 cumm.append(cumm[i-1]+dfl[i])
	cummulative_of_iitb(dfg)

	#print (cumm)
	df['cummulative_of_iitb'] = cumm
	#print (df.head())

	df = df[(df.diff_interval>24)]
	df=df[(df.value>20000)]
	print (len(df))

	#def equivalent_timestamp(df):
	#	for i in range(0,len(df)):
	#		df['cummulative_of_iitb'][i]=int(df['cummulative_of_iitb'][i]/30)

	#equivalent_timestamp(df)
	df['cummulative_of_iitb']=df['cummulative_of_iitb']/30
	df['int_cumm_of_iitb']=df['cummulative_of_iitb'].astype(int)

	#print (df.head())
	final_dataframe = ['time','value']
	my_df  = pd.DataFrame(columns = final_dataframe)

	my_df['time'] =df[ 'int_cumm_of_iitb']
	my_df['value'] = df['value']
	my_df.to_csv('unwanted1.csv', index = False)

	return(my_df)
	#return final_dataframe

