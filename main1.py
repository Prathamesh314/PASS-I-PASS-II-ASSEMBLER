
from tabulate import tabulate
import pandas as pd

v={"LA":4,"SR":2,"L":4,"AR":2,"A":4,"C":4,"BNE":4,"LR":2,"ST":4,"BR":2}
psuedoop = ["START","USING","EQU"]

symbol_table = {}
literal_table = {}
base_table = {}
literals = []
lc_table = []
lc = 0
symbolLength = []
with open("input file.txt",'r') as input:
    inst = input.readlines()
    for i in inst:
        if("END" in i):
            lc_table.append([lc,"END"])
        else:
            lc_table.append([lc,i])
        t = i.split()
        if("START" in t):
            symbol_table[t[0]] = lc
            # symbolLength.append(1)
        if("USING" in t):
            val = t[1].split(',')
            try:
                if(val[0]=="*"):
                    base_table[int(val[1])] = lc
                else:
                    base_table[int(val[1])] = symbol_table[val[0]]
            except:
                pass
        if("EQU" in t):
            if(t[2] == "*"):
                symbol_table[t[0]] = lc
                # symbolLength.append(1)
            else:
                try:
                    symbol_table[t[0]] = int(t[2])
                    # symbolLength.append(4)
                except:
                    pass
        if(t[0] in v):
            val = t[1].split(',')
            if(len(val)>1 and val[1][0:1] == '='):
                literals.append(val[1])
                try:
                    if(t[0] == 'A' and val[0] in symbol_table):
                        symbol_table[val[0]]+=int(val[1][3:len(val[1])-1])
                    else:
                        symbol_table[val[0]] = int(val[1][3:len(val[1])-1])
                except:
                    pass
            lc+=v[t[0]]
        if("END" in t):
            break;
        else:
            if(t[1] == "DC"):
                lc+=4
            elif(t[1]=="DSÂ"):
                words = t[2][:len(t[2])-1]
                lc+=int(words)*4

r = lc%8
lc = lc+(8-r)
for i in literals:
    literal_table[i] = lc
    lc+=4
SYMBOLS = []
LITERALS = []
BASES = []
for i in range(len(lc_table)):
    lc = lc_table[i][0]
    instr = lc_table[i][1]
    instrlist = instr.split()
    if("USING" in instrlist):
        spl = instrlist[1].split(',')
        if('*' in spl):
            BASES.append((lc,spl[1]))
        else:
            BASES.append((spl[0],spl[1]))
    elif("START" in instrlist):
        SYMBOLS.append((lc,instrlist[0]))
        symbolLength.append(1)
    elif("DC" in instrlist):
        SYMBOLS.append((lc,instrlist[0]))
        symbolLength.append(4)
    elif("DSÂ" in instrlist):
        SYMBOLS.append((lc,instrlist[0]))
        symbolLength.append(4)

MOT_CODE = {}
base = BASES[0][1]
value = BASES[0][0]
for i in SYMBOLS:
    address = i[0]
    offset = address - value
    if(offset >= 0):
        second = str(offset)+"( 0," + str(base) + ")"
        MOT_CODE[i[1]] = second


print("************* PASS I ASSEMBLER ***************")
pass1 = {}
for i in lc_table:
    pass1[i[0]] = i[1][:len(i[1])-1]

# print(pass1)
dict3 = {
    "LC":pass1.keys(),
    "Instructions":pass1.values()
}

df2 = pd.DataFrame(dict3)
print(df2)

ANS = []

for i in lc_table:
    t = i[1].split()
    if (t[0] in v):
        new_T = t[1].split(',')
        # print(new_T[1])
        if(new_T[1] in MOT_CODE):
            ss = t[1]
            ss = ss.replace(new_T[1],MOT_CODE[new_T[1]])
            ANS.append([i[0],ss])
        else:
            ANS.append(i)
    else:
        ANS.append(i)

FINALANS = []
for i in ANS:
    if ("USING" not in i[1].split()):
        FINALANS.append(i)




print("************* PASS II ASSEMBLER ***************")
pass2 = {}
for i in FINALANS:
    pass2[i[0]] = i[1][:len(i[1])]

# print(pass1)
dict4 = {
    "LC":pass2.keys(),
    "Instructions":pass2.values()
}

df3 = pd.DataFrame(dict4)

print(df3)

dict1 = {
    "BASE":base_table.keys(),
    "VALUE":base_table.values()
}

df = pd.DataFrame(dict1)
print("\n***** Base Table *****")
print(df)

# print(literal_table)

dict5 = {
    "Literal":literal_table.keys(),
    "Value":literal_table.values()
}

df4 = pd.DataFrame(dict5)
print("\n**** Literal Table ****")
print(df4)

SYMBOLS_DICT = {}
for i in SYMBOLS:
    SYMBOLS_DICT[i[0]] = i[1]

dict2 = {
    "Symbols":SYMBOLS_DICT.values(),
    "LC":SYMBOLS_DICT.keys(),
    "Length":symbolLength,
    "Relocation":['R' for i in range(len(SYMBOLS_DICT))]
}

df2 = pd.DataFrame(dict2)
print("\n***** Symbol Table *****")
print(df2)