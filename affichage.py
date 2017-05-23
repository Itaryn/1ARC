import lecture, chip8, opcode
from tkinter import *

fenetreChip8 = Tk() # Création de la fenêtre tkinter

# Procédure principal qui va permettre de lancer l'instruction puis l'affichage

def fonctionnement():
    # On récupère l'Id et le code hexadécimale
    val, oc = opcode.interpretation()
    if val == 1:
        # 00E0 : On efface l'écran
        effacerEcran()
    elif val == 23:
        # DXYN : On dessine un sprite selon les données
        dessinerSprite(opcode.valueX(oc), opcode.valueY(oc), opcode.valueN(oc))
    elif val == 27:
        # FX0A : On attend l'appuie d'une touche puis on stocke dans VX
        attente = True
        while attente:
            for x, i in enumerate(chip8.tabTouche):
                if x == 1:
                    chip8.V[opcode.valueX(oc)] = i
    # On raffraichit les registres pour les afficher
    refreshRegistre()
    # On décompte les timers
    decompteSoundDelay()
    # On incrémente le PC
    chip8.PC += 2
    # A chaque tour on réinitialise le tableau des touches
    chip8.tabTouche = [0] * 16
    # On regarde si on est en mode step by step, si on ne l'est pas on relance cette procédure après 4ms
    if not stepActiver.get():
        fenetreChip8.after(16, fonctionnement)

# Procédure qui décompte les 2 timers de 1 tant qu'ils sont supérieurs à 0

def decompteSoundDelay():
    if chip8.DT > 0:
        chip8.DT -= 1
    if chip8.ST > 0:
        chip8.ST -= 1

# Procédure qui efface l'écran

def effacerEcran():
    # On efface l'écran graphique
    ecran.create_rectangle((5, 5, 325, 165), fill="black")
    # On éteint tous les pixels dans le tableau
    chip8.tabEcran = [[0 for x in range(64)] for x in range(32)]

# Procédure qui va dessiner un sprite

def dessinerSprite(x,y,n):
    chip8.V[0xF] = 0
    # On fait autant de ligne que nous a donné la valeur n du code hexadécimale
    for i in range(n):
        # On stocke le binaire à l'adresse mémoire adéquate (notre registre I + le nombre de ligne i)
        binaire = bin(chip8.memoire[chip8.I + i])
        # On calcul la ligne où l'on va allumer ou éteindre les pixels
        coordY = (chip8.V[y] + i) % 32
        # On test chaque bit de l'octet récupéré
        for k in range(-1, -9, -1):
            # Si on arrive à la fin de l'octet on arrête la boucle
            if binaire[k] == 'b':
                break
            # Si notre bit est égale à 1, ça veut dire qu'il va falloir changer la valeur du pixel
            if binaire[k] == '1':
                # On calcul la collone du pixel
                coordX = (chip8.V[x] + k + 8) % 64
                # Si le pixel est éteint on l'allume
                if chip8.tabEcran[coordY][coordX] == 0:
                    chip8.tabEcran[coordY][coordX] = 1
                    ecran.create_rectangle((coordX*5 + 5, coordY*5 + 5, coordX*5 + 10, coordY*5 + 10), fill="white")
                # Si il était allumé on l'éteint et on met VF à 1
                else:
                    chip8.tabEcran[coordY][coordX] = 0
                    chip8.V[0xF] = 1
                    ecran.create_rectangle((coordX*5 + 5, coordY*5 + 5, coordX*5 + 10, coordY*5 + 10), fill="black")

# Procédure qui va changer les valeurs des registres

