import os
from sys import platform
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
listeAvions = []
listeATC = []
squawk = []
compagnies = []
aeroports = []
anglais = []
francais = []
positions = []
fir = []

def platforme(platform):
	if platform == "linux" or platform == "linux2":
		os.system('clear')
	elif platform == "win32":
		os.system('CLS')

def position():
    position = []
    aeroport_pos =''
    while len(aeroport_pos) != 4:
        aeroport_pos = input('Quel est le code OACI de l\'aeroport / de la FIR? ') 

    while position != '1' and position != '2' and position != '3' and position != '4' and position != '5' and position != '6':
        print ('1. XXXX_DEL')
        print ('2. XXXX_GND')
        print ('3. XXXX_TWR')
        print ('4. XXXX_DEP')
        print ('5. XXXX_APP')
        print ('6. XXXX_CTR')
        print('7. XXXX_FSS')
        position = input('Quelle position? ')
        platforme(platform)
    return (position, aeroport_pos)

def getMETAR(aeroport_pos,position):
    webpage = "https://aviationweather.gov/adds/tafs/?station_ids="+aeroport_pos+"&std_trans=translated&submit_both=Get+TAFs+and+METARs"
    websource = urllib.request.urlopen(webpage)
    soup = BeautifulSoup(websource.read(), "html.parser")
    all = soup.find_all("strong", {"id": ""})
    raw_data = all[1]
    metar_html = str(raw_data).split("<strong>")
    metar_html = metar_html[1].split("</strong>")
    if position == '6' or position == '7':
        metar_full = metar_html[0]
    else:
        metar_RMK = metar_html[0].split("RMK")
        metar_full = (metar_RMK[0])
    return metar_full

def affichermeteo(aeroport_pos):
    metar = getMETAR(aeroport_pos,position)
    if metar.upper() == metar:
        print (metar.replace("\n", ""))

    else:
        print ('\nMetar Non-Disponible\n')

def meteo(aeroport_pos):
        metar = getMETAR(aeroport_pos,position)
        if metar.upper() == metar:
            metar = metar.split(' ')
            for i in metar:
                if i[-2:] == 'KT':
                    vents = i
                    break

            for i in metar:
                if i != "":
                    if i[0] == 'A' or i[0] == 'Q':
                        altimetre = i[1:].replace("\n", "")
                        break
            return (vents , altimetre)
            
        else:
                print ('\nMetar Non-Disponible\n')
                QNH = input('Altimetre? ')
                return('[VENTS]', QNH)


def affichage(position):
    print('')
    if position == '1':
        print('1. Delivery')
        print('9. Urgence')

    elif position == '2':
        print('1. Delivery')
        print('2. Sol')
        print('9. Urgence')

    elif position == '3':
        print('1. Delivery')
        print('2. Sol')
        print('3. Tour')
        print('9. Urgence')
    
    elif position == '4' or position == '5':
        print('1. Delivery')
        print('2. Sol')
        print('3. Tour')
        print('4. Departs')
        print('5. Approche')
        print('9. Urgence')
    
    elif position == '6':
        print('1. Delivery')
        print('2. Sol')
        print('3. Tour')
        print('4. Departs')
        print('5. Approche')
        print('6. Centre')
        print('9. Urgence')
    
    elif position == '7':
        print('0. FSS')

def remplirSquawk():
	for i in range(4001, 4778):
		boolean = True
		valid = list(str(i))
		for j in valid:
			if j == '8' or j == '9':
				boolean = False
				break
		if boolean == True:
			squawk.append(i)

def remplirDictionnaire(nomFichier, liste):
	fichier = open(nomFichier, "r")
	lines = fichier.readlines()
	values = []
	for i in lines:
		code, indicatif = i.split(",")
		indicatif = indicatif.split("\n")[0]
		values.append(code)
		values.append(indicatif)
		liste.append(values)
		values = []
	fichier.close()

def flightLevel():
	flight_level = True
	while flight_level == True:
		regle = input('Regle de vol? ')
		if regle.capitalize() == 'I':
			flight_level = '5000'
			return (flight_level, regle.capitalize())

		elif regle.capitalize() == 'V':
			flight_level = '1000'
			return (flight_level, regle.capitalize())

		elif regle.capitalize() == 'Y' or regle.capitalize() == 'Z':
			flight_level = 'CHECK'
			return (flight_level, regle.capitalize())
		
		elif regle == 'exit':
			flight_level = 'VOID'
			return (flight_level, regle.upper())

		else:
			print('Veuillez entrer selon les options suivantes:')
			print('I pour IFR')
			print('V pour VFR')
			print('Y pour IFR puis VFR')
			print('Z pour VFR puis IFR')


    
def afficherListeAvions():
	if len(listeAvions) == 0:
		print("\nAUCUN AVION DANS LA LISTE")
	else:
		print("\nIL Y A " + str(len(listeAvions)) + " AVION(S):")
		compteur = 1
		for i in listeAvions:
			print(str(compteur) + ". " + i[0] + ": " + str(i))
			compteur += 1

def assignerSquawk():
	value = []
	for i in squawk:
		chaineSquawk = list(str(i))
		if chaineSquawk[0] != '5':
			value = i
			break
	if value != None:
		indice = squawk.index(value)
		squawk[indice] += 1000
		return(value)
	else:
		print("ERREUR SQUAWK")

