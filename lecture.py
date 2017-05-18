import chip8

# Transforme le fichier texte en une liste, chaque bloc correspond à une ligne

def lecture(fichier):
    fichierCHIP8 = open(fichier, 'rb').read()
    for i, x in enumerate(fichierCHIP8): # On va lire ligne par ligne le fichier
        chip8.memoire[512 + i] = x # On stock dans la mémoire en commençant à l'octet 512 selon la doc

# Procédure qui sauvegarde le programme en cours de route

def sauvegarde(nomSauv):
    fichierSauve = open(nomSauv, 'w') # On ouvre le fichier en écriture
    # On écrit la mémoire
    for x in chip8.memoire:
        fichierSauve.write(str(x) + '\n')
    # On écrit les registres V0 à VF
    for x in chip8.V:
        fichierSauve.write(str(x) + '\n')
    # On écrit les autres registre : I, DT, ST, PC et SP
    fichierSauve.write(str(chip8.I) + '\n')
    fichierSauve.write(str(chip8.DT) + '\n')
    fichierSauve.write(str(chip8.ST) + '\n')
    fichierSauve.write(str(chip8.PC) + '\n')
    fichierSauve.write(str(chip8.SP) + '\n')
    # On écrit la pile de saut
    for x in chip8.saut:
        fichierSauve.write(str(x) + '\n')
    # On écrit le nombre de saut
    fichierSauve.write(str(chip8.nbrSaut) + '\n')
    # On écrit le tableau contenant la valeur des pixels
    for x in chip8.tabEcran:
        for y in x:
            fichierSauve.write(str(y) + '\n')
    # On ferme le fichier
    fichierSauve.close()

# Procédure qui charge une sauvegarde

def chargement(nomSauv):
    # On test si le fichier existe
    try:
        with open(nomSauv):
            pass
    # Si il n'existe pas on renvoit une erreur et on affichage "Le fichier n'existe pas"
    except IOError:
        print("Le fichier n'existe pas")
        return 0
    # On ouvre le fichier
    fichierSauve = open(nomSauv, 'r')
    # On va transformer le fichier en une liste
    listeSauv = []
    for x in fichierSauve:
        listeSauv.append(int(x.replace('\n',''))) # On retire les \n
    # On stocke les 4096 premières ligne dans la mémoire
    chip8.memoire = []
    for i in range(4096):
        chip8.memoire.append(listeSauv[i])
    # On stocke les 16 lignes suivantes dans les registre V0 à VF
    chip8.V = []
    for i in range(4096, 4112):
        chip8.V.append(listeSauv[i])
    # On stocke les 5 lignes suivantes dans les registres I, DT, ST, PC et SP
    chip8.I = listeSauv[4112]
    chip8.DT = listeSauv[4113]
    chip8.ST = listeSauv[4114]
    chip8.PC = listeSauv[4115]
    chip8.SP = listeSauv[4116]
    # On stocke les 16 lignes suivantes dans la pile de saut
    chip8.saut = []
    for i in range(4117, 4133):
        chip8.saut.append(listeSauv[i])
    # On stocke la ligne suivante dans le nombre de saut
    chip8.nbrSaut = listeSauv[4133]
    # On finit par remplir le tableau représentant la valeur des pixels
    chip8.tabEcran = []
    for i in range(32):
        ligne = []
        for j in range(64):
            ligne.append(listeSauv[4134+j+(64*i)])
        chip8.tabEcran.append(ligne)