def refreshRegistre():
    V0.delete(0, 'end')
    V0.insert(0, chip8.V[0])
    V1.delete(0, 'end')
    V1.insert(0, chip8.V[1])
    V2.delete(0, 'end')
    V2.insert(0, chip8.V[2])
    V3.delete(0, 'end')
    V3.insert(0, chip8.V[3])
    V4.delete(0, 'end')
    V4.insert(0, chip8.V[4])
    V5.delete(0, 'end')
    V5.insert(0, chip8.V[5])
    V6.delete(0, 'end')
    V6.insert(0, chip8.V[6])
    V7.delete(0, 'end')
    V7.insert(0, chip8.V[7])
    V8.delete(0, 'end')
    V8.insert(0, chip8.V[8])
    V9.delete(0, 'end')
    V9.insert(0, chip8.V[9])
    VA.delete(0, 'end')
    VA.insert(0, chip8.V[0xA])
    VB.delete(0, 'end')
    VB.insert(0, chip8.V[0xB])
    VC.delete(0, 'end')
    VC.insert(0, chip8.V[0xC])
    VD.delete(0, 'end')
    VD.insert(0, chip8.V[0xD])
    VE.delete(0, 'end')
    VE.insert(0, chip8.V[0xE])
    VF.delete(0, 'end')
    VF.insert(0, chip8.V[0xF])
    PC.delete(0, 'end')
    PC.insert(0, chip8.PC)
    I.delete(0, 'end')
    I.insert(0, chip8.I)
    DT.delete(0, 'end')
    DT.insert(0, chip8.DT)
    ST.delete(0, 'end')
    ST.insert(0, chip8.ST)
    SP.delete(0, 'end')
    SP.insert(0, chip8.SP)

# Procédure qui va rafraichir l'écran selon le tableau (tabEcran qui stock la valeur des pixels)

def refreshEcran():
    for i, x in enumerate(chip8.tabEcran):
        for j, k in enumerate(x):
            if k == 1:
                ecran.create_rectangle((j * 5 + 5, i * 5 + 5, j * 5 + 10, i * 5 + 10), fill="white")
            else:
                ecran.create_rectangle((j * 5 + 5, i * 5 + 5, j * 5 + 10, i * 5 + 10), fill="black")

# Procédure qui va changer la valeur des touches, appuyée ou non

def touche(event):
    if event.char == "&":
        chip8.tabTouche[0] = 1
    if event.char == "é":
        chip8.tabTouche[1] = 1
    if event.char == '"':
        chip8.tabTouche[2] = 1
    if event.char == "'":
        chip8.tabTouche[3] = 1
    if event.char == "a":
        chip8.tabTouche[4] = 1
    if event.char == "z":
        chip8.tabTouche[5] = 1
    if event.char == "e":
        chip8.tabTouche[6] = 1
    if event.char == "r":
        chip8.tabTouche[7] = 1
    if event.char == "q":
        chip8.tabTouche[8] = 1
    if event.char == "s":
        chip8.tabTouche[9] = 1
    if event.char == "d":
        chip8.tabTouche[10] = 1
    if event.char == "f":
        chip8.tabTouche[11] = 1
    if event.char == "w":
        chip8.tabTouche[12] = 1
    if event.char == "x":
        chip8.tabTouche[13] = 1
    if event.char == "c":
        chip8.tabTouche[14] = 1
    if event.char == "v":
        chip8.tabTouche[15] = 1

# On créer la détection des 16 touches

fenetreChip8.bind("<Key>", touche)

# Procédure qui change l'activation ou non des boutons step by step

def stepChange():
    # Si le bouton est checké on autorise le clique sur les boutons avancé et reculé
    if stepActiver.get():
        arriere.config(state=NORMAL)
        avant.config(state=NORMAL)
    # Si le bouton n'est pas checké on interdit le clique sur les boutons avancé et reculé
    else:
        arriere.config(state=DISABLED)
        avant.config(state=DISABLED)

# Procédure qui avance d'une étape

def pcAvant():
    lecture.sauvegarde("savetemp")
    fonctionnement()

# Procédure qui charge un programme lorque le bouton Load est appuyé

def lancement():
    # On initialise la mémoire, registre, etc
    chip8.memoire = [0] * 4096
    chip8.V = [0] * 16
    chip8.I = 0
    chip8.DT = 0
    chip8.ST = 0
    chip8.PC = 512
    chip8.SP = 0
    chip8.saut = [0] * 16
    chip8.nbrSaut = 0
    chip8.tabEcran = [[0 for x in range(64)] for x in range(32)]
    effacerEcran()
    chip8.chargerCaractere()
    ecran.focus_set() # On donne le focus à l'écran
    # On stock le programme en mémoire
    lecture.lecture(programme.get())
    # On lance la procédure fonctionnement pour commencer le programme
    fonctionnement()

# Procédure qui va permettre de voir l'état de la mémoire

