from bs4 import BeautifulSoup
import urllib.request

aeroport_pos = 'CYUL'

metar = []

def metar():
	webpage = "https://aviationweather.gov/adds/tafs/?station_ids="+aeroport_pos+"&std_trans=translated&submit_both=Get+TAFs+and+METARs"
	websource = urllib.request.urlopen(webpage)
	soup = BeautifulSoup(websource.read(), "html.parser")
	all = soup.find_all("strong", {"id": ""})
	raw_data = all[1]
	metar_html = str(raw_data).split("<strong>")
	metar_html = metar_html[1].split("</strong>")
	metar_RMK = metar_html[0].split("RMK")
	metar_full = (metar_RMK[0])
	metar_full = (metar_full.replace("\n", ""))
	metar_full = metar_full.split(' ')	
	if metar_full[1].upper() == metar_full[1]:
		print (metar_full)
		vents = metar_full[2]
		altimetre = metar_full[9]
		metar.append(vents)
		metar.append(altimetre)
	else:
		print ('Metar Non-Disponible')

metar()
print (metar)
print (metar[0])
print (metar[1])
