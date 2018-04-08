import os
listeAvions = []
squawk = []
compagnies = []
aeroports = []
anglais = []
francais = []
frequenceDepart = raw_input('Frequence de depart: ')


#REMPLIR SQUAWK
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


#REMPLIR LISTE A PARTIR DES DICTIONNAIRES
def remplirDictionnaire(nomFichier, liste):
	fichier = open(nomFichier, "r")
	lines = fichier.readlines()
	values = []
	for i in lines:
		code, indicatif = i.split(",")
		indicatif = indicatif.split("\n")[0];
		values.append(code)
		values.append(indicatif)
		liste.append(values)
		values = []
	fichier.close()
    

#DETERMINER LE NIVEAU DE VOL
def flightLevel():
	flight_level = True
	while flight_level == True:
		regle = raw_input('Regle de vol? ')
		if regle.capitalize() == 'I':
			flight_level = '5000'
			return (flight_level, regle.capitalize())

		elif regle.capitalize() == 'V':
			flight_level = '1000'
			return (flight_level, regle.capitalize())

		elif regle.capitalize() == 'Y' or regle.capitalize() == 'Z':
			flight_level = 'CHECK'
			return (flight_level, regle.capitalize())

		else:
			print('Veuillez entrer selon les options suivantes:')
			print('I pour IFR')
			print('V pour VFR')
			print('Y pour IFR puis VFR')
			print('Z pour VFR puis IFR')


#AFFICHER LA LISTE DES AVIONS
def afficherListeAvions():
	if len(listeAvions) == 0:
		print("\nAUCUN AVION DANS LA LISTE")
	else:
		print("\nIL Y A " + str(len(listeAvions)) + " AVION(S):")
		compteur = 1
		for i in listeAvions:
			print(str(compteur) + ". " + i[0] + ": " + str(i))
			compteur += 1


#ASSIGNER UN SQUAWK A UN AVION
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


#RECHERCHER LE CALLSIGN
def rechercherIndicatif(code, liste):
	for i in liste:
		if code == i[0]:
			return(i[1])
	return("NULL AIRPORT")

        
#AJOUTER UN AVION
def ajouterAvion():
	print("\n\n====================== NOUVEL AVION ======================\n")

	compagnie = raw_input("Nom de la compagnie: ")
	numeroVol = raw_input("Numero du vol: ")
	nom = compagnie + numeroVol
	langue = raw_input("Langue: ")
	if langue.upper() == "EN":
		remplirDictionnaire("alphabet_anglais", anglais)
	elif langue.upper() == "FR":
		remplirDictionnaire("alphabet_francais", francais)
        
	destination = raw_input("Destination: ")
    
	(flightlevel, regle) = flightLevel()
	sid = raw_input("SID: ")
	rwy = raw_input("RWY: ")
	squawk = assignerSquawk()

	avion = []    
	avion.append(nom)
	avion.append(langue.upper())
	avion.append(destination)
	avion.append(regle)
	avion.append(sid)
	avion.append(rwy)
	avion.append(flightlevel)
	avion.append(squawk)
	avion.append(None)#clearance nulle
    
	listeAvions.append(avion)
	print("\nAJOUT DE L'AVION " + nom)


#SUPPRIMER UN AVION
def supprimerAvion():
	if len(listeAvions) > 0:
		print("\n\n====================== SUPPRESSION ======================\n")
        
		avionSuppr = input("Quel avion veux-tu supprimer? ")
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
		else:
			print("\nAVION INTROUVABLE...")
	else:
		print("\nAUCUN AVION A SUPPRIMER")


def creerClearance(avion):
	altimetre = raw_input('QNH? ')
	print('1. Clearance initiale')
	print('2. Push et demarrage')
	print('3. Taxi')
	print('4. Line-up')
	print('5. Takeoff')
	print('6. Leg VFR')
	print('7. Landing')
	print('8. Depart espace aerien VFR')
	typeClearance = raw_input('Quelle clearance veux-tu donner? ')

	nom = avion[0]
	langue = avion[1]
	destination = avion[2]
	indicatifAeroport = rechercherIndicatif(avion[2], aeroports)
	regle = avion[3]
	sid = avion[4]
	rwy = avion[5]
	flightLevel = avion[6]
	squawk = str(avion[7])
	clearance = avion[8]
	clearance_txt = ""