def affichageMemoire():
    fenetreMemoire = Tk() # Création d'une nouvelle fenêtre
    fenetreMemoire.configure(width=120, height=150) # On configure la taille
    # On créer une scrollbar pour se déplacer
    scrollbar = Scrollbar(fenetreMemoire)
    scrollbar.pack(side=RIGHT, fill=Y)
    # On créer une "listbox" qui va permettre de stocker/afficher notre mémoire
    mem = Listbox(fenetreMemoire, yscrollcommand=scrollbar.set)
    mem.configure(width=120, height=30)
    # On va boucler sur la mémoire pour la stocker dans la "listbox" que l'on a créer juste avant
    # On affiche 16 valeurs par ligne
    for y in range(256):
        ligne = []
        ligne.append(str(y*16)+' -> '+str(((y*16)+15)))
        for x in range(16):
            ligne.append(hex(chip8.memoire[y*16+x]))
        mem.insert(END, ligne)
    mem.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=mem.yview)
    fenetreMemoire.mainloop() # On lance la fenêtre

# Procédure qui va sauvegarder dans un fichier le contenu de la mémoire, registre, ...

def sauvegarde():
    lecture.sauvegarde(sauvegarde.get())

# Procédure qui va charger une sauvegarde

def charge():
    lecture.chargement(sauvegarde.get())
    refreshEcran()
    refreshRegistre()
    fonctionnement()

# Création des boutons de sauvegarde et de charge

boutonSauv = Button(fenetreChip8, text="Sauver", command=sauvegarde) # On créer le bouton
boutonSauv.grid(column="3", row="15") # On le place
boutonCharge = Button(fenetreChip8, text="Charger", command=charge)
boutonCharge.grid(column="5", row="15")

# Création du label et de l'entrée pour écrire le nom de la sauvegarde

sauvLbl = Label(text="Nom de la Sauvegarde :") # On créer le label
sauvegarde = StringVar() # On créer la variable qui va stocké l'entrée utilisateur
sauv = Entry(fenetreChip8, textvariable=sauvegarde) # On créer l'élément qui va permettre à l'utilisateur d'écrire
sauvLbl.grid(column="4", row="13", columnspan=1) # On place le label
sauv.grid(column="4", row="14", columnspan=1) # On place l'entrée

# Création du bouton de mémoire

boutonMemoire = Button(fenetreChip8, text="Mémoire", command=affichageMemoire)
boutonMemoire.grid(column="3", row="4")

# Création du bouton de relance

boutonRelance = Button(fenetreChip8, text="Relance", command=pcAvant)
boutonRelance.grid(column="5", row="2")

# Création du bouton avant pour se déplacer en step by step

boutonAvant = Button(fenetreChip8, text="->", state=DISABLED, command=pcAvant)
boutonAvant.grid(column="5", row="4")

# Création de la case à cocher pour le step by step

stepActiver = BooleanVar() # On créer la variable booléenne qui va stocker la valeur de la case
stepbystep = Checkbutton(fenetreChip8, text='Step by Step', command=stepChange, variable=stepActiver)
stepbystep.grid(column="4", row="4",)

# Création du label et de l'entrée pour écrire le nom du programme

programme = StringVar()
prgmLbl = Label(text="Nom du programme :")
prgm = Entry(fenetreChip8, textvariable=programme)
prgmLbl.grid(column="4", row="0")
prgm.grid(column="4", row="1")

# Création du bouton pour charger le programme

load = Button(fenetreChip8, text="Load", command=lancement)
load.grid(column="4", row="2")

# Création de l'écran du chip8

ecran = Canvas(fenetreChip8, width=327, height=167, bg="black")
ecran.grid(column="1", row="5", rowspan=8, columnspan=6)

# Création de l'affichage des registres

