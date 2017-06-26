import memoire
import sys

# Transforme le fichier texte en une liste, chaque bloc correspond à une ligne

def lecture(fichier):
    # On test si le fichier existe
    try:
        with open(sys.path[0] + '/Programme/' + fichier):
            pass
    # Si il n'existe pas on renvoit 0 (erreur)
    except IOError:
        return 0
    # On ouvre le fichier
    fichierCHIP8 = open(sys.path[0] + '/Programme/' + fichier, 'rb').read()
    for i, x in enumerate(fichierCHIP8): # On va lire ligne par ligne le fichier
        memoire.memoire[512 + i] = x # On stock dans la mémoire en commençant à l'octet 512 selon la doc

# Procédure qui sauvegarde le programme en cours de route

def sauvegarde(nomSauv, force = False):
    # On test si le fichier existe
    try:
        with open(sys.path[0] + '/Sauvegarde/' + nomSauv):
            if not force:
                return 0
    # Si il n'existe pas on renvoit 0 (erreur)
    except IOError:
        pass
    fichierSauve = open(sys.path[0] + '/Sauvegarde/' + nomSauv, 'w') # On ouvre le fichier en écriture
    # On écrit la mémoire
    for x in memoire.memoire:
        fichierSauve.write(str(int(x)) + '\n')
    # On écrit les registres V0 à VF
    for x in memoire.V:
        fichierSauve.write(str(x) + '\n')
    # On écrit les autres registre : I, DT, ST, PC et SP
    fichierSauve.write(str(memoire.I) + '\n')
    fichierSauve.write(str(memoire.DT) + '\n')
    fichierSauve.write(str(memoire.ST) + '\n')
    fichierSauve.write(str(memoire.PC) + '\n')
    fichierSauve.write(str(memoire.SP) + '\n')
    # On écrit la pile de saut
    for x in memoire.saut:
        fichierSauve.write(str(x) + '\n')
    # On écrit le tableau contenant la valeur des pixels
    for x in memoire.tabEcran:
        for y in x:
            fichierSauve.write(str(y) + '\n')
    # On ferme le fichier
    fichierSauve.close()

# Procédure qui charge une sauvegarde

def chargement(nomSauv):
    # On test si le fichier existe
    try:
        with open(sys.path[0] + '/Sauvegarde/' + nomSauv):
            pass
    # Si il n'existe pas on renvoit une erreur et on affichage "Le fichier n'existe pas"
    except IOError:
        return 0
    # On ouvre le fichier
    fichierSauve = open(sys.path[0] + '/Sauvegarde/' + nomSauv, 'r')
    # On va transformer le fichier en une liste
    listeSauv = []
    for x in fichierSauve:
        listeSauv.append(int(x.replace('\n',''))) # On retire les \n
    # On stocke les 4096 premières ligne dans la mémoire
    memoire.memoire = []
    for i in range(4096):
        memoire.memoire.append(listeSauv[i])
    # On stocke les 16 lignes suivantes dans les registre V0 à VF
    memoire.V = []
    for i in range(4096, 4112):
        memoire.V.append(listeSauv[i])
    # On stocke les 5 lignes suivantes dans les registres I, DT, ST, PC et SP
    memoire.I = listeSauv[4112]
    memoire.DT = listeSauv[4113]
    memoire.ST = listeSauv[4114]
    memoire.PC = listeSauv[4115]
    memoire.SP = listeSauv[4116]
    # On stocke les 16 lignes suivantes dans la pile de saut
    memoire.saut = []
    for i in range(4117, 4133):
        memoire.saut.append(listeSauv[i])
    # On finit par remplir le tableau représentant la valeur des pixels
    memoire.tabEcran = []
    for i in range(32):
        ligne = []
        for j in range(64):
            ligne.append(listeSauv[4133+j+(64*i)])
        memoire.tabEcran.append(ligne)
    # On ferme le fichier
    fichierSauve.close()