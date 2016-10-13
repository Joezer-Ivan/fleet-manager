from django.shortcuts import render
from django.http import HttpResponse
# from BeautifulSoup import BeautifulSoup
# import mechanize
# Create your views here.
import mechanicalsoup
from bs4 import BeautifulSoup
from django.template.response import TemplateResponse
import re
from .models import *

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


def mtc(request):

	browser = mechanicalsoup.Browser(soup_config={"features":"html.parser"})
	page = browser.get("http://www.mtcbus.org/Routes.asp")


	soup = BeautifulSoup(page.text,"html.parser")
	select = soup.findAll("select",{"name":"cboRouteCode"})
	routes = select[0].findAll("option")

	dic = {}
	for route in routes:
		print(route.getText())
		url = "http://www.mtcbus.org/Routes.asp?cboRouteCode="+str(route.getText())+"&submit=Search"
		response = browser.get(url)

		soup = BeautifulSoup(response.text,"html.parser")
		table = soup.findAll("table",{"border":"1"})
		td = table[0].findAll("td",{"align":"left"})

		for data in td:
			if 'Go Back' not in data.getText():

				place = str(data.getText())

				if place in dic:
					dic[place] = dic[place],str(route.getText())

				else:
					dic[place] = str(route.getText())




	for place in dic:
		ob = Routes(stage=str(place),route = str(dic[place]))
		ob.save()


	return HttpResponse("done")



def Bus_route(request):
	ob = Routes.objects.all().filter(stage = "PORUR")
	ob2 = Routes.objects.values("route").filter(stage = "PORUR")
	ob2 = list(ob2)
	route = ob2[0]['route'].replace('(','')
	route = ob2[0]['route'].replace(')','')

	route = re.sub(r"\(","",route)
	route = route.replace("'","")
	route = route.split(',')

	# return HttpResponse(route)
	return TemplateResponse(request,"routes.html",{'ob':ob,'ob2':route})

	
