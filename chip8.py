
# Création de la mémoire

memoire  =  [0] * 4096

# 16 registres 8-bit V0 -> VF

V  =  [0] * 16

# registre I 16-bit

I  =  0

# 2 registre pour le son et le délai

DT  =  0
ST  =  0

# PC 16-bit utilisé pour se déplacer dans le programme

PC  =  512

# SP 8-bit Stack Pointer, permet de compter dans le tas

SP  =  0

# Gestion des sauts

saut  =  [0] * 16
nbrSaut  =  0

# Tableau représentant les pixels éteints/allumés

tabEcran  =  [[0] * 64] * 32

# Procédure qui écrit en mémoire les sprites de base (1 à 9 et A à F)

def chargerCaractere():
    # 0
    memoire[0] = 0xF0
    memoire[1] = 0x90
    memoire[2] = 0x90
    memoire[3] = 0x90
    memoire[4] = 0xF0
    # 1
    memoire[5] = 0x20
    memoire[6] = 0x60
    memoire[7] = 0x20
    memoire[8] = 0x20
    memoire[9] = 0x70
    # 2
    memoire[10] = 0xF0
    memoire[11] = 0x10
    memoire[12] = 0xF0
    memoire[13] = 0x80
    memoire[14] = 0xF0
    # 3
    memoire[15] = 0xF0
    memoire[16] = 0x10
    memoire[17] = 0xF0
    memoire[18] = 0x10
    memoire[19] = 0xF0
    # 4
    memoire[20] = 0x90
    memoire[21] = 0x90
    memoire[22] = 0xF0
    memoire[23] = 0x10
    memoire[24] = 0x10
    # 5
    memoire[25] = 0xF0
    memoire[26] = 0x80
    memoire[27] = 0xF0
    memoire[28] = 0x10
    memoire[29] = 0xF0
    # 6
    memoire[30] = 0xF0
    memoire[31] = 0x80
    memoire[32] = 0xF0
    memoire[33] = 0x90
    memoire[34] = 0xF0
    # 7
    memoire[35] = 0xF0
    memoire[36] = 0x10
    memoire[37] = 0x20
    memoire[38] = 0x40
    memoire[39] = 0x40
    # 8
    memoire[40] = 0xF0
    memoire[41] = 0x90
    memoire[42] = 0xF0
    memoire[43] = 0x90
    memoire[44] = 0xF0
    # 9
    memoire[45] = 0xF0
    memoire[46] = 0x90
    memoire[47] = 0xF0
    memoire[48] = 0x10
    memoire[49] = 0xF0
    # A
    memoire[50] = 0xF0
    memoire[51] = 0x90
    memoire[52] = 0xF0
    memoire[53] = 0x90
    memoire[54] = 0x90
    # B
    memoire[55] = 0xE0
    memoire[56] = 0x90
    memoire[57] = 0xE0
    memoire[58] = 0x90
    memoire[59] = 0xE0
    # C
    memoire[60] = 0xF0
    memoire[61] = 0x80
    memoire[62] = 0x80
    memoire[63] = 0x80
    memoire[64] = 0xF0
    # D
    memoire[65] = 0xE0
    memoire[66] = 0x90
    memoire[67] = 0x90
    memoire[68] = 0x90
    memoire[69] = 0xE0
    # E
    memoire[70] = 0xF0
    memoire[71] = 0x80
    memoire[72] = 0xF0
    memoire[73] = 0x80
    memoire[74] = 0xF0
    # F
    memoire[75] = 0xF0
    memoire[76] = 0x80
    memoire[77] = 0xF0
    memoire[78] = 0x80
    memoire[79] = 0x80