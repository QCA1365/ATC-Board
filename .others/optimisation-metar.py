from bs4 import BeautifulSoup
import urllib.request

aeroport_pos = 'CYUL'

def getMETAR(aeroport_pos):
    webpage = "https://aviationweather.gov/adds/tafs/?station_ids="+aeroport_pos+"&std_trans=translated&submit_both=Get+TAFs+and+METARs"
    websource = urllib.request.urlopen(webpage)
    soup = BeautifulSoup(websource.read(), "html.parser")
    all = soup.find_all("strong", {"id": ""})
    raw_data = all[1]
    metar_html = str(raw_data).split("<strong>")
    metar_html = metar_html[1].split("</strong>")
    metar_RMK = metar_html[0].split("RMK")
    metar_full = (metar_RMK[0])
    return metar_full

def affichermeteo():
    metar = getMETAR(aeroport_pos)
    if metar.upper() == metar:
        print (metar.replace("\n", ""))

    else:
        print ('\nMetar Non-Disponible\n')

def meteo():
        metar = getMETAR(aeroport_pos)
        if metar.upper() == metar:
            metar = metar.split(' ')
            for i in metar:
                if i[-2:] == 'KT':
                    vents = i
                    break

            for i in metar:
                if i != "":
                    if i[0] == 'A' or i[0] == 'Q':
                        altimetre = i[1:]
                        break
            return (vents , altimetre)
            
        else:
                print ('\nMetar Non-Disponible\n')
                QNH = input('Altimetre? ')
                return('[VENTS]', QNH)
                
(vents, altimetre) = meteo()
print (vents)
print (altimetre)

affichermeteo()