def rechercherIndicatif(code, liste):
	for i in liste:
		if code == i[0]:
			return(i[1])
	return(code)

def ajouterAvionArrivees():
    compagnie = input("Nom de la compagnie: ")
    numeroVol = input("Numero du vol: ")
    nom = compagnie + numeroVol

    while True:
        langue = input("Langue: ")
        if langue.upper() == "EN":
            remplirDictionnaire("dictionnaries/english/alphabet", anglais)
            break
        elif langue.upper() == "FR":
            remplirDictionnaire("dictionnaries/francais/alphabet", francais)
            break
        else:
            print('Sorry, this language is not covered yet')
            print('Please choose between english (EN) or french (FR)')

    destination = input("Destination: ")
    regle = ''
    while regle != 'I' and regle != 'V' and regle != 'Y' and regle != 'Z' and regle != 'EXIT':
        regle = input('Quelle est la regle de vol? ')
    if regle == 'EXIT':
        return()
    flightlevel = input('Niveau de vol? ')
    star = input("STAR: ")
    rwy = input("RWY: ")
    squawk = assignerSquawk()

    avion = []    
    avion.append(nom.upper())
    avion.append(langue.upper())
    avion.append(destination.upper())
    avion.append(regle.upper())
    avion.append(star.upper())
    avion.append(rwy.upper())
    avion.append(flightlevel)
    avion.append(squawk)
    avion.append(None)#clearance nulle
    
    listeAvions.append(avion)
    print("\nAJOUT DE L'AVION " + nom)

def ajouterAvionDepart(position):
    print("\n\n====================== NOUVEL AVION ======================\n")
    
    if position ==  '6' or position == '7':
        print("1. Depart")
        print("2. Arrivee")
        print('3. Transit')
        category = input('Quelle categorie? ')
        if category == '2':
            ajouterAvionArrivees()
        if category == '3':
            ajouterAvionTransit()
    compagnie = input("Nom de la compagnie: ")
    numeroVol = input("Numero du vol: ")
    nom = compagnie + numeroVol

    while True:
        langue = input("Langue: ")
        if langue.upper() == "EN":
            remplirDictionnaire("dictionnaries/english/alphabet", anglais)
            break
        elif langue.upper() == "FR":
            remplirDictionnaire("dictionnaries/francais/alphabet", francais)
            break
        else:
            print('Sorry, this language is not covered yet')
            print('Please choose between english (EN) or french (FR)')

    destination = input("Destination: ")
    (flightlevel, regle) = flightLevel()
    if regle == 'EXIT':
        return()
    sid = input("SID: ")
    rwy = input("RWY: ")
    squawk = assignerSquawk()

    avion = []    
    avion.append(nom.upper())
    avion.append(langue.upper())
    avion.append(destination.upper())
    avion.append(regle.upper())
    avion.append(sid.upper())
    avion.append(rwy.upper())
    avion.append(flightlevel)
    avion.append(squawk)
    avion.append(None)#clearance nulle
    
    listeAvions.append(avion)
    print("\nAJOUT DE L'AVION " + nom)


    
def ajouterAvionTransit():
    compagnie = input("Nom de la compagnie: ")
    numeroVol = input("Numero du vol: ")
    nom = compagnie + numeroVol

    while True:
        langue = input("Langue: ")
        if langue.upper() == "EN":
            remplirDictionnaire("dictionnaries/english/alphabet", anglais)
            break
        elif langue.upper() == "FR":
            remplirDictionnaire("dictionnaries/francais/alphabet", francais)
            break
        else:
            print('Sorry, this language is not covered yet')
            print('Please choose between english (EN) or french (FR)')
    
    depart = input('Quel est l\'aeroport de depart? ')
    destination = input("Destination? ")
    regle = ''
    while regle != 'I' and regle != 'V' and regle != 'Y' and regle != 'Z' and regle != 'EXIT':
        regle = input('Quelle est la regle de vol? ')
    if regle == 'EXIT':
        return()
    flightlevel = input('Niveau de vol? ')
    point = input('Point de rapport? ')
    squawk = assignerSquawk()

    avion = []    
    avion.append(nom.upper())
    avion.append(langue.upper())
    avion.append(depart.upper())
    avion.append(destination.upper())
    avion.append(regle.upper())
    avion.append(point.upper())
    avion.append(flightlevel)
    avion.append(squawk)
    avion.append(None)#clearance nulle
    
    listeAvions.append(avion)
    print("\nAJOUT DE L'AVION " + nom)

def supprimerAvion():
    if len(listeAvions) > 0:
        print("\n\n====================== SUPPRESSION ======================\n")
        avionSuppr = input("Quel avion veux-tu supprimer? ").upper()
        if avionSuppr != "":
            if avionSuppr.isdigit() == True:
#SUPPRESSION PAR INDEX
                if int(avionSuppr) > 0 and int(avionSuppr) <= len(listeAvions): 
                    avion = listeAvions[int(avionSuppr)-1]
                    squawkAvion = avion[7]+1000
                    for j in squawk:
                        if squawkAvion == j:
                            indice = squawk.index(j)
                            squawk[indice] -= 1000
                            break
                    listeAvions.remove(avion)

            else:
                avionPresent = False 
                indexAvion = [] 
                for i in listeAvions: 
                    if i[0] == avionSuppr: 
                        avionPresent = True 
                        indexAvion = i 
                        break 
                if avionPresent == True: 
                    squawkAvion = indexAvion[7]+1000 
                    for j in squawk: 
                        if squawkAvion == j: 
                            indice = squawk.index(j) 
                            squawk[indice] -= 1000 
                            break 
                    listeAvions.remove(indexAvion) 
                    print("\nSUPPRESSION DE L'AVION...")               

                print("\nSUPPRESSION DE L'AVION...")
        else:
            print("\nAVION INTROUVABLE...")
    else:
        print("\nAUCUN AVION A SUPPRIMER")


    
