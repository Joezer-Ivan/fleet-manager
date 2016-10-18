from django.shortcuts import render
from django.http import HttpResponse
# from BeautifulSoup import BeautifulSoup
# import mechanize
import random
import mechanicalsoup
from Buses.serializers import CurrentLocationSerializer
from rest_framework import generics
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


def Choose_Location(request):
	ob = Routes.objects.all().values_list("stage")
	route_list = []
	for i,route in enumerate(ob):
		route_list.append(re.sub("\S*\d\S*", "", route[0]).strip())

	route_list = list(filter(None, route_list))
	route_list = sorted(route_list)
	return TemplateResponse(request,"choice.html",{'ob':route_list})


def Bus_route(request):

	source = request.POST["from"]
	dest = request.POST["to"]
	ob = Routes.objects.all().filter(stage = str(source))
	ob2 = Routes.objects.values("route").filter(stage = str(source))


	ob2 = list(ob2)
	route = ob2[0]['route'].replace('(','')
	route = ob2[0]['route'].replace(')','')

	route = re.sub(r"\(","",route)
	route = route.replace("'","")
	route = route.split(',')

	ob = Routes.objects.all().filter(stage = str(dest))
	ob2 = Routes.objects.values("route").filter(stage = str(dest))

	ob2 = list(ob2)
	route1 = ob2[0]['route'].replace('(','')
	route1 = ob2[0]['route'].replace(')','')

	route1 = re.sub(r"\(","",route1)
	route1 = route1.replace("'","")
	route1 = route1.split(',')

	common_routes = list(set(route).intersection(route1))

	occupancy = []
	eta = []
	lat = []
	lon = []
	for indices in common_routes:
		occupancy.append(random.randint(10,80))
		eta.append(random.randint(1,60))
		lat.append(random.uniform(12.0067074,13.586019))
		lon.append(random.uniform(79.2022314,80.021088))

	ob4 = zip(common_routes,occupancy,eta,lat,lon)
	ob4 = sorted(ob4, key=lambda x: x[2])

	# return HttpResponse(route)
	return TemplateResponse(request,"routes.html",{'source':source,'dest':dest,'ob':ob,'ob2':route,'ob3':route1,'ob4':ob4,'occupancy':occupancy,'eta':eta})



class CurrentLocationList(generics.ListCreateAPIView):
    queryset = CurrentLocation.objects.all()
    serializer_class = CurrentLocationSerializer


class CurrentLocationDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = CurrentLocation.objects.all()
	serializer_class = CurrentLocationSerializer
	lookup_field = 'license_plate'
