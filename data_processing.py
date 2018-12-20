import json
import pandas as pd
import arrow
data = json.loads(open('data.json').read())

#print (data)

stringe = json.dumps(data[0])
o=json.loads(stringe)

#print (str)

#sk=pd.read_json(sf)
#gf=pd.DataFrame(sf)
#print (gf.head())
print (type(o))

#print (o['value'])
#df = pd.read_csv(sf , sep=";")
#gf = pd.DataFrame(df)
#print (gf.head())
df = pd.io.json.json_normalize(o)
df.columns = df.columns.map(lambda x: x.split(".")[-1])

print (df.shape)
print (df.head())

new_date = df['time']
print (new_date)
fg=[]
for i in range(0,len(new_date)):
	local=arrow.get(new_date[i])
	hj=local.timestamp
	fg.append(hj)

print (fg[0])
print (len(fg))

df['time']=fg
dfr=df.reindex(index=df.index[::-1])
print (dfr.head())
n_dfr=dfr['time']
df.sort_values('time')
for i in range(0,len(n_dfr)):
	print (n_dfr[i+1]-n_dfr[i])


