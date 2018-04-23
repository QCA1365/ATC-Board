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
	aeroport_pos = input('Quel est le code OACI de l\'aeroport / de la FIR? ') 
	while position != '1' and position != '2' and position != '3' and position != '4' and position != '5' and position != '6':
		print ('1. XXXX_DEL')
		print ('2. XXXX_GND')
		print ('3. XXXX_TWR')
		print ('4. XXXX_DEP')
		print ('5. XXXX_APP')
		print ('6. XXXX_CTR')
		position = input('Quelle position? ')
	return (position, aeroport_pos)

(position,aeroport_pos) = position()

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

def affichermeteo(aeroport_pos):
    metar = getMETAR(aeroport_pos)
    if metar.upper() == metar:
        print (metar.replace("\n", ""))

    else:
        print ('\nMetar Non-Disponible\n')

def meteo(aeroport_pos):
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


def affichage(position):
    if position == '1':
        print('1. Clearance initiale')
        print('9. Urgence')

    elif position == '2':
        print('1. Clearance initiale')
        print('2. Push et demarrage')
        print('3. Taxi')
        print('9. Urgence')

    elif position == '3' or position == '4'or position == '5' or  position == '6' :
        print('1. Clearance initiale')
        print('2. Push et demarrage')
        print('3. Taxi')
        print('4. Line-up')
        print('5. Takeoff')
        print('6. Leg VFR')
        print('7. Landing')
        print('8. Depart espace aerien VFR')
        print('9. Urgence')
    else:
        print("La position n'est pas valide; veuillez redemarrer.")

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

def ajouterAvion():
	print("\n\n====================== NOUVEL AVION ======================\n")

	compagnie = input("Nom de la compagnie: ")
	numeroVol = input("Numero du vol: ")
	nom = compagnie + numeroVol

	langue = input("Langue: ")
	if langue.upper() == "EN":
		remplirDictionnaire("dictionnaries/english/alphabet", anglais)
	elif langue.upper() == "FR":
		remplirDictionnaire("dictionnaries/francais/alphabet", francais)
		
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


    
def supprimerAvion():
	if len(listeAvions) > 0:
		print("\n\n====================== SUPPRESSION ======================\n")

		avionSuppr = input("Quel avion veux-tu supprimer? ").upper()
		if avionSuppr != "":

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
				print("\nSUPPRESSION DE L'AVION...")

			else:
				print("\nAVION INTROUVABLE...")

			#SUPPRESSION PAR CALLSIGN
			"""else:
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
					print("\nSUPPRESSION DE L'AVION...")"""

		else:
			print("\nAVION INTROUVABLE...")
	
	else:
		print("\nAUCUN AVION A SUPPRIMER")


    
