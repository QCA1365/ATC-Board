import os
from sys import platform
from datetime import datetime
listeAvions = []
squawk = []
compagnies = []
aeroports = []
anglais = []
francais = []
frequenceDepart = input('Frequence de depart: ')
position = []
nom_controle = []


#Cette section est inutile pour le moment... Doit etre incorporee dans les structures plus basses
#Entres autres dans des options a ajouter eventuellement telles que aeroport d'arrivee
#Ou encore pour definir certaines phraseologies a adopter comme le rapport a certains points

def position():
	print ('1. XXXX_DEL')
	print ('2. XXXX_GND')
	print ('3. XXXX_TWR')
	print ('4. XXXX_DEP')
	print ('5. XXXX_APP')
	print ('6. XXXX_CTR')
	position = input('Quelle position? ')
	return position
	
def frequences():
	nom_controle = input('Quel est le code du controleur? ')
	frequence_controle = input('Quelle est la frquence du controleur')
	

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
		
		elif regle == 'exit':
			flight_level = 'VOID'
			return (flight_level, regle.upper())

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
	print('9. Urgence')
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
			
			clearance = 'INIT'

#Clearance Initiale + Taxi VFR
		elif regle == 'V' or regle == 'Z':
			taxiRoute = input('Taxi? ')
			avion.append(taxiRoute)
			if destination == 'CYUL':	### ---------- A modifier pour l'examen ACC ---------- ###
				if runway == '24L' or runway == '06L': 
					if langue == 'EN':
						clearance_txt = nom+', right hand pattern '+flightLevel+', squawk '+squawk+' taxi holding point runway '+rwy+' via '+taxiRoute
					
					elif langue == 'FR':
						clearance_txt = nom+', tour de piste main droite a '+flightLevel+' pieds, squawk '+squawk+" taxi point d'arret piste "+rwy+' via '+taxiRoute 
				
				elif runway == '06R' or runway  == '24R':
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
		altimetre = input('QNH? ')
		taxiRoute = input('Taxi? ')
		avion.append(taxiRoute)
		if langue == 'EN':
			clearance_txt = nom+', runway '+rwy+', altimeter '+altimetre+ ', taxi '+taxiRoute+', hold short '+rwy+', report ready for takeoff'
            
		elif langue == 'FR':
			clearance_txt = nom + ', piste ' + rwy + ', altimetre ' + altimetre + ', taxi ' + taxiRoute + ", restez a l'ecart piste " + piste + ', rappelez pret a decoller' 

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
				clearance_txt = nom + ', contactez Montreal departs sur ' + frequenceDepart + ' en vol, autorise decollage piste ' + rwy

		elif regle == 'V':
			if rwy == '06R' or rwy == '24R':
				if langue == 'EN':
					clearance_txt = nom+ ' report right hand downwind runway '+rwy+', cleared for takeoff, winds [VENTS]'

				elif langue == 'FR':
					clearance_txt = nom+ ' rappelez downwind main droite '+rwy+', autorise decollage, vents [VENTS]'

			elif rwy == '06L' or rwy == '24L':
				if langue == 'EN':
					clearance_txt = nom + 'report left hand downwind runway '+rwy+', cleared for takeoff, winds [VENTS]'
				
				elif langue == 'FR':
					clearance_txt = nom+ ' rappelez downwind main gauche '+rwy+', autorise decollage, vents [VENTS]'

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
				print ('1. Report end of Downwind')
				print ('2. Downwind -> Final')
				print ('3. Extend Downwind')
				position2 = input('Quelle clearance?')
				
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
						clearance_txt = nom + ', report on final runway ' + rwy + ',numero ' + numero
										
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
				altimetre = input('QNH? ')
				print ('1. approche straight-in')
				print ('2. fin de downwind')
				print ('3. VFR entry-point')
				position2 = input('Quelle clearance? ')

				#Approche Straight-In
				if position2 == '1':
					if langue == 'EN':
						clearance_txt = nom + ', make straight-in approach runway ' + rwy + ', winds [VENTS], altimeter ' + altimetre
					
					elif langue == 'FR':
						clearance_txt = nom + ', faites une approche directe piste ' + rwy + ', vents [VENTS], altimetre ' + altimetre
					
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
								clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							
							elif langue == 'FR':
								clearance_txt = nom + ', rejoignez downwind main gauche ' + rwy + ', vents [VENTS], altimetre ' + altimetre
							
							clearance = 'LHDW'
						
						elif rwy == '24L' or rwy == '24L':
							if langue == 'EN':
								clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							
							elif langue == 'FR':
								clearance_txt = nom + ', rejoignez downwind main gauche piste ' + rwy + ', vents [VENTS], altimetre ' + altimetre
							
							clearance = 'RHDW'
					
					elif cote == '2':
						if rwy == '06R' or rwy == '24R':
							if langue == 'EN':
								clearance_txt = nom + ', join right hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre
							clearance = 'RHDW'
						
						elif rwy == '24L' or rwy == '06L':
							if langue == 'EN':
								clearance_txt = nom + ', join left hand downwind runway ' + rwy + ', wind [VENTS], altimeter ' + altimetre

							elif langue == 'FR':
								clearance_txt = nom + ', rejoignez downwind main gauche ' + rwy + ', vents [VENTS], altimetre ' + altimetre
							
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
				clearance_txt = nom + ', winds [VENTS], exit at ' + sortie + ', cleared to land runway ' + rwy
			
			elif langue  == 'FR':
				clearance_txt = nom + ', vents [VENTS], sortez a ' +  sortie + ', autorise a atterir piste ' + rwy
				
			clearance = 'LDG'+rwy
			
		#Touch and Go	
		elif operation == '2':
			if langue == 'EN':
				clearance_txt = nom + ', runway ' + rwy + ', cleared touch and go, winds [VENTS]'
			
			elif langue == 'FR':
				clearance_txt = nom + ', piste ' + rwy + ', autorise toucher, vents [VENTS]'
			
			clearance = 'T&GO'
		
		#Low Pass
		elif operation == '3':
			if langue == 'EN':
				clearance_txt = nom + ', cleared low pass runway ' + rwy + ', winds [VENTS]'
				
			elif langue == 'FR':
				clearance_txt = nom + ', autorise low pass piste ' + rwy + ', winds [VENTS]'
				
			clearance = 'LOWP'
			
		#Stop and Go
		elif operation == '4':
			if langue == 'EN':
				clearance_txt = nom + ', cleared to land runway ' + rwy + ', winds [VENTS] \n Report ready for take-off -> Donner clearance Takeoff'
			
			if langue == 'FR':
				clearance_txt = nom + ', autorise a atterir piste ' + rwy + ', vents [VENTS] \n Rappelez pret a decoller -> Donner clearance Takeoff'
				 
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
		print ('1. Decollage -> point')
		print ('2. Sortie zone de controle')
		maniere = input('Quelle clearance? ')
		
		if maniere == '1':
			point = input('Quel est le point de rapport? ')
			if langue == 'EN':
				clearance_txt = nom + ', report over ' + point + ', runway ' + rwy + ', cleared for takeoff, winds [VENTS]'
			
			elif langue == 'FR':
				clearance_txt = nom + ', rappelez a ' + point + ', piste ' +rwy+ ', autorise decollage, vents [VENTS]'
			
			clearance = 'TOPT'
		
		elif maniere == '2':
			if langue == 'EN':
				clearance_txt = nom + ', frequency change approved, monitor UNICOM 122.8, good day!'
			
			elif langue == 'FR':
				clearance_txt = nom + ', changement de frequence approuve, surveillez unicom 122.8, Bon vol!'
			
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
            

#AJOUTER UNE CLEARANCE A UN AVION
def ajouterClearance():
	if len(listeAvions) > 0:
		if platform == "linux" or platform == "linux2":
			os.system('clear')
		elif platform == "win32":
			os.system('CLS')
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
				if platform == "linux" or platform == "linux2":
					os.system('clear')
				elif platform == "win32":
					os.system('CLS')
	else:
		print("\nAUCUN AVION DANS LA LISTE")


#### ===== ----- ===== ----- ===== ----- ===== ----- PROGRAMME PRINCIPAL ----- ===== ----- ===== ----- ===== ----- =====
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
	if platform == "linux" or platform == "linux2":
		os.system('clear')
	elif platform == "win32":
		os.system('CLS')
