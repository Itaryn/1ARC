import chip8

# Transforme le fichier texte en une liste, chaque bloc correspond à une ligne

def lecture(fichier):
    fichierCHIP8 = open(fichier, 'rb').read()
    for i, x in enumerate(fichierCHIP8):
        chip8.memoire[512 + i] = x

# Sauvegarde le programme en cours de route

def sauvegarde(nomSauv):
    fichierSauve = open(nomSauv, 'w')
    for x in chip8.memoire:
        fichierSauve.write(str(x) + '\n')
    for x in chip8.V:
        fichierSauve.write(str(x) + '\n')
    fichierSauve.write(str(chip8.I) + '\n')
    fichierSauve.write(str(chip8.DT) + '\n')
    fichierSauve.write(str(chip8.ST) + '\n')
    fichierSauve.write(str(chip8.PC) + '\n')
    fichierSauve.write(str(chip8.SP) + '\n')
    for x in chip8.saut:
        fichierSauve.write(str(x) + '\n')
    fichierSauve.write(str(chip8.nbrSaut) + '\n')
    for x in chip8.tabEcran:
        for y in x:
            fichierSauve.write(str(y) + '\n')
    fichierSauve.close()

# Charge une sauvegarde

def chargement(nomSauv):
    # On test si le fichier existe
    try:
        with open(nomSauv):
            pass
    except IOError:
        print("Le fichier n'existe pas")
        return 0
    fichierSauve = open(nomSauv, 'r')
    listeSauv = []
    for x in fichierSauve:
        listeSauv.append(int(x.replace('\n','')))
    chip8.memoire = []
    for i in range(4096):
        chip8.memoire.append(listeSauv[i])
    chip8.V = []
    for i in range(4096, 4112):
        chip8.V.append(listeSauv[i])
    chip8.I = listeSauv[4112]
    chip8.DT = listeSauv[4113]
    chip8.ST = listeSauv[4114]
    chip8.PC = listeSauv[4115]
    chip8.SP = listeSauv[4116]
    chip8.saut = []
    for i in range(4117, 4133):
        chip8.saut.append(listeSauv[i])
    chip8.nbrSaut = listeSauv[4133]
    chip8.tabEcran = []
    for i in range(32):
        ligne = []
        for j in range(64):
            ligne.append(listeSauv[4134+j+(64*i)])
        chip8.tabEcran.append(ligne)