def AjouterClearance(avion,position):
    affichage(position)
    niveau = input('Quel niveau? ')
    if niveau == '1':
        delivery(avion)
    elif niveau == '2':
        ground(avion)
    elif niveau == '3':
        tower(avion)
    elif niveau == '4':
        departure(avion)
    elif niveau == '5':
        approach(avion)
    elif niveau == '6':
        center(avion)
    elif niveau == '7':
        fss(avion)
    elif niveau == '9':
        urgence(avion)

def delivery(avion):
    longueurNom = len(avion[0])
    langue = avion[1]
    regle = avion[3]
    nom = ""
    langueDico = []
    if langue == "EN":
        langueDico = anglais
    elif langue == "FR":
        langueDico = francais

    if regle == 'I' or regle == 'Y':
        nom = rechercherIndicatif(avion[0][:3], compagnies)+" "+avion[0][3:]
    elif regle == 'V'  or regle == 'Z':
        if avion[0].find('-') != -1:
            nom += rechercherIndicatif(avion[0][0], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-2], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-1], langueDico)
        else:
            for i in avion[0]:
                nom += rechercherIndicatif(i, langueDico)
                if avion[0].index(i) == len(avion[0])-1:
                    break
                nom += " "

    indicatifAeroport = rechercherIndicatif(avion[2], aeroports)
    sid = avion[4]
    rwy = avion[5]
    flightLevel = avion[6]
    squawk = str(avion[7])
    clearance = avion[8]
    clearance_txt = ""
    
    print('1. Clearance Initiale IFR')
    print('0. Sortie de ce menu')
    typeClearance = input('Quelle clearance veux-tu donner? ')
    if typeClearance == '1':
        if regle == 'I' or regle == 'Y':
            if langue == 'EN':
                clearance_txt = nom+' is cleared to '+indicatifAeroport+', via the '+sid+' departure, then planned route, expect runway '+rwy+', Initial climb '+flightLevel+', squawk '+squawk
            elif langue == 'FR':
                clearance_txt = nom+', depart vers '+indicatifAeroport+' approuve, depart via '+sid+', puis route prevue, piste '+rwy+' prevue , montee initiale '+flightLevel+', squawk '+squawk
            clearance = 'INIT'
            
            avion[8] = clearance
            print(clearance_txt)
            
        else:
            print('Les vols VFR ne sont pas inclus dans la tache des controleurs XXXX_DEL')
            
    elif typeClearance == '0':
        print('Sortie')
    
def ground(avion):
    (vents, altimetre) = meteo(aeroport_pos)
    longueurNom = len(avion[0])
    langue = avion[1]
    regle = avion[3]
    nom = ""
    langueDico = []
    if langue == "EN":
        langueDico = anglais
    elif langue == "FR":
        langueDico = francais

    if regle == 'I' or regle == 'Y':
        nom = rechercherIndicatif(avion[0][:3], compagnies)+" "+avion[0][3:]
    elif regle == 'V'  or regle == 'Z':
        if avion[0].find('-') != -1:
            nom += rechercherIndicatif(avion[0][0], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-2], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-1], langueDico)
        else:
            for i in avion[0]:
                nom += rechercherIndicatif(i, langueDico)
                if avion[0].index(i) == len(avion[0])-1:
                    break
                nom += " "

    rwy = avion[5]
    flightLevel = avion[6]
    squawk = str(avion[7])
    clearance = avion[8]
    clearance_txt = ""
    
    print('\n1. Push and start')
    print('2. Taxi depart')
    print('3. Taxi arrivees')
    print('4. Clearance initiale VFR')
    choix = input('Quelle clearance? ')
    
    if choix == '1':
        if langue == 'EN':
            clearance_txt = nom+', pushback and startup at your discretion, advise ready for taxi.'
        elif langue == 'FR':
            clearance_txt = nom + ' repoussage et demarrage a votre discretion, rappelez pret au taxi '

        clearance = 'PUSH'
        
    #Clearance Taxi
    elif choix == '2' or choix =='3':
        taxiRoute = input('Taxi? ')
        avion.append(taxiRoute)
        if choix == '2':
            if langue == 'EN':
                clearance_txt = nom+', runway '+rwy+', altimeter '+altimetre+ ', taxi '+taxiRoute+', hold short '+rwy+', report ready for takeoff'
    
            elif langue == 'FR':
                clearance_txt = nom + ', piste ' + rwy + ', altimetre ' + altimetre + ', taxi ' + taxiRoute + ", restez a l'ecart piste " + rwy + ', rappelez pret a decoller' 
        
        elif choix == '3':
            gate = input('Porte (Si non applicable, entrez 0 ')
            if gate != '0':
                if langue == 'EN':
                    clearance_txt = nom + ', taxi via ' + taxiRoute + ' to gate ' + gate
                elif langue == 'FR':
                    clearance_txt = nom + ', circulez via ' + taxiRoute + 'jusqu\'a la porte ' + gate
            
            elif gate == '0':
                if langue == 'EN':
                    clearance_txt = nom + ', taxi via ' + taxiRoute + ' to the gate'
                elif langue  == 'FR':
                    clearance_txt = nom + ', circulez via ' + taxiRoute + 'jusqu\'au parking '

    elif choix == '4':
        print('1. Vol VFR')
        print('2. Circuits')
        type = input('Type de vol? ')
        if type == '1':
            if langue == 'EN':
                clearance_txt = nom  + ', VFR [Intentions] approved, depart runway' + rwy + ', climb runway heading, not above ' + flightLevel + ' until advised, squawk ' + squawk
            elif langue == 'FR':
                clearance_txt = nom + ', [Intentions] VFR approuvees, piste ' + rwy + ', montez dans l\'axe de la piste, ne depassez pas ' + flightLevel + 'avant d\'etre autorise, affichez ' + squawk
        elif type == '2':
            if avion[5][-1:] == 'L':
                if langue == 'EN':
                    clearance_txt = nom + 'VFR circuits approved, runway ' + rwy + ' left hand circuits, not above ' + flightLevel + ', squawk ' + squawk 
                elif langue == 'FR':
                    clearance_txt = nom + ', Tours de pistes approuves, piste ' + rwy + ', tours de piste main gauche, ne depassez pas ' + flightLevel + ', squawk ' + squawk
            elif avion[5][-1:] == 'R':
                if langue == 'EN':
                    clearance_txt = nom + 'VFR circuits approved, runway ' + rwy + ' right hand circuits, not above ' + flightLevel + ', squawk ' + squawk 
                elif langue == 'FR':
                    clearance_txt = nom + ', Tours de pistes approuves, piste ' + rwy + ', tours de piste main droite, ne depassez pas ' + flightLevel + ', squawk ' + squawk
            else:
                print('Veuillez verifier la piste ')
        clearance = 'INIT'
    print (clearance_txt)
    avion[8] = clearance

