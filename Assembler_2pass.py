import sys, re

OPC = {
    "LDA":0x0, "STA":0x1, "MOV":0x2, "INB":0x3, "OUT":0x4, "JMP":0x5, "JIF":0x6, "HLT":0x7,
    "ADD":0x8, "SUB":0x9, "CMP":0xA, "AND":0xB, "OR":0xC, "XOR":0xD, "NOT":0xE, "RND":0xF,
    "DATA":0xFF}
REG = {
    "AC":0x0, "RX":0x1, "RY":0x2, "RZ":0x3}
FLAG = {
    "C":0x0, "A":0x1, "E":0x2, "Z":0x3}
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

#1st pass: labelize and calculate memory length of each inst. loops, categorize into a dict {"loopheader":int(memorysize)}
loop_len_dict = {}
loop_loc_dict = {}
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
        if ((opcode in range(0, 7)) and (opcode != 0x2)) or (opcode == 0xFF):
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
#print(loop_loc_dict, end="\n\n")
pc = 0x00

#2nd pass: re-read the whole loop, and generate proper bytes
for i in range(0, len(loops)):
    #print(loops[i][0])
    for j in range(1, len(loops[i])):
        opcode = OPC.get(loops[i][j][0])
        if len(loops[i][j]) == 2: operand = re.split(",", loops[i][j][1])
        else: pass
        """
        if len(loops[i][j]) == 2:
            print(loops[i][j][0], f"{opcode:#0{4}x}"[2:], loops[i][j][1])
        else:
            print(loops[i][j][0], f"{opcode:#0{4}x}"[2:])
        """
        #
        #
        if (opcode == 0x0) or (opcode == 0x1): #LDA, STA
            reg = REG.get(operand[0])
            byte1 = opcode*16 + reg*4
            byte2 = int(operand[1][1:], base=16)
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:], f"{byte2:#0{4}x}"[2:]); pc += 2
        if (opcode == 0x2) or ((opcode >= 0x8) and (opcode != 0xFF)): #MOV, MATH
            reg1, reg2 = REG.get(operand[0]), REG.get(operand[1])
            byte1 = opcode*16 + reg1*4 + reg2*1
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:]); pc += 1
        if (opcode == 0x3) or (opcode == 0x4):  #INB, OUT
            byte1 = opcode*16
            byte2 = int(operand[0][1:], base=16)
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:], f"{byte2:#0{4}x}"[2:]); pc += 2
        if (opcode == 0x5) or (opcode == 0x6):  #JMP, JIF
            byte1 = opcode*16
            if (opcode == 0x6): #JIF flag calculation
                flag = FLAG.get(operand[1])
                byte1 += (flag*4)
            else: pass
            byte2 = loop_loc_dict.get(operand[0])
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:], f"{byte2:#0{4}x}"[2:]); pc += 2
        if (opcode == 0x7): #HLT
            byte1 = opcode*16
            print(f"{pc:#0{4}x}:"[2:], f"{byte1:#0{4}x}"[2:]); pc += 1
        if (opcode == 0xFF):    #DATA
            dataValue = int(operand[0], base=16)
            dataAddr = int(operand[1][1:], base=16)
            print(f"{dataAddr:#0{4}x}:"[2:], f"{dataValue:#0{4}x}"[2:])
        else: pass
        j += 1
    i += 1
