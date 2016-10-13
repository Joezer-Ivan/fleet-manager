from django.shortcuts import render
from django.http import HttpResponse
# from BeautifulSoup import BeautifulSoup 
# import mechanize
# Create your views here.
import mechanicalsoup 
from bs4 import BeautifulSoup
from django.template.response import TemplateResponse



def areas_of_chennai(request):

	browser = mechanicalsoup.Browser(soup_config={"features":"html.parser"})
	page = browser.get("http://www.mapsofindia.com/lat_long/tamilnadu/")

	soup = BeautifulSoup(page.text,"html.parser")

	table = soup.find("table",{"class":"tableizer-table"})

	tr = table.findAll("tr")
	tr.pop(0)

	dic = {}
	for row in tr:
		td = row.findAll("td")
		lat = td[1].getText().replace("&deg","")
		lat = lat.replace(";",".")
		lat = lat.replace("' N","")
		lat = lat.replace(' ','')
		lat = lat.encode('ascii','ignore')
		lat = float(lat)
		lon = td[2].getText().replace("&deg","")
		lon = lon.replace(";",".")
		lon = lon.replace("' E","")
		lon = lon.replace(' ','')
		lon = lon.encode('ascii','ignore')
		lon = float(lon)
		dic[td[0].getText()]=(lat,lon)
		# for i,cells in enumerate(td):
		# 	print(cells.getText(),end='|')
			
		
	# for towns in dic:
	# 	print(towns,dic[towns])
	return TemplateResponse(request,"index.html",{'towns':dic})