def tower(avion):
    longueurNom = len(avion[0])
    langue = avion[1]
    regle = avion[3]
    nom = ""
    langueDico = []
    if langue == "EN":
        langueDico = anglais
    elif langue == "FR":
        langueDico = francais

    if regle == 'I' or regle == 'Y':
        nom = rechercherIndicatif(avion[0][:3], compagnies)+" "+avion[0][3:]
    elif regle == 'V'  or regle == 'Z':
        if avion[0].find('-') != -1:
            nom += rechercherIndicatif(avion[0][0], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-2], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-1], langueDico)
        else:
            for i in avion[0]:
                nom += rechercherIndicatif(i, langueDico)
                if avion[0].index(i) == len(avion[0])-1:
                    break
                nom += " "

    rwy = avion[5]
    clearance = avion[8]
    clearance_txt = ""
    print('1. Line-Up')
    print('2. Take-off')
    print('3. Atterissage')
    print('4. Clearances VFR')
    print('5. Manoeuvres VFR')
    typeClearance = input('Quelle clearance veux-tu donner? ')
    
    if typeClearance == '1':
        if langue == 'EN':
            clearance_txt = nom+' line up and wait runway '+rwy

        elif langue == 'FR':
            clearance_txt = nom+' alignez-vous piste '+rwy+' et attendez'

        clearance = 'LNUP'

    #Clearance Decollage
    elif typeClearance == '2':
        (vents, altimetre) = meteo(aeroport_pos)
        if regle == 'I' or regle == 'Y' or regle == 'Z':
            ATC = choisirATC()
            if langue == 'EN' :
                clearance_txt = nom+' contact '+ATC[1]+' on '+ATC[3]+' airborne, cleared for takeoff runway '+rwy

            elif langue == 'FR':
                clearance_txt = nom + ', contactez '+ATC[2]+' sur ' + ATC[3] + ' en vol, autorise decollage piste ' + rwy

        elif regle == 'V':
            if rwy == '06R' or rwy == '24R':        #A MODIFIER POUR AUTRES AEROPORTS. DICTIONNAIRE?
                if langue == 'EN':
                    clearance_txt = nom+ ' report right hand downwind runway '+rwy+', cleared for takeoff, winds '+vents

                elif langue == 'FR':
                    clearance_txt = nom+ ' rappelez downwind main droite '+rwy+', autorise decollage, vents '+vents

            elif rwy == '06L' or rwy == '24L':
                if langue == 'EN':
                    clearance_txt = nom + ' report left hand downwind runway '+rwy+', cleared for takeoff, winds '+vents

                elif langue == 'FR':
                    clearance_txt = nom+ ' rappelez downwind main gauche '+rwy+', autorise decollage, vents '+vents

        clearance = 'TKOF'
    #Atterissage
    elif typeClearance == '3':
        sortie = input('Quelle sortie? ')
        if langue == 'EN':
            clearance_txt = nom + ', winds '+vents+', exit at ' + sortie + ', cleared to land runway ' + rwy

        elif langue  == 'FR':
            clearance_txt = nom + ', vents '+vents+', sortez a ' +  sortie + ', autorise a atterir piste ' + rwy
        clearance = 'LDG'+rwy
    #Clearance leg VFR
    elif typeClearance == '3':
        if regle == 'I' or regle == 'Y':
            print('Non disponible pour les vols IFR')
            return()

        elif regle == 'V' or 'Z':
            print ('1. Circuit')
            print ('2. Arrivees')
            position = input('Quelle position? ')

            if position == '1':
                print ('1. Rappelez fin de downwind')
                print ('2. Downwind -> Finale')
                print ('3. Allongez Downwind ')
                position2 = input('Quelle clearance? ')

                #Report end of downwind
                if position2 == '1':
                    if langue == 'EN':
                        clearance_txt = nom + ', report end of downwind runway ' + rwy

                    elif langue == 'FR':
                        clearance_txt = nom + ', rappelez fin de downwind piste ' + rwy

                    clearance = 'DWND'

                #Downwind -> Final
                elif position2 == '2':
                    numero = input('Numero en approche? ')
                    if langue == 'EN':
                        clearance_txt = nom + ', report on final runway ' +rwy+', number ' + numero
                    elif langue == 'FR':
                        clearance_txt = nom + ', report on final runway ' + rwy + ', numero ' + numero

                    clearance = 'FINL'

                #Extend Downwind
                elif position2 == '3':
                    numero = input('Numero en approche? ')
                    if langue == 'EN':
                        clearance_txt = nom + ', extend downwind, number ' + numero + ', 4 miles final runway ' + rwy
                    elif langue  == 'FR':
                        clearance_txt = nom + ', allongez downwind, numero ' + numero + ', finale 4 nautiques piste ' + rwy
                    clearance = 'EXTD'

            if position == '2':
                (vents, altimetre) = meteo(aeroport_pos)
                print ('1. approche straight-in')
                print ('2. fin de downwind')
                print ('3. VFR entry-point')
                position2 = input('Quelle clearance? ')

                #Approche Straight-In
                if position2 == '1':
                    if langue == 'EN':
                        clearance_txt = nom + ', make straight-in approach runway ' + rwy + ', winds '+vents+', altimeter ' + altimetre
                    elif langue == 'FR':
                        clearance_txt = nom + ', faites une approche directe piste ' + rwy + ', vents '+vents+', altimetre ' + altimetre
                    clearance = 'APPR'

                #Fin de downwind
                elif position2 == '2':
                    numero = input('Numero en approche? ')
                    if langue == 'EN':
                        clearance_txt = nom + ', report on final runway ' + rwy + ', number ' + numero
                    elif langue == 'FR':
                        clearance_txt = nom + ', rappelez en finale piste ' + rwy + ', numero ' + numero
                    clearance = 'FINL'

                #VFR entry point
                elif position == '3':
                    print ("1. Arrive de l'est")
                    print ("2. Arrive de l'ouest")
                    cote = input('Quel cote? ')	
                    if cote == '1':
                        if rwy == '06R' or rwy == '24R':
                            if langue == 'EN':
                                clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind '+vents+', altimeter ' + altimetre
                            elif langue == 'FR':
                                clearance_txt = nom + ', rejoignez downwind main gauche ' + rwy + ', vents '+vents+', altimetre ' + altimetre

                            clearance = 'LHDW'

                        elif rwy == '24L' or rwy == '24L':
                            if langue == 'EN':
                                clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind '+vents+', altimeter ' + altimetre
                            elif langue == 'FR':
                                clearance_txt = nom + ', rejoignez downwind main gauche piste ' + rwy + ', vents '+vents+', altimetre ' + altimetre
                            clearance = 'RHDW'

                    elif cote == '2':
                        if rwy == '06R' or rwy == '24R':
                            if langue == 'EN':
                                clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind '+vents+', altimeter ' + altimetre
                            clearance = 'RHDW'

                        elif rwy == '24L' or rwy == '06L':
                            if langue == 'EN':
                                clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind '+vents+', altimeter ' + altimetre
                            elif langue == 'FR':
                                clearance_txt = nom + ', rejoignez downwind main gauche ' + rwy + ', vents '+vents+', altimetre ' + altimetre
                            clearance = 'LHDW'


    #Clearances d'approche
    elif typeClearance == '7':
        print ('1. Touch and go')
        print ('2. Low pass')
        print ('3. Stop and go')
        print ('4. Go around')
        operation = input('Quelle operation? ')

        #Touch and Go	
        if operation == '1':
            if langue == 'EN':
                clearance_txt = nom + ', runway ' + rwy + ', cleared touch and go, winds '+vents
            elif langue == 'FR':
                clearance_txt = nom + ', piste ' + rwy + ', autorise toucher, vents '+vents
            clearance = 'T&GO'

        #Low Pass
        elif operation == '2':
            if langue == 'EN':
                clearance_txt = nom + ', cleared low pass runway ' + rwy + ', winds '+vents
            elif langue == 'FR':
                clearance_txt = nom + ', autorise low pass piste ' + rwy + ', winds '+vents
            clearance = 'LOWP'

        #Stop and Go
        elif operation == '3':
            if langue == 'EN':
                clearance_txt = nom + ', cleared to land runway ' + rwy + ', winds '+vents+' \n Report ready for take-off -> Donner clearance Takeoff'
            if langue == 'FR':
                clearance_txt = nom + ', autorise a atterir piste ' + rwy + ', vents '+vents+' \n Rappelez pret a decoller -> Donner clearance Takeoff'
            clearance = 'S&GO'

        #Go-Around	
        elif operation == '4':
            print ('1. Initie par ATC')
            print ('2. Initie par pilote')
            personne = input('Qui a initie le Go-Around? ')
            if personne == '1':
                raison = input('Raison? ')
                if langue == 'EN':
                    clearance_txt = nom + ', go around, ' + raison
                elif langue == 'FR':
                    clearance_txt = nom + ', remettez les gaz, ' + raison 

            elif personne == '2':
                clearance_txt = nom + ', roger'
            clearance = 'G-A'

    elif typeClearance == '8':
        ATC = choisirATC()
        print ('1. Decollage -> point')
        print ('2. Sortie zone de controle')
        maniere = input('Quelle clearance? ')
        if maniere == '1':
            point = input('Quel est le point de rapport? ')
            if langue == 'EN':
                clearance_txt = nom + ', report over ' + point + ', runway ' + rwy + ', cleared for takeoff, winds '+vents
            elif langue == 'FR':
                clearance_txt = nom + ', rappelez a ' + point + ', piste ' +rwy+ ', autorise decollage, vents '+vents
            clearance = 'TOPT'

        elif maniere == '2':
            if langue == 'EN':
                clearance_txt = nom + ', frequency change approved, Contact '+ATC[1]+' on ' + ATC[3] +', good day!'
            elif langue == 'FR':
                clearance_txt = nom + ', changement de frequence approuve, contactez '+ATC[2]+' sur '+ATC[3]+', Bon vol!'
  
        clearance = 'EXIT'
    print (clearance_txt)
    avion[8] = clearance

