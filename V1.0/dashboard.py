import os
listeAvions = []
squawk = []
compagnies = []
aeroports = []
anglais = []
francais = []
frequenceDepart = input('Frequence de depart: ')


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
	return(code)

        
#AJOUTER UN AVION
def ajouterAvion():
	print("\n\n====================== NOUVEL AVION ======================\n")

	compagnie = input("Nom de la compagnie: ")
	numeroVol = input("Numero du vol: ")
	nom = compagnie + numeroVol
    
	langue = input("Langue: ")
	if langue.upper() == "EN":
		remplirDictionnaire("dictionnaires/alphabet_anglais", anglais)
	elif langue.upper() == "FR":
		remplirDictionnaire("dictionnaires/alphabet_francais", francais)
        
	destination = input("Destination: ")
    
	(flightlevel, regle) = flightLevel()
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


#SUPPRIMER UN AVION
def supprimerAvion():
	if len(listeAvions) > 0:
		print("\n\n====================== SUPPRESSION ======================\n")
        
		avionSuppr = input("Quel avion veux-tu supprimer? ").upper()
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


#CREER UNE CLEARANCE
def creerClearance(avion):
	print('1. Clearance initiale')
	print('2. Push et demarrage')
	print('3. Taxi')
	print('4. Line-up')
	print('5. Takeoff')
	print('6. Leg VFR')
	print('7. Landing')
	print('8. Depart espace aerien VFR')
	typeClearance = input('Quelle clearance veux-tu donner? ')

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
					taxiRoute = input('Taxi? ')
					clearance_txt = nom+', right hand pattern '+flightLevel+', squawk '+squawk+' taxi holding point runway '+rwy+' via '+taxiRoute
                    
			else:
				if langue == 'EN':
					taxiRoute = input('Taxi? ')
					clearance_txt = nom+' initial climb '+flightLevel+', squawk '+squawk+', taxi holding point runway '+rwy+' via '+taxiRoute+', hold short '+rwy+', report ready for takeoff'

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
		altimetre = input('QNH? ')
		taxiRoute = input('Taxi? ')
		if langue == 'EN':
			clearance_txt = nom+', runway '+rwy+', altimeter '+altimetre+ ', taxi '+taxiRoute+', hold short '+rwy+', report ready for takeoff'
			avion.append(taxiRoute)
            
		elif langue == 'FR':
			print('\nfr')

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
			if langue == 'EN':
				clearance_txt = nom+' contact Montreal departure on '+frequenceDepart+' airborne, cleared for takeoff runway '+rwy

			elif langue == 'FR':
				print('\nfr')

		elif regle == 'V':
			if rwy == '06R':
				if langue == 'EN':
					clearance_txt = nom+' report left hand downwind runway '+rwy+', cleared for takeoff, winds [VENTS]'

				elif langue == 'FR':
					print('\nfr')

		clearance = 'TKOF'

    #Clearance leg VFR							##### ========== AJOUTER LE FRANCAIS ========== #####
	elif typeClearance == '6':
		if regle == 'I' or regle == 'Y':
			print('Non disponible pour les vols IFR')
			return()

		elif regle == 'V' or 'Z':
			print '1. Circuit'
			print '2. Arrivees'
			position = input('Quelle position? ')
			
			if position == '1':
				print '1. Report end of Downwind'
				print '2. Downwind -> Final'
				print '3. Extend Downwind'
				position2 = input('Quelle clearance?')
				
				if position2 == '1':
					clearance_txt = nom + ', report end of downwind runway ' + rwy
					clearance = 'DWND'
				
				elif position2 == '2':
					numero = input('Numero en approche? ')
					clearance_txt = nom + ', report on final runway ' +rwy', number ' + numero
					clearance = 'FINL'
				
				elif position2 == '3':
					numero = input('Numero en approche? ')
					clearance_txt = nom + ', extend downwind, number ' + numero + ', 4 miles final runway ' + rwy
					clearance = 'EXTD'
					
			if position == '2':
				altimetre = input('QNH? ')
				print '1. approche straight-in'
				print '2. fin de downwind'
				print '3. VFR entry-point'
				position2 = input('Quelle clearance? ')

				if position2 == '1':
					clearance_txt = nom + ', make straight-in approach runway ' + rwy + ', winds [VENTS], altimeter ' + altimetre
					clearance = 'SIAP'
				
				elif position2 == '2':
					numero = input('Numero en approche? ')
					clearance_txt = nom + ', report on final runway ' + rwy + ', number ' + numero
					clearance = 'FINL'
					
				elif position == '3':
					print "1. Arrive de l'est"
					print "2. Arrive de l'ouest"
					cote = input('Quel cote? ')	

					if cote == '1':
						if rwy == '06R':
							clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							clearance = 'LHDW'
						
						elif rwy == '24L':
							clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							clearance = 'RHDW'
					
					elif cote == '2':
						if rwy == '06R':
							clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							clearance = 'RHDW'
						
						elif rwy == '24L':
							clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							clearance = 'LHDW'

#atterissage

	elif typeClearance == '7':
		if langue == 'EN':
			sortie = input('Quelle sortie? ')
			clearance_txt = nom + ', winds [VENTS], exit at ' + sortie + ', cleared to land runway ' + rwy
			clearance = 'LDG'+rwy
			

        #MENU LEG ICI

	print("\n"+clearance_txt)
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

			avionClearance = input("\nA quel avion veux-tu ajouter une clearance? ").upper()
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
				input('')
				os.system('clear')
	else:
		print("\nAUCUN AVION DANS LA LISTE")


#PROGRAMME PRINCIPAL
remplirSquawk()
remplirDictionnaire("dictionnaires/compagnies", compagnies)
remplirDictionnaire("dictionnaires/aeroports", aeroports)

while True:
	print("\n\n================== PROGRAMME PRINCIPAL ==================\n")
	afficherListeAvions()
	print("\n1. Ajouter un avion")
	print("2. Ajouter clearance a un avion")
	print("3. Supprimer")
	print("4. Quitter")
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

    #QUITTER
	elif choix == '4':
		quitter = input("Voulez vous vraiment quitter? (Y / N) ")
		if quitter == 'Y' or quitter == 'y':
			print("\nEXIT")
			break
        
    #CHOIX INEXISTANT
	else:
		print("\nCHOIX INEXISTANT")
        
	input('')
	os.system('clear')
