from urllib import urlopen
from urllib.request import urlopen
request = urlopen("http://api.faclon.com:4000/getData?device=GHEM_A2&sensor=APR&sTime=1545046374&eTime=1545053708")
response=request.read()
json=json.loads(response)