def departure(avion):
    print('Cette section n\'existe pas encore')

def approach(avion):
    print('Cette section n\'existe pas encore')
    
def center(avion):
    print("Cette section n'existe pas encore")

def fss(avion):
    print("Cette section n'existe pas encore")

def urgence(avion):
    longueurNom = len(avion[0])
    langue = avion[1]
    regle = avion[3]
    nom = ""
    langueDico = []
    if langue == "EN":
        langueDico = anglais
    elif langue == "FR":
        langueDico = francais

    if regle == 'I' or regle == 'Y':
        nom = rechercherIndicatif(avion[0][:3], compagnies)+" "+avion[0][3:]
    elif regle == 'V'  or regle == 'Z':
        if avion[0].find('-') != -1:
            nom += rechercherIndicatif(avion[0][0], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-2], langueDico) + " "
            nom += rechercherIndicatif(avion[0][longueurNom-1], langueDico)
        else:
            for i in avion[0]:
                nom += rechercherIndicatif(i, langueDico)
                if avion[0].index(i) == len(avion[0])-1:
                    break
                nom += " "
                
    print ('1. PAN PAN' )
    print ('2. MAYDAY MAYDAY')
    urgence = input('Quelle urgence? ')
    if urgence == '1':
        urgence = 'PAN PAN'
        clearance = 'PAN PAN'
    elif urgence == '2':
        urgence = 'MAYDAY'
        clearance = 'MAYDAY'
    UTC = datetime.utcnow().strftime('%H:%M')

    if langue == 'EN':
        clearance_txt = nom + ', Roger ' + urgence + ' at time ' + UTC + 'z'
    elif langue == 'FR':
        clearance_txt = nom + ', Compris ' + urgence + ' recue a ' + UTC + 'z'
    print (clearance_txt)
    avion[8] = clearance

