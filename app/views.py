# -*- coding: utf-8 -*-

from app import app

@app.route('/')
@app.route('/index')

def index():

	import numpy as np
	import json
	import gspread
	from oauth2client.client import SignedJwtAssertionCredentials

	json_key = json.load(open('./costfish-3a4d1968df8f.json'))
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

	gc = gspread.authorize(credentials)


	wks = gc.open('costfish')
	sheet = wks.sheet1
	list_of_lists = sheet.get_all_values()

	import pandas as pd

	columns_name=['Date','牛','羊','豬','雞','魚','貝','蟹','軟絲','高麗菜','空心菜','絲瓜','南瓜','西瓜','柳丁','鳯梨','百合','蓮子','紅棗']
	df = pd.DataFrame(list_of_lists[1:],columns=columns_name,dtype=float)
	nparray = df.as_matrix()
	rows , columns = nparray.shape

	lastPriceList = nparray[rows-1][1:]
	last2ThPriceList =nparray[rows-2][1:]

	priceChangeList = lastPriceList - last2ThPriceList
	priceChPercent = priceChangeList / last2ThPriceList

	r = '<img src=https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn2/v/t1.0-1/c18.0.160.160/p160x160/556433_337509823007948_1184595735_n.jpg?oh=286a67f0cc1a125346a3d7cb7b6b23e8&oe=561FB8BD&__gda__=1444064936_e6a1665103cd0e5412e2d0e198e7d442 /><br><h1>'
	kpiindex=[]
	for index , change in enumerate(priceChPercent) :
    		if change > 0.05 : 
        		r += columns_name[index + 1] + ': '  + str(round(change*100,2))+ '%<br>'
	return r
	
