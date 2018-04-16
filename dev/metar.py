from bs4 import BeautifulSoup
import urllib.request

def metar():
    webpage = "https://aviationweather.gov/adds/tafs/?station_ids=CYUL&std_trans=translated&submit_both=Get+TAFs+and+METARs"
    websource = urllib.request.urlopen(webpage)
    soup = BeautifulSoup(websource.read(), "html.parser")
    all = soup.find_all("strong", {"id": ""})
    raw_data = all[1]
    metar_html = str(raw_data).split("<strong>")
    metar_html = metar_html[1].split("</strong>")
    metar_RMK = metar_html[0].split("RMK")
    metar_full = (metar_RMK[0])
    print (metar_full)
    metar.replace("\n", "")
    metar = metar_full.split(' ')
    return metar

metar = metar()
print (metar)