def AvionClearance():
    if len(listeAvions) > 0:
        platforme(platform)
        while True:
            affichermeteo(aeroport_pos)
            print("\n\n================== CLEARANCE ==================\n")
            afficherListeAvions()
            avionClearance = input("\nA quel avion veux-tu donner une clearance? ").upper()
            if avionClearance != "":
                if avionClearance.isdigit() == True:
                    if int(avionClearance) > 0 and int(avionClearance) <= len(listeAvions): 
                        avion = listeAvions[int(avionClearance)-1]
                        AjouterClearance(avion,position) 
                        break
                
                elif avionClearance.upper() == 'EXIT':
                    break
                
                else:
                    for i in listeAvions:
                        if i[0] == avionClearance:
                            avionPresent = True
                            indexAvion = i
                            break
                    if avionPresent == True:
                        AjouterClearance(indexAvion,position)
                        break
                    else:
                        print('AVION INTROUVABLE')
            else:
                print('VEUILLEZ ENTRER UN AVION')
    else:
        print ('AUCUN AVION DANS LA LISTE')

def modifierAvion(avion, position):
    print('1. Changer la langue')
    print('2. Changer la destination')
    print('3. Changer la regle de vol')
    print('4. Changer la SID')
    print('5. Changer la piste)' )
    print('6. Changer l\' altitude')
    ObjetModif = input('Quelle modification veux-tu faire? ')
    if ObjetModif == '1':
        while True:
            langue = input('Quelle langue? ')
            if langue.upper() == "EN":
                remplirDictionnaire("../dictionnaries/english/alphabet", anglais)
                break
            elif langue.upper() == "FR":
                remplirDictionnaire("../dictionnaries/francais/alphabet", francais)
                break
            else:
                print('Sorry, this language is not covered yet')
                print('Please choose between english (EN) or french (FR)')
        avion[1] = langue.upper()
    
    elif ObjetModif =='2':
        destination = input('Quelle est la destination? ')
        avion[2] = destination
    
    elif ObjetModif == '3':
        regle = ''
        while regle != 'I' and regle != 'V' and regle != 'Y' and regle != 'Z':
            regle = input('Regle? ')
            if regle != 'I' and regle != 'V' and regle != 'Y' and regle != 'Z':
                print('Cette option n\'est pas valide, veuillez recommencer')
            else:
                avion[3] = regle
    
    elif ObjetModif == '4':
        sid = input('SID? ').upper()
        avion[4] = sid
    
    elif ObjetModif == '5':
        while True:
            piste = input('Quelle piste? ')
            if piste[:2].replace('0' ,  '').isdigit() == True:
                if int(piste.replace('0' ,  '')[:2]) > 1 and int(piste.replace('0' ,  '')[:2]) <= 36:
                    avion[5] = piste.upper()
                    break
                else:'Veuillez entrer un numero de piste valide'
            else:'Veuillez entrer un numero de piste valide'
    
    elif ObjetModif == '6':
        level = input('Altitude')
        if len(level) == 3:
            altitude = 'FL' + level
        avion[6] = altitude