#Clearance Initiale IFR
	if typeClearance == '1':
		if regle == 'I' or regle == 'Y':
			if langue == 'EN':
				clearance_txt = nom+' is cleared to '+indicatifAeroport+', via the '+sid+' departure, then planned route, expect runway '+rwy+', Initial climb '+flightLevel+', squawk '+squawk
                
			elif langue == 'FR':
				clearance_txt = nom+', depart vers '+indicatifAeroport+' approuve, depart via '+sid+', puis route prevue, piste '+rwy+' prevue , montee initiale '+flightLevel+', squawk '+squawk
                
			else:
				print('\nAucun message disponible: Verifiez la langue')
			clearance = 'INIT'

        #Clearance Initiale + Taxi VFR
		elif regle == 'V' or regle == 'Z':
			if destination == 'CYUL':#A modifier pour l'examen ACC
				if langue == 'EN':
					taxiRoute = raw_input('Taxi? ')
					clearance_txt = nom+', right hand pattern'+flightLevel+', squawk '+squawk+'taxi holding point runway '+rwy+' via '+taxiRoute
                    
			else:
				if langue == 'EN':
					taxiRoute = raw_input('Taxi? ')
					clearance_txt = nom+'initial climb '+flightLevel+', squawk '+squawk+', taxi holding point runway'+rwy+' via '+taxiRoute+', hold short '+rwy+', report ready for takeoff'

				elif langue == 'FR':
					print('\nfr')

			clearance = 'TAXI'
                
    #Clearance Push + Start
	elif typeClearance == '2':
 		if langue == 'EN':
			clearance_txt = nom+', pushback and startup at your discretion, advise ready for taxi.'

		elif langue == 'FR':
			print("\nfr")

		clearance = 'PUSH'
            
    #Clearance Taxi				
	elif typeClearance == '3':
		taxiRoute = raw_input('Taxi? ')
        if langue == 'EN':
            clearance_txt = nom+', runway '+rwy+', taxi '+taxiRoute+', hold short '+rwy+', report ready for takeoff'

        elif langue == 'FR':
            print('\nfr')

        clearance = 'TAXI'
#Clearance line-up
	if clearance == '4':
		if langue == 'EN':
			clearance_txt = nom+' line up and wait runway '+rwy

		elif langue == 'FR':
			clearance_txt = nom+' alignez-vous piste '+rwy+' et attendez'

		clearance = 'LNUP'

    #Clearance Decollage
	elif typeClearance == '5':
		if regle == 'I' or regle == 'Y' or regle == 'Z':
			if langue == 'EN':
				clearance_txt = nom+' contact Montreal departure on '+frequenceDepart+' airborne, cleared for takeoff runway '+rwy

			elif langue == 'FR':
				print('\nfr')

		elif regle == 'V':
			if rwy == '06R':
				if langue == 'EN':
					clearance_txt = nom+' report left hand downwind runway '+rwy+', cleared for takeoff, winds [VENTS]'

				elif langue == 'FR':
					clearance_txt = nom+'rappelez au downind main gauche piste '+rwy+', autorise decollage, vents [VENTS]'
			elif rwy == '24L':
				if langue == 'EN':
					clearance_txt = nom+' report right hand downwind runway '+rwy+', cleared for takeoff, winds [VENTS]' 
				elif langue == 'EN':
					clearance_txt = nom+'rappelez au downwind main droite piste'+rwy+', autorise decollage, vents [VENTS]'

        clearance = 'TKOF'

    #Clearance leg VFR
	if typeClearance == '6':
		if regle == 'I' or regle == 'Y':
			print('Non disponible pour les vols IFR')
			return()

		elif regle == 'V' or 'Z':
			if regle == 'V':
				print '1. Downwind'
				print '2. Base'
				print '3. Insertion dans pattern'
				TypeClearance= raw_input('Quel leg? ')
        		if TypeClearance == '1':
        			print '1'
				clearance_txt = 'To be defined'

	print(clearance_txt)
        #MENU LEG ICI
    
	if clearance != "TAXI":
		if len(avion) > 9:
			avion.remove(avion[9])
	avion[8] = clearance
            

#AJOUTER UNE CLEARANCE A UN AVION
def ajouterClearance():
    if len(listeAvions) > 0:
        os.system('clear')
        while True:
            print("\n\n================== CLEARANCE ==================\n")
            afficherListeAvions()

            avionClearance = raw_input("\nA quel avion veux-tu ajouter une clearance? ")
            avionPresent = False
            indexAvion = []
            for i in listeAvions:
                if i[0] == avionClearance:
                    avionPresent = True
                    indexAvion = i
                    break
            if avionPresent == True:
                creerClearance(indexAvion)
                break
            else:
                print("\nAVION INTROUVABLE...")
                raw_input('')
                os.system('clear')
    else:
        print("\nAUCUN AVION DANS LA LISTE")


#PROGRAMME PRINCIPAL
remplirSquawk()
remplirDictionnaire("compagnies", compagnies)
remplirDictionnaire("aeroports", aeroports)

while True:
    print("\n\n================== PROGRAMME PRINCIPAL ==================\n")
    afficherListeAvions()
    print("\n1. Ajouter un avion")
    print("2. Ajouter clearance a un avion")
    print("3. Supprimer")
    print("4. Quitter")
    choix = raw_input("Que veux-tu faire? ")

    #AJOUTER UN AVION
    if choix == '1':
        ajouterAvion()

    #AJOUTE CLEARANCE A UN AVION
    elif choix == '2':
        ajouterClearance()
    
    #SUPPRIMER UN AVION   
    elif choix == '3':
        supprimerAvion()

    #QUITTER
    elif choix == '4':
        quitter = raw_input("Voulez vous vraiment quitter? (Y / N) ")
        if quitter == 'Y' or quitter == 'y':
            print("\nEXIT")
            break
        
    #CHOIX INEXISTANT
    else:
        print("\nCHOIX INEXISTANT")
        
    raw_input('')
    os.system('clear')