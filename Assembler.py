import sys, re

OPC = {
    "LDA":0x0, "STA":0x1, "MOV":0x2, "INB":0x3, "OUT":0x4, "JMP":0x5, "JIF":0x6, "HLT":0x7,
    "ADD":0x8, "SUB":0x9, "CMP":0xA, "AND":0xB, "OR":0xC, "XOR":0xD, "NOT":0xE, "RND":0xF,
    "DATA":0xFF}
REG = {
    "AC":0x0, "RX":0x1, "RY":0x2, "RZ":0x3}
FLAG = {
    "C":0x0, "A":0x1, "E":0x2, "Z":0x3}

lines = []
pc = 0x00
memory = []

#generate memory map
m = 0
for m in range(0, 255):
    memory.append(0x00)
    m += 1
#print(memory)

#split by lines
f = open(sys.argv[1], mode='r')
file = f.read()
lines = re.split("\n", file)
print("\nv3.0 hex words addressed")

#1-pass system; read-decode-write each line, proceed to next line
i = 0
for i in range (0, len(lines)):
    ignorecomment = re.split("//", str(lines[i]))
    line = re.split("\s", str(ignorecomment[0]))
    opcode = OPC.get(line[0])
    if (opcode == 0x7):
        segment2nd = line[0]
    else:
        segment2nd = line[1]
    if ((opcode == 0x00) or (opcode == 0x01)):  #LDA, STA
        comp = re.split(",", segment2nd)
        regs = REG.get(comp[0])
        addrstr = comp[1]
        addr = int(addrstr[1:], base=16)
        header = opcode*16 + regs*4
        print(f"{pc:#0{4}x}:"[2:], f"{header:#0{4}x}"[2:], f"{addr:#0{4}x}"[2:]); pc += 2
    if ((opcode == 0x02) or ((opcode >= 0x08) and (opcode != 0xFF))):  #MOV, Maths
        comp = re.split(",", segment2nd)
        reg1 = REG.get(comp[0])
        reg2 = REG.get(comp[1])
        header = opcode*16 + reg1*4 +reg2*1
        print(f"{pc:#0{4}x}:"[2:], f"{header:#0{4}x}"[2:]); pc += 1
    if ((opcode == 0x03) or (opcode == 0x04)):  #INB, OUT
        comp = re.split(",", segment2nd)
        addr = int(comp[0][1:], base = 16)
        header = opcode*16
        print(f"{pc:#0{4}x}:"[2:], f"{header:#0{4}x}"[2:], f"{addr:#0{4}x}"[2:]); pc += 2
    if ((opcode == 0x05) or (opcode == 0x06)):  #JMP, JIF
        comp = re.split(",", segment2nd)
        addr = int(comp[0][1:], base = 16)
        if len(comp) == 2:
            flag = FLAG.get(comp[1])
        else:
            flag = 0
            pass
        header = opcode*16 + flag*4
        print(f"{pc:#0{4}x}:"[2:], f"{header:#0{4}x}"[2:], f"{addr:#0{4}x}"[2:]); pc += 2
    if (opcode == 0x07):    #HLT
        header = opcode*16
        print(f"{pc:#0{4}x}:"[2:], f"{header:#0{4}x}"[2:]); pc += 1
    if (opcode == 0xFF):  #DATA
        comp = re.split(",", segment2nd)
        datastr = comp[0]
        addrstr = comp[1]
        addr = int(addrstr[1:], base=16)
        data = int(datastr, base=16)
        header = opcode*16 + regs*4
        print(f"{addr:#0{4}x}:"[2:], f"{data:#0{4}x}"[2:])
    i += 1