V0Lbl = Label(text="V0 :")
valeurV0 = StringVar()
V0 = Entry(fenetreChip8, textvariable=valeurV0, width="5")
V0Lbl.grid(column="8", row="0")
V0.grid(column="9", row="0")
V1Lbl = Label(text="V1 :")
valeurV1 = StringVar()
V1 = Entry(fenetreChip8, textvariable=valeurV1, width="5")
V1Lbl.grid(column="8", row="1")
V1.grid(column="9", row="1")
V2Lbl = Label(text="V2 :")
valeurV2 = StringVar()
V2 = Entry(fenetreChip8, textvariable=valeurV2, width="5")
V2Lbl.grid(column="8", row="2")
V2.grid(column="9", row="2")
V3Lbl = Label(text="V3 :")
valeurV3 = StringVar()
V3 = Entry(fenetreChip8, textvariable=valeurV3, width="5")
V3Lbl.grid(column="8", row="3")
V3.grid(column="9", row="3")
V4Lbl = Label(text="V4 :")
valeurV4 = StringVar()
V4 = Entry(fenetreChip8, textvariable=valeurV4, width="5")
V4Lbl.grid(column="8", row="4")
V4.grid(column="9", row="4")
V5Lbl = Label(text="V5 :")
valeurV5 = StringVar()
V5 = Entry(fenetreChip8, textvariable=valeurV5, width="5")
V5Lbl.grid(column="8", row="5")
V5.grid(column="9", row="5")
V6Lbl = Label(text="V6 :")
valeurV6 = StringVar()
V6 = Entry(fenetreChip8, textvariable=valeurV6, width="5")
V6Lbl.grid(column="8", row="6")
V6.grid(column="9", row="6")
V7Lbl = Label(text="V7 :")
valeurV7 = StringVar()
V7 = Entry(fenetreChip8, textvariable=valeurV7, width="5")
V7Lbl.grid(column="8", row="7")
V7.grid(column="9", row="7")
V8Lbl = Label(text="V8 :")
valeurV8 = StringVar()
V8 = Entry(fenetreChip8, textvariable=valeurV8, width="5")
V8Lbl.grid(column="8", row="8")
V8.grid(column="9", row="8")
V9Lbl = Label(text="V9 :")
valeurV9 = StringVar()
V9 = Entry(fenetreChip8, textvariable=valeurV9, width="5")
V9Lbl.grid(column="8", row="9")
V9.grid(column="9", row="9")
VALbl = Label(text="VA :")
valeurVA = StringVar()
VA = Entry(fenetreChip8, textvariable=valeurVA, width="5")
VALbl.grid(column="8", row="10")
VA.grid(column="9", row="10")
VBLbl = Label(text="VB :")
valeurVB = StringVar()
VB = Entry(fenetreChip8, textvariable=valeurVB, width="5")
VBLbl.grid(column="8", row="11")
VB.grid(column="9", row="11")
VCLbl = Label(text="VC :")
valeurVC = StringVar()
VC = Entry(fenetreChip8, textvariable=valeurVC, width="5")
VCLbl.grid(column="8", row="12")
VC.grid(column="9", row="12")
VDLbl = Label(text="VD :")
valeurVD = StringVar()
VD = Entry(fenetreChip8, textvariable=valeurVD, width="5")
VDLbl.grid(column="8", row="13")
VD.grid(column="9", row="13")
VELbl = Label(text="VE :")
valeurVE = StringVar()
VE = Entry(fenetreChip8, textvariable=valeurVE, width="5")
VELbl.grid(column="8", row="14")
VE.grid(column="9", row="14")
VFLbl = Label(text="VF :")
valeurVF = StringVar()
VF = Entry(fenetreChip8, textvariable=valeurVF, width="5")
VFLbl.grid(column="8", row="15")
VF.grid(column="9", row="15")
PCLbl = Label(text="PC :")
valeurPC = StringVar()
PC = Entry(fenetreChip8, textvariable=valeurPC, width="5")
PCLbl.grid(column="10", row="6")
PC.grid(column="11", row="6")
ILbl = Label(text="I :")
valeurI = StringVar()
I = Entry(fenetreChip8, textvariable=valeurI, width="5")
ILbl.grid(column="10", row="7")
I.grid(column="11", row="7")
DTLbl = Label(text="DT :")
valeurDT = StringVar()
DT = Entry(fenetreChip8, textvariable=valeurDT, width="5")
DTLbl.grid(column="10", row="8")
DT.grid(column="11", row="8")
STLbl = Label(text="ST :")
valeurST = StringVar()
ST = Entry(fenetreChip8, textvariable=valeurST, width="5")
STLbl.grid(column="10", row="9")
ST.grid(column="11", row="9")
SPLbl = Label(text="SP :")
valeurSP = StringVar()
SP = Entry(fenetreChip8, textvariable=valeurSP, width="5")
SPLbl.grid(column="10", row="10")
SP.grid(column="11", row="10")

fenetreChip8.mainloop() # lancement de la fenêtre

