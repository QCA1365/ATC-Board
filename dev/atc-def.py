fir = []
aeroport = []
listeATC = []
a=1

#REMPLIR LISTE A PARTIR DES DICTIONNAIRES
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
    
    print ('1. Aeroport')
    print ('2. FIR')
    local = input('FIR ou aeroport? ')
    if local == '1':
        poste = input('Poste? (XXXX) ')
        position = input('position? (_XXX) ')
        remplirDictionnaire("../V1.0/dictionnaires/aeroports", aeroport)
        
    
    elif local == '2':
        poste = input('Poste? (XXXX) ')
        position = 'CTR'
        type = input("Centre (C) ou Oceanique (O): ")
        if type.upper() == "C":
            remplirDictionnaire("../V1.0/dictionnaires/FIR", fir)
        elif type.upper() == "O":
            remplirDictionnaire("../V1.0/dictionnaires/OCEANIC", fir)
    nom = poste+'_'+position
    frequence = input("Quelle est la frquence de l'ATC? ")


    atc = []    
    atc.append(nom.upper())
    atc.append(frequence)
    listeATC.append(atc)
    print("\nAJOUT DE L'ATC " + nom)
    
atc()