def choisirAvion():
    if len(listeAvions) > 0:
        platforme(platform)
        while True:
            print("\n\n================== MODIFICATION AVION ==================\n")
            afficherListeAvions()
            avionModif = input("\nA quel avion veux-tu modifier? ").upper()
            if avionModif != "":
                if avionModif.isdigit() == True:
                    if int(avionModif) > 0 and int(avionModif) <= len(listeAvions): 
                        avion = listeAvions[int(avionModif)-1]
                        modifierAvion(avion,position) 
                        break
                
                elif avionModif.upper() == 'EXIT':
                    break
                
                else:
                    for i in listeAvions:
                        if i[0] == avionModif:
                            avionPresent = True
                            indexAvion = i
                            break
                    if avionPresent == True:
                        modifierAvion(indexAvion,position)
                        break
                    else:
                        print('AVION INTROUVABLE')
            else:
                print('VEUILLEZ ENTRER UN AVION')
    else:
        print ('AUCUN AVION DANS LA LISTE')
    
def choisirATC():
    if len(listeATC) > 0:
        platforme(platform)
        while True:
            print("\n\n================== CHOIX ATC ==================\n")
            afficherListeATC()
            print('POUR AJOUTER UN ATC VEUILLEZ TAPER "ATC"')
            ATCClearance = input("\nQuel ATC veux-tu choisir pour la clearance ").upper()
            if len(ATCClearance) != 0:
                if ATCClearance.isdigit() == True:
                    if int(ATCClearance) > 0 and int(ATCClearance) <= len(listeATC): 
                        ATC = listeATC[int(ATCClearance)-1]
                        return ATC
    
                elif ATCClearance == 'ATC' :
                    ajouterATC()

                else:
                    ATCPresent = False
                    indexATC = []
                    for i in listeATC:
                        if i[0] == ATCClearance:
                            ATCPresent = True
                            indexATC = i
                            break
                    if ATCPresent == True:
                        return indexATC
                        break
                    else:
                        print("\nATC INTROUVABLE...")
                        input(' ')
                        platforme(platform)
            else:
                ajouterATC()
    else:
        print("\nAUCUN ATC DANS LA LISTE")        

def ajouterATC():
    while True:
        print ("\n\n====================== NOUVEL ATC ======================\n")
        print("0. QUITTER CE MENU")
        print ('1. Aerodrome')
        print ('2. FIR / ARTCC')
        print ('3. FIR oceanique')
        type = input ('Quel type? ')
        emplacement_en = []
        emplacement_fr = []
        if type == '1':
            remplirDictionnaire("dictionnaries/airport-radio", emplacement_en)
            remplirDictionnaire("dictionnaries/airport-radio",  emplacement_fr)
            break
        elif type == '2':
            remplirDictionnaire("dictionnaries/english/ATC/FIR", emplacement_en)
            remplirDictionnaire('dictionnaries/francais/ATC/FIR', emplacement_fr)
            break
        elif type == '3':
            remplirDictionnaire("dictionnaries/english/ATC/OCEANIC", emplacement_en)
            remplirDictionnaire("dictionnaries/francais/ATC/OCEANIQUE",  emplacement_fr)
            break
            
        elif type == '0':
            break
            
        else:
            print ('CE CHOIX N\'EST PAS VALIDE')
    if type == '0':
        return()

    estPresent = False
    while True:
        endroitCode = input("Endroit? (XXXX): ").upper()
        if len(endroitCode) == 4:
            for i in emplacement_en:
                for j in emplacement_fr:
                    if j[0] == endroitCode.upper():
                        endroit_fr = j[1]
                        estPresent = True
                        break
                    if estPresent == True:
                        break
                if i[0] == endroitCode.upper():
                    endroit_en = i[1]
                    estPresent = True
                    break
            if estPresent == True:
                break
            else:
                endroit_en = endroitCode.upper()
                endroit_fr = endroitCode.upper()
                break
                
        else:
            print("ENDROIT INEXISTANT\n")
        
    positions_en = []
    positions_fr = []

    remplirDictionnaire("dictionnaries/english/ATC/positions", positions_en)
    remplirDictionnaire("dictionnaries/francais/ATC/postes",  positions_fr)
    estPresentPosition = False
    if type == '1' :
        while True:
            positionRole= input("Role? (XXX): ").upper()
            if len(positionRole) == 3 or positionRole.upper() == 'ATIS':
                for i in positions_en:
                    for j in positions_fr:
                        if j[0] == positionRole.upper() :
                            role_fr = j[1]
                            estPresentPosition = True
                            break
                        if estPresentPosition == True:
                            break
                    if i[0] == positionRole.upper() :
                        role_en = i[1]
                        estPresentPosition = True
                        break
                if estPresentPosition == True:
                    break
            print("ROLE INEXISTANT\n")
            
    elif type == '2':
        positionRole = 'CTR'
        
    elif type == '3':
        while True:
            print ('1. XXXX_OCE')
            print('2. XXX_FSS')
            role = input('Quel poste? ')
            if role == '1':
                positionRole = 'OCE'
                break
            elif role =='2':
                positionRole = 'FSS'
                break
            
    code = endroitCode + '_' + positionRole
    if type == '1':
        nom_en = endroit_en + ' ' + role_en
        nom_fr = endroit_fr + ' '+ role_fr
    elif type == '2' or type == '3':
        nom_en = endroit_en
        nom_fr = endroit_fr 

    ATC = []    
    ATC.append(code)
    ATC.append(nom_en)
    ATC.append(nom_fr)
    ATC.append(ATCFrequency())

    listeATC.append(ATC)
    print("\nAJOUT DE L'ATC " + code)

