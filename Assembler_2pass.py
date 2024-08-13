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

loop_len_dict = {}
loop_loc_dict = {}
#1st pass: labelize and calculate memory length of each inst. loops, categorize into a dict {"loopheader":int(memorysize)}
for i in range(0, len(loops)):
    loops[i] = re.split("\n", loops[i])
    loop_len = 0
    #print(loops[i], end="\n\n")
    end = len(loops[i])-1
    part = loops[i]
    if part[end] == "":
        part.pop()
        loops[i] = part
    else:
        pass
    for j in range(1, len(loops[i])):
        loops[i][j] = re.split(" ", loops[i][j])
        opcode = OPC.get(loops[i][j][0])
        if (opcode != 0x2) and (opcode < 0x8) and (opcode != 0x7):
            loop_len += 2
        else:
            loop_len += 1
        #print(loops[i][j], "\t", loop_len)
        j += 1
    loop_len_dict[loops[i][0]] = loop_len
    i += 1
#print(loop_len_dict)
loop_loc_dict[loops[0][0]] = 0x00
for i in range(1, len(loops)):
    pc += loop_len_dict.get(loops[i-1][0])
    loop_loc_dict[loops[i][0]] = pc
    i += 1
print(loop_loc_dict); pc = 0x00

#2nd pass: re-read the whole loop, and generate proper bytes
for i in range(0, len(loops)):
    for j in range(0, len(loops[i])):
        opcode = OPC.get(loops[i][j][0])
            if (opcode == 0x0) or (opcode == 0x1): #LDA, STA
                operand = re.split(",", loops[i][j][1])
                byte1 = opcode*16 + REG.get(operand[0])*4
                byte2 = int(operand[1][1:], base=16)
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:], f"{byte2:#0{4}x}:"[2:]); pc += 2
            if (opcode == 0x3) or (opcode == 0x4): #INB, OUT
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:], f"{byte2:#0{4}x}:"[2:]); pc += 2
            if (opcode == 0x5): #JMP
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:], f"{byte2:#0{4}x}:"[2:]); pc += 2
            if (opcode == 0x6): #JIF
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:], f"{byte2:#0{4}x}:"[2:]); pc += 2
            if (opcode == 0x7): #HLT
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:]); pc += 1
            if (opcode >= 0x8) and (opcode != 0xFF): #MATH
                print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}:"[2:]); pc += 1
            else: #DATA
        j += 1
    i += 1