def creerClearance(avion,position):
    affichermeteo(aeroport_pos)
    affichage(position)
    typeClearance = input('Quelle clearance veux-tu donner? ')
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

    if regle == 'I' or regle == 'Y' or regle == 'Z':
        nom = rechercherIndicatif(avion[0][:3], compagnies)+" "+avion[0][3:]
    elif regle == 'V':
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

    destination = avion[2]
    indicatifAeroport = rechercherIndicatif(avion[2], aeroports)

    sid = avion[4]
    rwy = avion[5]
    flightLevel = avion[6]
    squawk = str(avion[7])
    clearance = avion[8]
    clearance_txt = ""

    if typeClearance == '1':
        if regle == 'I' or regle == 'Y':
            if langue == 'EN':
                clearance_txt = nom+' is cleared to '+indicatifAeroport+', via the '+sid+' departure, then planned route, expect runway '+rwy+', Initial climb '+flightLevel+', squawk '+squawk
            elif langue == 'FR':
                clearance_txt = nom+', depart vers '+indicatifAeroport+' approuve, depart via '+sid+', puis route prevue, piste '+rwy+' prevue , montee initiale '+flightLevel+', squawk '+squawk
            clearance = 'INIT'

		#Clearance Initiale + Taxi VFR
        elif regle == 'V' or regle == 'Z':
            taxiRoute = input('Taxi? ')
            avion.append(taxiRoute)
            if destination == 'CYUL':
                if rwy == '24L' or rwy == '06L': 
                    if langue == 'EN':
                        clearance_txt = nom+', right hand pattern '+flightLevel+', squawk '+squawk+' taxi holding point runway '+rwy+' via '+taxiRoute
                    elif langue == 'FR':
                        clearance_txt = nom+', tour de piste main droite a '+flightLevel+' pieds, squawk '+squawk+" taxi point d'arret piste "+rwy+' via '+taxiRoute 
                elif rwy == '06R' or rwy  == '24R':
                    if langue == 'EN':
                        clearance_txt = nom+', left hand pattern '+flightLevel+', squawk '+ squawk+'taxi holding point runway '+rwy+' via '+taxiRoute

                    elif langue == 'FR':
                        clearance_txt = nom+', tour de piste main gauche a '+flightLevel+' pieds, squawk '+squawk+" taxi point d'arret piste "+rwy+' via '+taxiRoute 
            else:
                if langue == 'EN':
                    clearance_txt = nom+' initial climb '+flightLevel+', squawk '+squawk+', taxi holding point runway '+rwy+' via '+taxiRoute+', hold short '+rwy+', report ready for takeoff'
                elif langue == 'FR':
                    clearance_txt = nom + ', montee initiale ' + flightLevel + ', squawk ' + squawk + ", roulez point d'arret piste "+ rwy + ' via ' + taxiRoute + "restez a l'ecart piste " + rwy + ', rappelez pret a decoller '
            clearance = 'TAXI'

	#Clearance Push + Start
    elif typeClearance == '2':
        if langue == 'EN':
            clearance_txt = nom+', pushback and startup at your discretion, advise ready for taxi.'

        elif langue == 'FR':
            clearance_txt = nom + ' repoussage et demarrage a votre discretion, rappelez pret au taxi '

        clearance = 'PUSH'

	#Clearance Taxi
    elif typeClearance == '3':
        taxiRoute = input('Taxi? ')
        avion.append(taxiRoute)
        if langue == 'EN':
            clearance_txt = nom+', runway '+rwy+', altimeter '+altimetre+ ', taxi '+taxiRoute+', hold short '+rwy+', report ready for takeoff'

        elif langue == 'FR':
            clearance_txt = nom + ', piste ' + rwy + ', altimetre ' + altimetre + ', taxi ' + taxiRoute + ", restez a l'ecart piste " + rwy + ', rappelez pret a decoller' 

        clearance = 'TAXI'

	#Clearance Line-up
    elif typeClearance == '4':
        if langue == 'EN':
            clearance_txt = nom+' line up and wait runway '+rwy

        elif langue == 'FR':
            clearance_txt = nom+' alignez-vous piste '+rwy+' et attendez'

        clearance = 'LNUP'

	#Clearance Decollage
    elif typeClearance == '5':
        if regle == 'I' or regle == 'Y' or regle == 'Z':
            ATC = choisirATC()
            if langue == 'EN' :
                clearance_txt = nom+' contact '+ATC[1]+' on '+ATC[3]+' airborne, cleared for takeoff runway '+rwy

            elif langue == 'FR':
                clearance_txt = nom + ', contactez '+ATC[2]+' sur ' + ATC[3] + ' en vol, autorise decollage piste ' + rwy

        elif regle == 'V':
            if rwy == '06R' or rwy == '24R':
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

	#Clearance leg VFR
    elif typeClearance == '6':
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
        print ('1. Atterissage')
        print ('2. Touch and go')
        print ('3. Low pass')
        print ('4. Stop and go')
        print ('5. Go around')
        operation = input('Quelle operation? ')

		#Atterissage
        if operation == '1':
            sortie = input('Quelle sortie? ')
            if langue == 'EN':
                clearance_txt = nom + ', winds '+vents+', exit at ' + sortie + ', cleared to land runway ' + rwy

            elif langue  == 'FR':
                clearance_txt = nom + ', vents '+vents+', sortez a ' +  sortie + ', autorise a atterir piste ' + rwy
            clearance = 'LDG'+rwy

		#Touch and Go	
        elif operation == '2':
            if langue == 'EN':
                clearance_txt = nom + ', runway ' + rwy + ', cleared touch and go, winds '+vents
            elif langue == 'FR':
                clearance_txt = nom + ', piste ' + rwy + ', autorise toucher, vents '+vents
            clearance = 'T&GO'

		#Low Pass
        elif operation == '3':
            if langue == 'EN':
                clearance_txt = nom + ', cleared low pass runway ' + rwy + ', winds '+vents
            elif langue == 'FR':
                clearance_txt = nom + ', autorise low pass piste ' + rwy + ', winds '+vents
            clearance = 'LOWP'

		#Stop and Go
        elif operation == '4':
            if langue == 'EN':
                clearance_txt = nom + ', cleared to land runway ' + rwy + ', winds '+vents+' \n Report ready for take-off -> Donner clearance Takeoff'
            if langue == 'FR':
                clearance_txt = nom + ', autorise a atterir piste ' + rwy + ', vents '+vents+' \n Rappelez pret a decoller -> Donner clearance Takeoff'
            clearance = 'S&GO'

		#Go-Around	
        elif operation == '5':
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

    elif typeClearance == '9':
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

        #MENU LEG ICI
    print("\n"+clearance_txt)
    if clearance != "TAXI":
        if len(avion) > 9:
            avion.remove(avion[9])
    avion[8] = clearance

