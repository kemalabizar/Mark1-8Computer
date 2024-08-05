import sys, re

OPC = {
    "LDA":0x0, "STA":0x1, "MOV":0x2, "INB":0x3, "OUT":0x4, "JMP":0x5, "JIF":0x6, "HLT":0x7,
    "ADD":0x8, "SUB":0x9, "CMP":0xA, "AND":0xB, "OR":0xC, "XOR":0xD, "NOT":0xE, "RND":0xF,
    "DATA":0xFF}
REG = {
    "AC":0x0, "RX":0x1, "RY":0x2, "RZ":0x3}
FLAG = {
    "C":0x0, "A":0x1, "E":0x2, "Z":0x3}
MEMLENGTH = {
    "LDA":2, "STA":2, "MOV":1, "INB":2, "OUT":2, "JMP":2, "JIF":2, "HLT":1,
    "ADD":1, "SUB":1, "CMP":1, "AND":1, "OR":1, "XOR":1, "NOT":1, "RND":1}

pc = 0x00

#2-pass system

'''
1. The code is separated by ":" signs that indicate major loops, and are then labeled
2. Each loop would have the instructions examined, and subsequent memory span determined
3. After all loop's memory span is calculated, each loop is assigned their starting memory location
(e.g. loop MAIN is 1st and spans 8, CMPR is 2nd and spans 5.
As such, MAIN starts at $00, while CMPR starts at $00 + span of MAIN - 1 = $07)
4. Every JMP and JIF instructions would go to corresponding loops only, e.g. JMP MAJORLOOP; JIF 2NDLOOP,E
5. After that, other instructions are then assembled.
'''

#split by loop separators ":"
f = open(sys.argv[1], mode='r')
file = f.read()
loops = re.split(":", file)
loops.remove("")
print("\nv3.0 hex words addressed\n")
#print(loops)

#1st pass: labelize and calculate loop length into loopdict
loopdict = {}
looplen = 0
loopsign = ""
for i in range(0, len(loops)):
    loops[i] = re.split("\n", loops[i])
    sep = loops[i]
    while "" in sep:
        sep.remove("")
    loops[i] = sep
    m = 0
    for j in range(1, len(loops[i])):
        cont = re.split(" ", (loops[i])[j])
        if cont[0] in ["LDA", "STA", "INB", "OUT", "JMP", "JIF", "DATA"]:
            looplen += 2
        else:
            looplen += 1
        #print(cont)
        j += 1
    loopsign = loops[i][0]
    loopdict[loopsign] = looplen
    looplen = 0
    i += 1
print(loopdict, end="\n\n")

inst_string = ""
#2nd pass: decode and finalize instructions
for i in range(0, len(loops)):
    for j in range(1, len(loops[i])):
        cont = re.split(" ", (loops[i])[j])
        #print(cont)
        indices = OPC.get(cont[0])
        if (indices == 0x0) or (indices == 0x1):    # LDA, STA
            operand = re.split(",", cont[1])
            byte1 = indices*16 + REG.get(operand[0])*4
            byte2 = int(operand[1][1:], base=16)
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:], f"{byte2:#0{4}x}"[2:]); pc += 2
        if (indices == 0x3) or (indices == 0x4): pass    # INB, OUT
        if (indices == 0x5) or (indices == 0x6):    # JMP, JIF
            operand = re.split(",", cont[1])
            byte1 = indices*16
            if len(operand) == 2:
                byte1 = byte1 + FLAG.get(operand[1])*4
            else: pass
            byte2 = 
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:], f"{byte2:#0{4}x}"[2:]); pc += 2
        else: pass
        j += 1
    print("\n")
    i += 1
