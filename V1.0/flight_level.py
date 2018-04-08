airport_code = 'OACI'
airport_name = 'Nom'
compagnie = 'IND'
indicatif_appel = 'Indicatif'
numero_vol = '###'
flight_level = True
sid = 'SID1A'
runway = '##X'
squawk = '####'
langue = 'EN'
rwy = '##x'

flt_strip = compagnie + numero_vol
callsign = indicatif_appel + ' ' + numero_vol

#Altitude + Regles

while flight_level == True:
    regle = raw_input('Regle de vol? ')

    if regle.capitalize() == 'I':
        flight_level = '5000'

    elif regle.capitalize() == 'V':
        flight_level = '1000'

    elif regle.capitalize() == 'Y' or regle.capitalize() == 'Z':
        flight_level = 'CHECK'

    else:
        print 'Veuillez entrer selon les options suivantes:'
        print 'I pour IFR'
        print 'V pour VFR'
        print 'Y pour IFR puis VFR'
        print 'Z pour VFR puis IFR'

#messages clearances

#clearance initiale IFR
def creer_clearance():
	import os
	altimetre = raw_input('QNH? ')
	os.system('clear')
	print '1. Clearance initiale'
	print '2. Push et demarrage'
	print '3. Taxi'
	print '4. Line-up'
	print '5. Takeoff'
	print '6. Leg VFR'
	print '7. Landing'
	print '8. Depart espace aerien VFR'
	type_clearance = raw_input('Quelle clearance veux-tu donner? ')
	
	if type_clearance == '1':
		if regle == 'I' or regle == 'Y':
			if langue == 'EN':
				clearance_txt = callsign + ' is cleared to ' + airport_name + ',via the ' + sid + ' departure, then planned route, expect runway ' + rwy + ', Initial climb ' + flight_level + ', squawk ' + squawk 

			elif langue  == 'FR':
				clearance_txt = callsign + ', depart vers ' + airport_name + ' approuve, depart via ' + sid + ', puis route prevue, piste ' + rwy + ' prevue , montee initiale ' + flight_level + ', squawk ' + squawk
			else:
				print 'Aucun message disponible: Verifiez la langue'
			
			clearance = 'INIT'

#Clearance Initiale + Taxi VFR
		
		elif regle == 'V' or regle == 'Z':
			if destination == 'CYUL':				#A modifier pour l'examen ACC
				if langue == 'EN':
					taxi_route = raw_input('Taxi? ')
					clearance_txt = callsign + ', right hand pattern' + flight_level + ', squawk ' + squawk + 'taxi holding point runway ' + rwy + ' via ' + taxi_route
				
			else:
				if langue == 'EN':
					taxi_route = raw_input('Taxi? ')
					clearance_txt = callsign + 'initial climb ' + flight_level + ', squawk ' + squawk + ', taxi holding point runway' + rwy + ' via ' + taxi_route + ', hold short ' + rwy + ',  report ready for takeoff'
					
			clearance = 'TAXI'
		
		
#clearance push + start

	elif type_clearance == '2':
		if langue == 'EN':
			clearance_txt = callsign + ', pushback and startup at your discretion, advise ready for taxi.'
		
		elif langue == 'FR':
			print 'fr'
			
		clearance = 'PUSH'

#clearance Taxi		
			
	elif type_clearance == '3':
		taxi_route = raw_input('Taxi? ')
		if langue == 'EN':
			clearance_txt = callsign + ', runway ' + rwy + ', altimeter ' + altimetre + ', taxi ' + taxi_route + ', hold short ' + rwy + ', report ready for takeoff'
		
		elif langue == 'FR':
			print 'fr'
			
		clearance = 'TAXI'	
		
#clearance line-up

	elif type_clearance == '4':
		if langue == 'EN':
			clearance_txt = callsign + ' line up and wait runway ' + rwy
			
		elif langue == 'FR':
			clearance_txt = callsign + ' alignez-vous piste ' + rwy + ' et attendez'
			
		clearance = 'LNUP'

#clearance decollage
			
	elif type_clearance == '5':
		if regle == 'I' or regle == 'Y' or regle == 'Z':
			if langue == 'EN':
				clearance_txt = callsign + ' contact Montreal departure on ' + frequence_depart + ' airborne, cleared for takeoff runway ' + rwy
		
			elif langue == 'FR':
				print 'fr'
		
		elif regle == 'V':
			if rwy == '06R':
				if langue == 'EN':
					clearance_txt = callsign + 'report left hand downwind runway ' + rwy + ', cleared for takeoff, winds [VENTS]'

		clearance = 'TKOF'
		

#clearance leg VFR
	
	elif type_clearance == '6':
		if regle == 'I' or regle == 'Y':
			print 'Non disponible pour les vols IFR'
			return()
		
		elif regle == 'V' or 'Z':
			clearance_txt = 'TO BE DEFINED'
	print clearance_txt		
creer_clearance()
			