def ajouterClearance():
	if len(listeAvions) > 0:
		platforme(platform)
		while True:
			print("\n\n================== CLEARANCE ==================\n")
			afficherListeAvions()
			avionClearance = input("\nA quel avion veux-tu ajouter une clearance? ").upper()
			avionPresent = False
			indexAvion = []
			for i in listeAvions:
				if i[0] == avionClearance:
					avionPresent = True
					indexAvion = i
					break
			if avionPresent == True:
				creerClearance(indexAvion,position)
				break
			else:
				print("\nAVION INTROUVABLE...")
				input(' ')
				platforme(platform)
	else:
		print("\nAUCUN AVION DANS LA LISTE")

def choisirATC():
    if len(listeATC) > 0:
        platforme(platform)
        while True:
            print("\n\n================== CHOIX ATC ==================\n")
            afficherListeATC()
            ATCClearance = input("\nQuel ATC veux-tu choisir pour la clearance ").upper()
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
        print("\nAUCUN ATC DANS LA LISTE")        

def ajouterATC():
    print ("\n\n====================== NOUVEL ATC ======================\n")
    print ('1. Aerodrome')
    print ('2. FIR / ARTCC')
    print ('3. FIR oceanique')
    type = input ('Quel type? ')
    emplacement_en = []
    emplacement_fr = []
    if type == '1':
        remplirDictionnaire("dictionnaries/airport-radio", emplacement_en)
        remplirDictionnaire("dictionnaries/airport-radio",  emplacement_fr)
    elif type == '2':
        remplirDictionnaire("dictionnaries/english/FIR", emplacement_en)
        remplirDictionnaire('dictionnaries/francais/FIR', emplacement_fr)
    elif type == '3':
        remplirDictionnaire("dictionnaries/english/OCEANIC", emplacement_en)
        remplirDictionnaire("dictionnaries/francais/OCEANIQUE",  emplacement_fr)

    estPresent = False
    while True:
        endroitCode = input("Endroit? (XXXX): ")
        if len(endroitCode) == 4:
            for i in emplacement_en:
                for j in emplacement_fr:
                    if j[0] == endroitCode:
                        endroit_fr = j[1]
                        estPresent = True
                        break
                    if estPresent == True:
                        break
                if i[0] == endroitCode:
                    endroit_en = i[1]
                    estPresent = True
                    break
            if estPresent == True:
                break
            else:
                endroit_en = endroitCode
                endroit_fr = endroitCode
                break
                
        else:
            print("ENDROIT INEXISTANT\n")
        
    positions_en = []
    positions_fr = []

    remplirDictionnaire("dictionnaries/english/positions", positions_en)
    remplirDictionnaire("dictionnaries/francais/postes",  positions_fr)
    estPresentPosition = False
    if type == '1' :
        while True:
            positionRole = input("Role? (XXX): ")
            if len(positionRole) == 3:
                for i in positions_en:
                    for j in positions_fr:
                        if j[0] == positionRole:
                            role_fr = j[1]
                            estPresentPosition = True
                            break
                        if estPresentPosition == True:
                            break
                    if i[0] == positionRole:
                        role_en = i[1]
                        estPresentPosition = True
                        break
                if estPresentPosition == True:
                    break
            print("ROLE INEXISTANT\n")
            
    elif type == '2':
        positionRole = 'CTR'
        
    elif type == '3':
        positionRole = 'OCE'
            
    code = endroitCode + '_' + positionRole
    if type == '1':
        nom_en = endroit_en + ' ' + role_en
        nom_fr = endroit_fr + ' '+ role_fr
    elif type == '2' or type == '3':
        nom_en = endroit_en
        nom_fr = endroit_fr 
        
    frequency = input("Frequence de l'ATC? ")

    ATC = []    
    ATC.append(code)
    ATC.append(nom_en)
    ATC.append(nom_fr)
    ATC.append(frequency)

    listeATC.append(ATC)
    print("\nAJOUT DE L'ATC " + code)

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
        print("\n\n====================== SUPPRESSION ======================\n")
        ATCSuppr = input("Quel ATC veux-tu supprimer? ").upper()
        if ATCSuppr != "":
            indexATC = []
            for i in listeATC: 
                if i[0] == ATCSuppr:
                    indexATC = i 
                    break 
            listeATC.remove(indexATC) 
            print("\nSUPPRESSION DE L'ATC...")
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
    print("3. Supprimer")
    print("4. ATC / Frequences")
    print("5. Quitter")
    choix = input("Que veux-tu faire? ")

    #AJOUTER UN AVION
    if choix == '1':
        ajouterAvion()

    #AJOUTE CLEARANCE A UN AVION
    elif choix == '2':
        ajouterClearance()
    
    #SUPPRIMER UN AVION   
    elif choix == '3':
        supprimerAvion()

    #Modifier ATC
    elif choix == '4':
        atc()

    #QUITTER
    elif choix == '5':
        quitter = input("Voulez vous vraiment quitter? (Y / N) ")
        if quitter == 'Y' or quitter == 'y':
            print("\nEXIT")
            break
        
    #CHOIX INEXISTANT
    else:
        print("\nCHOIX INEXISTANT")
        
    input('')
    platforme(platform)
