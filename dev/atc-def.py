centre = []
oceanique = []
a=1

def frequences():
    print ('1. Ajouter un ATC ')
    print ('2. Enlever un ATC ')
    print ('3. Changer une frequence ')
    atc = input('Que veux-tu changer? ')
    
    if atc == '1':
        print (atc)
        
    elif atc == '2':
        print (atc)
    
    elif atc == '3':
        print (atc)

frequences()

def atc():
    print("\n\n====================== NOUVEL ATC ======================\n")
    poste = input('Poste? (XXXX) ')
    position = input('Position? (_XXX)')
    type = input("Centre (C) ou Oceanique (O): ")
    nom = compagnie + numeroVol

    if type.upper() == "C":
        remplirDictionnaire("dictionnaires/FIR", centre)
    elif langue.upper() == "O":
        remplirDictionnaire("../dictionnaires/OCEANIC", oceanique)
	
    destination = input("Destination: ")
    (flightlevel, regle) = flightLevel()
    if regle == 'EXIT':
	return()
    sid = input("SID: ")
    rwy = input("RWY: ")
    squawk = assignerSquawk()

	atc = []    
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