def ATCFrequency():
    while True:
        frequency = input('Quelle est la frequence de l\'ATC? ').replace(',', '.')
        if frequency.replace('.', '').isdigit:
            if float(frequency) > 117.975 and float(frequency) < 137.00 and float(frequency) != 121.5 :
                return frequency
        else:
            print('LA FREQUENCE N\'EST PAS VALIDE, VEUILLEZ RECOMMENCER')

def afficherListeATC():
    if len(listeATC) == 0:
        print("\nAUCUN ATC DANS LA LISTE")
    else:
        print("\nIL Y A " + str(len(listeATC)) + " ATC:")
        compteur = 1
        for i in listeATC:
            print(str(compteur) + ". " + i[0] + ": " + str(i))
            compteur += 1

	#SUPPRIMER UN ATC
def supprimerATC():
    if len(listeATC) > 0:
        while True:
            print("\n\n====================== SUPPRESSION ======================\n")
            ATCSuppr = input("QUEL ATC VEUX-TU SUPPRIMER?\n0 POUR SORTIR DU MENU ").upper()
            if ATCSuppr != "":
                if ATCSuppr.isdigit() == True and int(ATCSuppr) != 0:
                    if int(ATCSuppr) > 0 and int(ATCSuppr) <= len(listeATC): 
                        ATC = listeATC[int(ATCSuppr)-1]
                        listeATC.remove(ATC)
                        break
                    
                    else:
                        print('ATC INCONNU')
                
                elif ATCSuppr == '0':
                    break
                
                else:
                    ATCPresent = False
                    indexATC = []
                    for i in listeATC: 
                        if i[0] == ATCSuppr:
                            ATCPresent = True
                            indexATC = i 
                            break
                    if  ATCPresent == True:
                        listeATC.remove(indexATC) 
                        print("\nSUPPRESSION DE L'ATC...")
                        break
                    else:
                        print('ATC INEXISTANT')
            else:
                print('\nVEUILLEZ ENTRER UN ATC')
    else:
        print ('IL N\'Y A PAS D\'ATC DANS LA LISTE')
def atc():
    afficherListeATC()
    print ('\n1, Ajouter un ATC ')
    print ('2. Supprimer un ATC')
    option = input('Quelle option veux-tu choisir? ')
    if option == '1':
        ajouterATC()
    elif option == '2':
        supprimerATC()

def UNICOM():
    ATC = []    
    ATC.append('UNICOM')
    ATC.append('UNICOM')
    ATC.append('UNICOM')
    ATC.append('122.8')
    listeATC.append(ATC)

#### ===== ----- ===== ----- ===== ----- ===== ----- PROGRAMME PRINCIPAL ----- ===== ----- ===== ----- ===== ----- =====  ####
(position,aeroport_pos) = position()
remplirSquawk()
remplirDictionnaire("dictionnaries/companies", compagnies)
remplirDictionnaire("dictionnaries/airports", aeroports)
UNICOM()

while True:
    metar = []
    print("\n\n================== PROGRAMME PRINCIPAL ==================\n")
    affichermeteo(aeroport_pos)
    afficherListeAvions()
    print("\n1. Ajouter un avion")
    print("2. Ajouter clearance a un avion")
    print("3. Supprimer un avion")
    print("4. ATC / Frequences")
    print('5. Modifier un avion')
    print("6. Quitter")
    choix = input("Que veux-tu faire? ")

    #AJOUTER UN AVION
    if choix == '1':
        ajouterAvionDepart(position)

    #AJOUTE CLEARANCE A UN AVION
    elif choix == '2':
        AvionClearance()
    
    #SUPPRIMER UN AVION   
    elif choix == '3':
        supprimerAvion()

    #Modifier ATC
    elif choix == '4':
        atc()
        
    elif choix == '5':
        choisirAvion()
        
    #QUITTER
    elif choix == '6':
        quitter = input("Voulez vous vraiment quitter? (Y / N) ")
        if quitter == 'Y' or quitter == 'y':
            print("\nEXIT")
            break
        
    #CHOIX INEXISTANT
    else:
        print("\nCHOIX INEXISTANT")
        
    input('')
    platforme(platform)
