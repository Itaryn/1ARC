
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

tabEcran  = [[0 for x in range(64)] for x in range(32)]

# Tableau qui stocke les valeurs des touches

tabTouche = [0] * 16

# Procédure qui écrit en mémoire les sprites de base (1 à 9 et A à F)

def chargerCaractere():
    # 0
    memoire[0] = 0b11110000
    memoire[1] = 0b10010000
    memoire[2] = 0b10010000
    memoire[3] = 0b10010000
    memoire[4] = 0b11110000
    # 1
    memoire[5] = 0b00100000
    memoire[6] = 0b01100000
    memoire[7] = 0b00100000
    memoire[8] = 0b00100000
    memoire[9] = 0b01110000
    # 2
    memoire[10] = 0b11110000
    memoire[11] = 0b00010000
    memoire[12] = 0b11110000
    memoire[13] = 0b10000000
    memoire[14] = 0b11110000
    # 3
    memoire[15] = 0b11110000
    memoire[16] = 0b00010000
    memoire[17] = 0b11110000
    memoire[18] = 0b00010000
    memoire[19] = 0b11110000
    # 4
    memoire[20] = 0b10010000
    memoire[21] = 0b10010000
    memoire[22] = 0b11110000
    memoire[23] = 0b00010000
    memoire[24] = 0b00010000
    # 5
    memoire[25] = 0b11110000
    memoire[26] = 0b10000000
    memoire[27] = 0b11110000
    memoire[28] = 0b00010000
    memoire[29] = 0b11110000
    # 6
    memoire[30] = 0b11110000
    memoire[31] = 0b10000000
    memoire[32] = 0b11110000
    memoire[33] = 0b10010000
    memoire[34] = 0b11110000
    # 7
    memoire[35] = 0b11110000
    memoire[36] = 0b00010000
    memoire[37] = 0b00100000
    memoire[38] = 0b01000000
    memoire[39] = 0b01000000
    # 8
    memoire[40] = 0b11110000
    memoire[41] = 0b10010000
    memoire[42] = 0b11110000
    memoire[43] = 0b10010000
    memoire[44] = 0b11110000
    # 9
    memoire[45] = 0b11110000
    memoire[46] = 0b10010000
    memoire[47] = 0b11110000
    memoire[48] = 0b00010000
    memoire[49] = 0b11110000
    # A
    memoire[50] = 0b11110000
    memoire[51] = 0b10010000
    memoire[52] = 0b11110000
    memoire[53] = 0b10010000
    memoire[54] = 0b10010000
    # B
    memoire[55] = 0b11100000
    memoire[56] = 0b10010000
    memoire[57] = 0b11100000
    memoire[58] = 0b10010000
    memoire[59] = 0b11100000
    # C
    memoire[60] = 0b11110000
    memoire[61] = 0b10000000
    memoire[62] = 0b10000000
    memoire[63] = 0b10000000
    memoire[64] = 0b11110000
    # D
    memoire[65] = 0b11100000
    memoire[66] = 0b10010000
    memoire[67] = 0b10010000
    memoire[68] = 0b10010000
    memoire[69] = 0b11100000
    # E
    memoire[70] = 0b11110000
    memoire[71] = 0b10000000
    memoire[72] = 0b11110000
    memoire[73] = 0b10000000
    memoire[74] = 0b11110000
    # F
    memoire[75] = 0b11110000
    memoire[76] = 0b10000000
    memoire[77] = 0b11110000
    memoire[78] = 0b10000000
    memoire[79] = 0b10000000